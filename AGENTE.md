# Manual do agente: @mundoemhistorias

Este repositório produz e publica sozinho histórias em partes no Instagram **@mundoemhistorias**.
A cada horário agendado (9h, 12h, 15h, 18h e 21h, America/Campo_Grande) você publica **um** vídeo novo.
O dono da conta autorizou a publicação sem aprovação prévia.

## Arquivos

- `engine.py`: motor de vídeo (1080x1920, legenda grande, trilha sintetizada, capa). Não altere sem necessidade.
- `tts.py`: vozes grátis em português (Kokoro e Piper), uma por personagem. Antes de renderizar: `pip install --break-system-packages kokoro-onnx piper-tts soundfile` (os modelos baixam sozinhos do HuggingFace na 1ª vez).
- `tools/render_part.py <slug> <n>`: renderiza a parte `n` e gera `videos/<slug>/parte<n>.mp4` e `capa<n>.jpg`.
- `historias/<slug>/historia.json`: uma história (bíblia, personagens, roteiro de cada parte, status, votos).
- `estado.json`: o que está ativo, qual tipo vem agora e o histórico de posts.

## Várias histórias ao mesmo tempo

- Ficam ativas **4 histórias diferentes ao mesmo tempo**: 2 `continua` (sem votação) e 2 `votacao` (A/B), listadas em `estado.json > ativas`.
- Cada horário publica a parte da **próxima história da fila** (`estado.json > vez` aponta o índice em `ativas`; depois de publicar, avance para o próximo, voltando ao início no fim). Assim o mesmo dia tem histórias variadas e nunca a mesma duas vezes seguidas.
- As 4 precisam ser **bem distintas entre si**: gêneros diferentes (ex.: suspense sobrenatural, mistério policial, drama familiar, ficção científica, sobrevivência, comédia de mistério, romance com segredo), cenários diferentes e protagonistas diferentes (nome, aparência, cores de roupa).
- Toda história tem **exatamente 6 partes**. Quando a parte 6 sair, marque a história como `concluida`, tire-a de `ativas` e, no mesmo lugar da fila, crie uma nova do mesmo tipo e de gênero diferente das outras 3 ativas. Ela entra com a Parte 1 na próxima vez que a fila chegar nela.
- Se `ativas` tiver menos de 4 histórias, crie as que faltam (mantendo 2 de cada tipo) antes de publicar. A nova vai para o fim da fila.

## Passo a passo de cada execução

1. **Evite post duplicado.** Se o último item de `estado.json > historico` foi publicado há menos de 90 minutos, pare e diga "Já publicado neste horário".
2. **Escolha a história**: complete `ativas` até 4 se faltar (veja "Criar história") e pegue `ativas[vez]`.
3. **Defina a parte** = a primeira com status diferente de `publicada`. Nunca diga que uma parte "já está no perfil" se ela ainda não foi publicada. A frase padrão é "A Parte N+1 fica no perfil @mundoemhistorias (sai em até 24h)". Ela é verdadeira porque a fila de 4 histórias garante a próxima parte em menos de 24h.
   - `continua`: o roteiro já está pronto (`status: pronta`).
   - `votacao`: se for a parte 2 a 6, **antes de escrever**: leia todos os comentários da parte anterior, **responda os que ainda não têm resposta** (veja "Responder antes de apurar") e **conte os votos** (veja "Votação"). Escreva o roteiro seguindo a opção vencedora.
4. **Renderize** com `python3 tools/render_part.py <slug> <n>`. Confira: duração entre 50 e 100 s; extraia 2 quadros com ffmpeg e olhe se os personagens, o cenário e a legenda estão certos (a legenda não pode ficar cortada). Se algo estiver errado, corrija o roteiro e renderize de novo.
5. **Suba** o vídeo, a capa e o JSON: `git add -A && git commit -m "<slug> parte <n>" && git push`. Configure antes `git config user.name "mundoemhistorias-bot"` e `git config user.email "bot@mundoemhistorias.local"`.
6. **Confira o link público** (deve responder 200):
   `https://raw.githubusercontent.com/ricardosaback3b-pixel/claude/main/videos/<slug>/parte<n>.mp4`
   (o mesmo vale para `capa<n>.jpg`). Se der 404, espere 20 s e tente de novo, no máximo 5 vezes.
