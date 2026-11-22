# Manual do agente: @mundoemhistorias

Este repositório produz e publica sozinho histórias em partes no Instagram **@mundoemhistorias**.
A cada horário agendado (9h, 12h, 15h, 18h e 21h, America/Campo_Grande) você publica **um** vídeo novo.
O dono da conta autorizou a publicação sem aprovação prévia.

## Arquivos

- `engine.py`: motor de vídeo (1080x1920, legenda grande, trilha sintetizada, capa). Não altere sem necessidade.
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
3. **Defina a parte** = a primeira com status diferente de `publicada`.
   - `continua`: o roteiro já está pronto (`status: pronta`).
   - `votacao`: se for a parte 2 a 6, apure os votos da parte anterior (veja "Votação") e escreva o roteiro desta parte seguindo a opção vencedora.
4. **Renderize** com `python3 tools/render_part.py <slug> <n>`. Confira: duração entre 25 e 75 s; extraia 2 quadros com ffmpeg e olhe se os personagens, o cenário e a legenda estão certos (a legenda não pode ficar cortada). Se algo estiver errado, corrija o roteiro e renderize de novo.
5. **Suba** o vídeo, a capa e o JSON: `git add -A && git commit -m "<slug> parte <n>" && git push`. Configure antes `git config user.name "mundoemhistorias-bot"` e `git config user.email "bot@mundoemhistorias.local"`.
6. **Confira o link público** (deve responder 200):
   `https://raw.githubusercontent.com/ricardosaback3b-pixel/claude/main/videos/<slug>/parte<n>.mp4`
   (o mesmo vale para `capa<n>.jpg`). Se der 404, espere 20 s e tente de novo, no máximo 5 vezes.
7. **Publique** com o Windsor.ai (carregue as ferramentas `mcp__Windsor_ai__*` via ToolSearch): `execute_action`, connector `instagram`, account `17841437436804359`, action `create_video_post`, params `{video_url, cover_url, caption, share_to_feed: true}`. Se falhar, tente mais uma vez; se falhar de novo, **não** marque como publicada e avise no resumo.
8. **Registre**: na parte, ponha `status: publicada`, `media_id` e `publicada_em` (ISO, UTC). Em `estado.json`, adicione ao `historico` `{quando, slug, parte, media_id}` e avance `vez` (volta a 0 depois do último). Se foi a parte 6, ponha a história como `concluida` e troque-a em `ativas` por uma nova do mesmo tipo (crie o `historia.json` com a bíblia e, se for `continua`, as 6 partes). Faça commit e push.
9. **Limpeza**: apague com `git rm` os `.mp4` e `.jpg` de partes publicadas há mais de 3 dias (o Instagram já guardou o vídeo). Nunca apague os `historia.json`.
10. **Resumo final** curto (3 linhas): o que foi publicado (história, parte, link se tiver), placar da votação se houver, e qualquer problema.

## Criar história

- **Original**, em português do Brasil, suspense/mistério/drama que prende, classificação livre a 14 anos: sem gore, sem violência gráfica, sem pessoas reais, marcas ou personagens de terceiros.
- Não repita gênero, cenário principal nem premissa das outras histórias ativas nem das últimas 4 concluídas (veja `historias/`). Personagens de histórias diferentes não podem ser iguais.
- Se a história precisar de um cenário que não existe, você pode adicionar uma função `bg_...` em `engine.py` seguindo o padrão das outras (desenho com Pillow, tamanho BW x BH) e registrá-la em `BACKGROUNDS`. Teste renderizando um quadro antes de usar. Se existir o caderno de aprendizados na memória (`/areas/aprendizados-instagram.md`), use o que ele diz que funciona.
- Narração em **1ª pessoa**, frases curtas, um mistério central claro desde a parte 1 e uma pergunta que só se resolve na parte 6.
- Escreva a `biblia`: premissa, regras do mundo, personagens (nome, papel, segredo), linha do tempo e **o final planejado** (para `votacao`, os dois finais possíveis e como as escolhas levam a eles).
- `continua`: escreva **as 6 partes de uma vez** (status `pronta`), com começo, meio e fim. Cada parte termina num gancho que a próxima resolve.
- `votacao`: escreva só a parte 1. Cada parte termina num dilema com duas opções (`script.opcoes`: ["texto A", "texto B"], curtas). As duas opções têm que fazer sentido na história.
- Slug em minúsculas com hífens. Crie `historias/<slug>/historia.json` (campos: slug, titulo, tipo, genero, status, biblia, personagens, partes) e registre em `estado.json > ativas` como `{"slug": ..., "tipo": ...}`.

