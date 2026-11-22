"""Vozes grátis em português (rodam localmente).

Vozes base:
  kokoro:pf_dora  (feminina)      kokoro:pm_alex (masculina)   kokoro:pm_santa (masculina grave)
  piper:faber     (masculina)     piper:cadu     (masculina)   piper:jeff      (masculina)
Ajustes por personagem: "pitch" (0.8 grave … 1.25 agudo, ex.: criança 1.18) e "speed" (0.85 … 1.15).
Os modelos ficam em ~/.cache/mh_vozes (baixados do HuggingFace na primeira vez).
"""
import os, re, subprocess, tempfile, urllib.request
import numpy as np

CACHE = os.path.expanduser("~/.cache/mh_vozes")
HF = "https://huggingface.co"
KOKORO_FILES = {
    "kokoro.onnx": f"{HF}/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/onnx/model_quantized.onnx",
    **{f"{v}.bin": f"{HF}/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/voices/{v}.bin"
       for v in ("pf_dora", "pm_alex", "pm_santa")},
}
PIPER = ("faber", "cadu", "jeff")
SR = 44100
_kokoro = None
_piper = {}


def _get(name, url):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p) or os.path.getsize(p) < 1000:
        urllib.request.urlretrieve(url, p)
    return p


def _kokoro_model():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        for n, u in KOKORO_FILES.items():
            _get(n, u)
        npz = os.path.join(CACHE, "voices_pt.npz")
        if not os.path.exists(npz):
            v = {n: np.fromfile(os.path.join(CACHE, f"{n}.bin"), dtype=np.float32).reshape(-1, 1, 256)
                 for n in ("pf_dora", "pm_alex", "pm_santa")}
            np.savez(npz, **v)
        _kokoro = Kokoro(os.path.join(CACHE, "kokoro.onnx"), npz)
    return _kokoro


def _piper_voice(name):
    if name not in _piper:
        from piper import PiperVoice
        base = f"{HF}/rhasspy/piper-voices/resolve/main/pt/pt_BR/{name}/medium/pt_BR-{name}-medium"
        m = _get(f"pt_BR-{name}-medium.onnx", base + ".onnx")
        _get(f"pt_BR-{name}-medium.onnx.json", base + ".onnx.json")
        _piper[name] = PiperVoice.load(m)
    return _piper[name]


def clean(text):
    t = text.replace("*", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _raw(engine, voice, text):
    if engine == "kokoro":
        a, sr = _kokoro_model().create(text, voice=voice, speed=1.0, lang="pt-br")
        return np.asarray(a, dtype=np.float32), sr
    v = _piper_voice(voice)
    chunks = list(v.synthesize(text))
    a = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
    return a, chunks[0].sample_rate


# Vozes "piper" antigas viram misturas do Kokoro (soam bem mais naturais); cada uma continua diferente.
MISTURAS = {
    "piper:faber": {"pm_alex": 0.7, "pm_santa": 0.3},
    "piper:cadu": {"pm_alex": 0.45, "pm_santa": 0.55},
    "piper:jeff": {"pm_santa": 0.85, "pm_alex": 0.15},
}


def _voz_kokoro(nome):
    """'kokoro:pm_alex' ou 'kokoro:mix:pm_alex*0.6+pm_santa*0.4' -> nome ou vetor de estilo."""
    k = _kokoro_model()
    if nome in MISTURAS:
        partes = MISTURAS[nome]
    elif nome.startswith("kokoro:mix:"):
        partes = {}
        for p in nome.split(":", 2)[2].split("+"):
            v, w = p.split("*")
            partes[v.strip()] = float(w)
    else:
        return nome.split(":", 1)[1]
    tot = sum(partes.values())
    return sum(k.voices[v] * (w / tot) for v, w in partes.items())


def synth(spec, text):
    """spec: {"voz": "...", "pitch": 1.0, "speed": 1.0}. Retorna mono float32 a 44.1 kHz.
    Melhorias: só Kokoro (mais natural), pausas de fala, tom ajustado sem 'voz de robô'
    (rubberband preservando formantes, variação limitada) e tratamento de áudio (graves, presença,
    compressão leve e um pouco de ambiente)."""
    voz = spec.get("voz", "kokoro:pm_alex")
    pitch = min(1.08, max(0.93, float(spec.get("pitch", 1.0))))
    speed = min(1.12, max(0.85, float(spec.get("speed", 1.0)))) * 0.97
    k = _kokoro_model()
    a, sr = k.create(clean(text), voice=_voz_kokoro(voz), speed=speed, lang="pt-br",
                     sentence_pause=0.32, clause_pause=0.14)
    a = np.asarray(a, dtype=np.float32)
    with tempfile.TemporaryDirectory() as td:
        i, o = os.path.join(td, "i.f32"), os.path.join(td, "o.f32")
        a.tofile(i)
        af = (f"aresample={SR},"
              f"rubberband=pitch={pitch:.4f}:formant=preserved:transients=smooth,"
              "highpass=f=75,lowpass=f=11500,"
              "equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=3,deesser=i=0.3,"
              "acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,"
              "aecho=0.85:0.5:28|46:0.10|0.06,"
              "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
              "silenceremove=start_periods=1:start_threshold=-45dB,areverse")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", i,
                        "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", o], check=True)
        out = np.fromfile(o, dtype=np.float32)
    peak = np.max(np.abs(out)) + 1e-9
    return out / peak * 0.9


if __name__ == "__main__":
    import sys, wave
    spec = {"voz": sys.argv[1]}
    if len(sys.argv) > 3:
        spec["pitch"] = float(sys.argv[3])
    a = synth(spec, sys.argv[2])
    with wave.open("teste_voz.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())
    print(len(a) / SR, "s")