7. **Última conferência (só votação):** logo antes de publicar, leia de novo os comentários da parte anterior. Responda os novos sem resposta e reconte. Se a opção vencedora mudou, reescreva e renderize a parte com a nova escolha antes de publicar.
8. **Publique** com o Windsor.ai (carregue as ferramentas `mcp__Windsor_ai__*` via ToolSearch): `execute_action`, connector `instagram`, account `17841437436804359`, action `create_video_post`, params `{video_url, cover_url, caption, share_to_feed: true}`. Se falhar, tente mais uma vez; se falhar de novo, **não** marque como publicada e avise no resumo.
8b. **Puxe interação logo depois de publicar** (isso ajuda o Instagram a distribuir o vídeo):
   - **Primeiro comentário** no vídeo novo com `create_comment` (`media_id`, `message`): uma pergunta curta que dá vontade de responder, ligada à cena final. Na votação: "Votem aqui 👇 🅰️ ... ou 🅱️ ...?". Varie sempre, nunca repita a frase de outro post.
   - **Story** com `create_story` usando a capa (`image_url` = link raw da `capa<n>.jpg`) para avisar os seguidores que tem parte nova.
   - Se um desses falhar, siga em frente e só cite no resumo.
9. **Registre**: na parte, ponha `status: publicada`, `media_id` e `publicada_em` (ISO, UTC). Em `estado.json`, adicione ao `historico` `{quando, slug, parte, media_id}` e avance `vez` (volta a 0 depois do último). Se foi a parte 6, ponha a história como `concluida` e troque-a em `ativas` por uma nova do mesmo tipo (crie o `historia.json` com a bíblia e, se for `continua`, as 6 partes). Faça commit e push.
10. **Limpeza**: apague com `git rm` os `.mp4` e `.jpg` de partes publicadas há mais de 3 dias (o Instagram já guardou o vídeo). Nunca apague os `historia.json`.
11. **Resumo final** curto (3 linhas): o que foi publicado (história, parte, link se tiver), placar da votação se houver, e qualquer problema.

## Criar história

- **Original**, em português do Brasil, suspense/mistério/drama que prende, classificação livre a 14 anos: sem gore, sem violência gráfica, sem pessoas reais, marcas ou personagens de terceiros.
- Não repita gênero, cenário principal nem premissa das outras histórias ativas nem das últimas 4 concluídas (veja `historias/`). Personagens de histórias diferentes não podem ser iguais.
- Se a história precisar de um cenário que não existe, você pode adicionar uma função `bg_...` em `engine.py` seguindo o padrão das outras (desenho com Pillow, tamanho BW x BH) e registrá-la em `BACKGROUNDS`. Teste renderizando um quadro antes de usar. Leia `APRENDIZADOS.md` (e, se existir, o caderno na memória `/areas/aprendizados-instagram.md`) e aplique o que funciona.
- Narração em **1ª pessoa**, frases curtas, um mistério central claro desde a parte 1 e uma pergunta que só se resolve na parte 6.
- Escreva a `biblia`: premissa, regras do mundo, personagens (nome, papel, segredo), linha do tempo e **o final planejado** (para `votacao`, os dois finais possíveis e como as escolhas levam a eles).
- `continua`: escreva **as 6 partes de uma vez** (status `pronta`), com começo, meio e fim. Cada parte termina num gancho que a próxima resolve.
- `votacao`: escreva só a parte 1. Cada parte (1 a 5) termina num **dilema de verdade**: duas opções (`script.opcoes`: ["texto A", "texto B"], curtas) em que **as duas têm um preço** (salvar alguém x salvar a si mesmo, confiar x desconfiar, contar a verdade x proteger alguém). Nada de opção obviamente certa. As últimas 2 cenas montam a tensão da escolha (relógio, ameaça, alguém pedindo ajuda) e a última pergunta direto ao público: "E você, o que faria?". A parte seguinte começa mostrando a consequência da escolha da maioria.
- Slug em minúsculas com hífens. Crie `historias/<slug>/historia.json` (campos: slug, titulo, tipo, genero, status, biblia, personagens, partes) e registre em `estado.json > ativas` como `{"slug": ..., "tipo": ...}`.