## Coerência entre partes (obrigatório)

Antes de escrever qualquer parte, leia a `biblia` e o texto de **todas** as partes anteriores. Mantenha nomes, aparências (use sempre os mesmos `ref` de personagens), lugares, horários e fatos. Na `votacao`, depois de escrever a parte, acrescente à `biblia` uma linha com o que ficou decidido ("Parte 3: escolheram B, Lia abriu a porta e ..."). A parte 6 tem que fechar o mistério de verdade.

## Votação

- Leia os comentários da parte anterior com `get_data` (connector `instagram`, campos `media_id, comment_id, comment_text, comment_username, comment_parent_id`, `date_preset: last_7dT`) filtrando pelo `media_id` registrado.
- Conte só comentários principais (sem `comment_parent_id`), 1 voto por pessoa, ignorando a própria conta. Vale "A", "a", "letra A", "🅰️", "opção A" e frases que citam claramente uma opção.
- A mais votada vence. Empate ou zero votos: escolha a mais dramática e escreva na legenda "Deu empate, então eu decidi...".
- Guarde em `votos: {"A": x, "B": y}` e `escolha`. Comece a legenda da parte nova com o resultado ("Vocês escolheram B (7 a 3)!").

## Formato do roteiro (`script`)

```json
{
  "cover_text": "Frase curta e chocante (até 5 palavras)",
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

- **5 a 7 cenas** por parte, **110 a 150 palavras** no total. Cena 1 = gancho forte nos 3 primeiros segundos (`hook: true`, `cover: true`). Última cena = gancho/dilema (`hook: true`).
- `bg`: `rua_noite`, `rua_amanhecer` (`bg_params.sign`), `onibus_dentro`, `onibus_fora` (`bg_params.number`), `casa_noite` (+ `"window": true` para ver por uma janela), `escuro`, `corredor_predio`, `elevador` (`bg_params.floor`), `quarto_noite`, `floresta_noite`, `sala_aula`.
- `cam`: `in`, `out`, `zoom_forte`, `pan_l`, `pan_r`, `shake` (sustos).
- `prop.type`: `lista`/`carta` (title + lines; linha começando com `!` fica vermelha), `bilhete` (lines), `celular` (title + lines), `placa` (title). Use em cenas sem personagens.
- Personagens: defina em `personagens` com `skin`, `cloth`, `hair` (RGB), `hairstyle` (`curto`, `longo`, `coque`, `bone` + `cap`, `careca`, `capuz`), opcionais `age`, `uniform`, `shadow_face`. Na cena use `ref` + `x` (0–1), `scale` (0.3–1.15), `y` (padrão 0.86), `eyes` (`normal`, `arregalado`, `fechado`), `mouth` (`neutra`, `o`, `sorriso`, `triste`), `look` (-1/0/1), `flip`, `prop: "papel"`. No máximo 2 personagens por cena.
- `tint`: [r,g,b] opcional para clima (ex.: vermelho no clímax).

## Legenda do post

- Linha 1: gancho ou resultado da votação. Linha com "Parte N — título da parte".
- Uma pergunta que puxe comentário.
- Votação: as opções como `🅰️ ...` e `🅱️ ...` + "A mais votada decide a Parte N+1".
- Fecho: "Parte N+1 em breve. Segue @mundoemhistorias 🔔" (na parte 6: "FIM. Começa da Parte 1 no perfil. Nova história em breve.").
- 4 a 6 hashtags no fim.

## Limites

- Use só este repositório. Não apague posts do Instagram e não responda comentários (outra tarefa faz isso).
- Nunca publique mais de 1 vídeo por execução.
