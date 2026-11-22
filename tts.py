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


def synth(spec, text):
    """spec: {"voz": "kokoro:pf_dora", "pitch": 1.0, "speed": 1.0}. Retorna mono float32 a 44.1 kHz."""
    engine, voice = spec.get("voz", "kokoro:pm_alex").split(":")
    a, sr = _raw(engine, voice, clean(text))
    pitch = float(spec.get("pitch", 1.0))
    speed = float(spec.get("speed", 1.0))
    with tempfile.TemporaryDirectory() as td:
        i, o = os.path.join(td, "i.f32"), os.path.join(td, "o.f32")
        a.tofile(i)
        tempo = speed / pitch
        chain = []
        while tempo > 2.0:
            chain.append("atempo=2.0"); tempo /= 2.0
        while tempo < 0.5:
            chain.append("atempo=0.5"); tempo /= 0.5
        chain.append(f"atempo={tempo:.4f}")
        af = f"asetrate={int(sr * pitch)},aresample={SR}," + ",".join(chain) + \
             ",silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
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