## Coerência entre partes (obrigatório)

- **Personagens nunca mudam.** Depois que a Parte 1 sai, o bloco `personagens` daquela história fica congelado: mesma pele, roupa, cabelo, acessórios, nome, voz, pitch e speed em todas as partes. Na cena use sempre o `ref`; só mude expressão (`eyes`, `mouth`, `look`), posição e tamanho. Personagem novo no meio da história ganha uma entrada nova e também fica congelado.

Antes de escrever qualquer parte, leia `APRENDIZADOS.md` e aplique as recomendações (gancho, duração, ritmo, tipo de final, horário). Leia também a `biblia` e o texto de **todas** as partes anteriores. Mantenha nomes, aparências (use sempre os mesmos `ref` de personagens), lugares, horários e fatos. Na `votacao`, depois de escrever a parte, acrescente à `biblia` uma linha com o que ficou decidido ("Parte 3: escolheram B, Lia abriu a porta e ..."). A parte 6 tem que fechar o mistério de verdade.

## Responder antes de apurar

- Use `execute_action` com `reply_to_comment` (`comment_id`, `message`). Só comentários principais de outras pessoas que ainda não têm resposta da @mundoemhistorias (confira as respostas: linhas com `comment_parent_id` = esse comentário e `comment_username` = mundoemhistorias). Nunca responda o mesmo comentário duas vezes.
- Só votou ("A", "B"): confirme o voto, diga que a Parte N+1 sai em breve e convide a seguir. Sem pergunta.
- Opinou, brincou ou teorizou: reaja ao que a pessoa disse, de forma leve e provocativa; pode terminar com pergunta.
- Ignore spam e ofensas. No máximo 40 respostas por execução.

## Votação

- Leia os comentários da parte anterior com `get_data` (connector `instagram`, campos `media_id, comment_id, comment_text, comment_username, comment_parent_id`, `date_preset: last_7dT`) filtrando pelo `media_id` registrado.
- Conte só comentários principais (sem `comment_parent_id`), 1 voto por pessoa, ignorando a própria conta. Vale "A", "a", "letra A", "🅰️", "opção A" e frases que citam claramente uma opção.
- A mais votada vence. Empate ou zero votos: escolha a mais dramática e escreva na legenda "Deu empate, então eu decidi...".
- Guarde em `votos: {"A": x, "B": y}` e `escolha`. Comece a legenda da parte nova com o resultado ("Vocês escolheram B (7 a 3)!").

## Formato do roteiro (`script`)

```json
{
  "cover_text": "Título da parte, curto (até 5 palavras)",
  "opcoes": ["Só na votação"],
  "caption": "Legenda do post (veja abaixo)",
  "scenes": [
    {"bg": "rua_noite", "cam": "in", "hook": true, "cover": true,
     "chars": [{"ref": "LIA", "x": 0.5, "scale": 0.9, "eyes": "arregalado", "mouth": "o"}],
     "prop": {"type": "placa", "title": "PARADA 1"},
     "text": "Frase da narração com *palavra destaque* em amarelo."}
  ]
}
```

- **8 a 10 cenas** por parte, **190 a 240 palavras** no total (vídeo de ~60 a 90 s). Se uma parte já `pronta` tiver menos de 190 palavras, expanda antes de renderizar (mais detalhes, mais uma fala, tensão crescendo) sem mudar os fatos nem o gancho final. Cena 1 = gancho forte nos 3 primeiros segundos (`hook: true`, `cover: true`). Última cena = gancho/dilema (`hook: true`).
- `bg`: `rua_noite`, `rua_amanhecer` (`bg_params.sign`), `onibus_dentro`, `onibus_fora` (`bg_params.number`), `casa_noite` (+ `"window": true` para ver por uma janela), `escuro`, `corredor_predio`, `elevador` (`bg_params.floor`), `quarto_noite`, `floresta_noite`, `sala_aula`.
- `cam`: `in`, `out`, `zoom_forte`, `pan_l`, `pan_r`, `shake` (sustos).
- `prop.type`: `lista`/`carta` (title + lines; linha começando com `!` fica vermelha), `bilhete` (lines), `celular` (title + lines), `placa` (title). Use em cenas sem personagens.
- Personagens: defina em `personagens` com `skin`, `cloth`, `hair` (RGB), `hairstyle` (`curto`, `longo`, `coque`, `bone` + `cap`, `careca`, `capuz`), opcionais `age`, `uniform`, `shadow_face`. Na cena use `ref` + `x` (0–1), `scale` (0.3–1.15), `y` (padrão 0.86), `eyes` (`normal`, `arregalado`, `fechado`), `mouth` (`neutra`, `o`, `sorriso`, `triste`), `look` (-1/0/1), `flip`, `prop: "papel"`. No máximo 2 personagens por cena.
- `tint`: [r,g,b] opcional para clima (ex.: vermelho no clímax).

### Vozes e falas (cada personagem tem a sua voz)

- No `historia.json`, defina `narrador` (o `ref` de quem conta a história em 1ª pessoa) e, em cada personagem, `nome` (aparece na etiqueta da fala), `voz`, `pitch` e `speed`.
- Vozes disponíveis: `kokoro:pf_dora` (feminina), `kokoro:pm_alex` (masculina), `kokoro:pm_santa` (masculina grave), `piper:faber`, `piper:cadu`, `piper:jeff` (masculinas). Use `pitch` para diferenciar: criança 1.18–1.25, jovem 1.0–1.1, adulto 0.95–1.0, idoso 0.86–0.92; `speed` 0.88–1.08.
- **Duas personagens da mesma história nunca podem ter a mesma combinação de voz + pitch** (diferença mínima de 0.08 no pitch se usarem a mesma voz). Prefira vozes base diferentes para os homens.
- Na cena, use `text` para narração simples (voz do narrador) ou `linhas` para misturar narração e diálogo:
  `"linhas": [{"voz": "LIA", "texto": "Ele me olhou e disse:"}, {"voz": "IVO", "texto": "Você não devia estar aqui."}]`
  Toda parte deve ter **pelo menos 2 falas de personagens** além da narração. As falas aparecem com o nome do personagem acima da legenda.
- Escreva números e siglas por extenso quando forem falados ("parada quatro", "meia-noite").

## Capa

A capa sai sozinha com: **nome original da história** (o `titulo`, sempre igual em todas as partes) em amarelo, **"PARTE N"** em destaque (na 6: "PARTE 6 · FINAL") e o título da parte (`cover_text`). Nunca mude o `titulo` de uma história depois da Parte 1.

## Legenda do post

- Linha 1: gancho ou resultado da votação. Linha com "Parte N — título da parte".
- Uma pergunta que puxe comentário.
- Votação: as opções como `🅰️ ...` e `🅱️ ...` + "A mais votada decide a Parte N+1".
- Fecho: "A Parte N+1 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔" (na parte 6: "FIM. Começa da Parte 1 no perfil. Nova história em breve.").
- 4 a 6 hashtags no fim.

## Para não perder alcance

- Nada de spam: respostas e comentários sempre diferentes entre si, curtos e ligados ao que a pessoa disse. No máximo 40 respostas por execução.
- Nunca poste a mesma legenda, capa ou hashtags iguais em sequência; varie as hashtags dentro do tema.
- Primeiros 3 segundos com gancho forte e legenda grande; a última cena sempre termina em suspense ou dilema.

## Limites

- Sempre siga as regras do Instagram e da Meta: conteúdo original, sem personagens que se passem por pessoas reais, sem tentar esconder ou burlar a detecção de IA.
- **Não mude nada sobre rótulos de IA, bio, configurações do perfil ou forma de identificar o uso de IA sem o dono pedir.** Se achar que algo precisa mudar, só sugira no resumo.

- Use só este repositório. Não apague posts do Instagram. Fora das histórias com votação, as respostas aos comentários ficam com a outra tarefa.
- Nunca publique mais de 1 vídeo por execução.
