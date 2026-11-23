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

## Várias histórias ao mesmo tempo (uma parte por dia cada)

- Ficam ativas **5 histórias diferentes**, uma para cada horário do dia (9h, 12h, 15h, 18h, 21h): 2 `continua` (sem votação) e 3 `votacao` (A/B), em `estado.json > ativas`.
- **Cada história publica no máximo 1 parte por dia**, sempre no mesmo horário. `estado.json > vez` aponta a história da vez; depois de publicar, avance para a próxima (volta a 0 depois da última). Como são 5 histórias e 5 horários, cada uma cai sempre no mesmo horário.
- **Trava de segurança:** antes de publicar, confira no `historico` se a história da vez já publicou uma parte nas últimas 20 horas. Se já publicou, pule para a próxima da fila que não publicou nesse período.
- As 5 precisam ser **bem distintas entre si**: gêneros diferentes (suspense sobrenatural, mistério policial, drama familiar, ficção científica, sobrevivência, comédia de mistério, romance com segredo...), cenários e protagonistas diferentes (nome, aparência, cores de roupa, voz).
- Toda história tem **exatamente 6 partes**. Quando a parte 6 sair, marque a história como `concluida` e, no mesmo lugar da fila, crie uma nova do mesmo tipo e de gênero diferente das outras ativas. Ela estreia com a Parte 1 no dia seguinte, no mesmo horário.
- Se `ativas` tiver menos de 5, crie as que faltam (mantendo 2 contínuas e 3 de votação) e coloque no fim da fila.

## Passo a passo de cada execução

1. **Evite post duplicado.** Se o último item de `estado.json > historico` foi publicado há menos de 90 minutos, pare e diga "Já publicado neste horário".
2. **Escolha a história**: complete `ativas` até 5 se faltar (veja "Criar história") e pegue `ativas[vez]`.
3. **Defina a parte** = a primeira com status diferente de `publicada`. Nunca diga que uma parte "já está no perfil" se ela ainda não foi publicada. A frase padrão é "A Parte N+1 fica no perfil @mundoemhistorias (sai em até 24h)". Ela é verdadeira porque cada história publica uma parte por dia, no mesmo horário.
   - `continua`: o roteiro já está pronto (`status: pronta`).
   - `votacao`: se for a parte 2 a 6, **antes de escrever**: leia todos os comentários da parte anterior, **responda os que ainda não têm resposta** (veja "Responder antes de apurar") e **conte os votos** (veja "Votação"). Escreva o roteiro seguindo a opção vencedora.
3b. **Processo de preparação (obrigatório, nesta ordem):** rode `python3 tools/preparar.py <slug> <n>`. Ele faz: (1) **catálogo**: confere o estilo da história; numa história nova escolhe o estilo (alternando) e grava, e trava o visual de cada personagem; (2) **falas**: confere a voz de cada personagem e grava todas as falas da parte em `historias/<slug>/falas.json`; (3) **verificação**: confere catálogo, vozes travadas, quem fala, gancho visual na 1ª cena, zoom nas cenas de tensão, tamanho da parte e votos. Se aparecer ERRO, corrija o roteiro e rode de novo; não gere o vídeo com erro. Resolva também os avisos quando possível. (O `render_part.py` roda essa preparação de novo e se recusa a gerar com erro.)
4. **Renderize** com `python3 tools/render_part.py <slug> <n>`. Confira: duração entre 50 e 100 s; extraia 2 quadros com ffmpeg e olhe se os personagens, o cenário e a legenda estão certos (a legenda não pode ficar cortada). Se algo estiver errado, corrija o roteiro e renderize de novo.
5. **Suba** o vídeo, a capa e o JSON: `git add -A && git commit -m "<slug> parte <n>" && git -c push.negotiate=true push` (se o push for recusado por conflito, `git pull --rebase` e tente de novo). Configure antes `git config user.name "mundoemhistorias-bot"` e `git config user.email "bot@mundoemhistorias.local"`.
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
- Não repita gênero, cenário principal nem premissa das outras histórias ativas nem das últimas 5 concluídas (veja `historias/`). Personagens de histórias diferentes não podem ser iguais.
- Se a história precisar de um cenário que não existe, você pode adicionar uma função `bg_...` em `engine.py` seguindo o padrão das outras (desenho com Pillow, tamanho BW x BH) e registrá-la em `BACKGROUNDS`. Teste renderizando um quadro antes de usar. Leia `APRENDIZADOS.md` (e, se existir, o caderno na memória `/areas/aprendizados-instagram.md`) e aplique o que funciona.
- Narração em **1ª pessoa**, frases curtas, um mistério central claro desde a parte 1 e uma pergunta que só se resolve na parte 6.
- Escreva a `biblia`: premissa, regras do mundo, personagens (nome, papel, segredo), linha do tempo e **o final planejado** (para `votacao`, os dois finais possíveis e como as escolhas levam a eles).
- `continua`: escreva **as 6 partes de uma vez** (status `pronta`), com começo, meio e fim. Cada parte termina num gancho que a próxima resolve.
- `votacao`: escreva só a parte 1. Cada parte (1 a 5) termina num **dilema de verdade**: duas opções (`script.opcoes`: ["texto A", "texto B"], curtas) em que **as duas têm um preço** (salvar alguém x salvar a si mesmo, confiar x desconfiar, contar a verdade x proteger alguém). Nada de opção obviamente certa. As últimas 2 cenas montam a tensão da escolha (relógio, ameaça, alguém pedindo ajuda) e a última pergunta direto ao público: "E você, o que faria?". A parte seguinte começa mostrando a consequência da escolha da maioria.
- Slug em minúsculas com hífens. Crie `historias/<slug>/historia.json` (campos: slug, titulo, tipo, genero, status, biblia, personagens, partes) e registre em `estado.json > ativas` como `{"slug": ..., "tipo": ...}`.

## Elenco salvo de cada história

Cada história tem `historias/<slug>/elenco.json` (estilo/catálogo + desenho e voz de cada personagem), `falas.json` (vozes e tudo o que cada personagem falou em cada parte) e o resumo geral em `ELENCOS.md`. Leia o elenco antes de escrever qualquer parte. **Sempre:** toda vez que o `tools/preparar.py` roda (antes de cada vídeo), ele grava de novo o elenco de todas as histórias (`elenco.json`, `falas.json`, `ELENCOS.md`). Ao criar uma história nova ou um personagem novo, rode a preparação e faça commit desses arquivos junto com o vídeo.

## Estilos de personagens (obrigatório usar só estes desenhos)

Existem **só dois estilos**. Cada história usa **um estilo só**, gravado em `historia.json > estilo`, e **as histórias novas alternam** entre eles (`estado.json > ultimo_estilo`: a próxima história nova usa o outro estilo e atualiza esse campo).

- **`cartela`** (cartelas chibi do dono, corpo inteiro). Personagens: advogada, agricultor, bombeiro, cabeleireira, cozinheiro, cozinheiro_bigode, dentista, diretor, eletricista, empresario, enfermeira, enfermeiro_azul, engenheiro, entregador, farmaceutico, fazendeiro_chapeu, fotografo, garcom, garota_bone, garota_moletom_roxo, garoto_gorro_preto, homem_barba_gravata, homem_camisa_verde, homem_camiseta_amarela, homem_uniforme_azul, jornalista, juiz, manicure, mecanico, medico, medico_oculos, menina_laco_amarelo, menina_laco_vermelho, menina_vestido_rosa, menininha_rosa, menino_bone_azul, menino_camiseta_amarela, menino_fones, menino_mochila_verde, menino_moletom_verde, menino_ruivo_oculos, moca_loira, motorista, mulher_lenco_avental, mulher_terno, mulher_vestido_roxo, operario_colete, pedreiro, policial, policial_2, politico, porteiro, prefeito, professor, protagonista, seguranca, vendedora, veterinaria, vovo, vovozinha. Até 2 por cena, lado a lado (`x` 0.3 e 0.72, `scale` ~0.95).
- **`andar`** (catálogo próprio no estilo dos episódios de "O Andar que Não Existe": cabeça redonda, olhos grandes, contorno grosso; todos com o mesmo formato de corpo). Personagens: andar_voce (protagonista estudante), andar_medico (médico de jaleco), andar_porteiro (porteiro de farda e quepe), andar_estudante_ana (estudante, cabelo longo), andar_amigo_cacheado (amigo, cabelo cacheado), andar_rival (rival de boné), andar_professor (professor grisalho de óculos), andar_medica (médica de coque), andar_policial (policial), andar_faxineira (faxineira), andar_idoso (idoso de bigode), andar_idosa (idosa de óculos), andar_jornalista (jornalista), andar_empresario (empresário de terno), andar_mae (mãe), andar_pai (pai de barba), andar_menino (criança curiosa), andar_menina (criança alegre), andar_adolescente_fones (adolescente de fones), andar_adolescente_menina (adolescente determinada), andar_cientista (cientista de óculos), andar_esportista (esportista), andar_artista (artista de boina), andar_gamer (gamer), andar_leitora (leitora de óculos), andar_motorista (motorista de ônibus), andar_seguranca (segurança), andar_entregador (entregador), andar_vizinha (vizinha de cabelo cacheado), andar_vizinho (vizinho), andar_prefeito (prefeito de faixa), andar_zelador (zelador de macacão), andar_enfermeira (enfermeira), andar_cozinheiro (cozinheiro), andar_bombeiro (bombeiro), andar_garota_loira (garota loira). Enquadramento **padrão = `"medio"`** (plano médio igual aos episódios: dois personagens lado a lado, cabeça grande perto de 31% da altura, tronco inteiro e as pernas saindo por baixo; use `x` 0.21 e 0.67, sem `scale`). Também existem:  `"enquadramento": "busto"` (close como nos episódios: rosto grande, o tronco termina dentro da cena e as pernas saem pela borda de baixo; 1 por cena `x` 0.5 `scale` 0.9; 2 lado a lado `x` 0.28/0.72 `scale` 0.75 `y` 0.30). Prefira close nas cenas de diálogo e emoção; corpo inteiro só quando importa ver o corpo (andar, correr, lugar). Prefira close nas cenas de diálogo e emoção; use corpo inteiro só quando importa ver o corpo (andar, correr, lugar) ou `"enquadramento": "corpo"` (de pé; `x` 0.3/0.72, `scale` ~1.1). Nunca troque o `sprite` de um personagem para mudar o enquadramento.
- Em `personagens`, cada um tem `nome`, `sprite` (um nome das listas acima), `voz`, `pitch`, `speed`. Nunca dois personagens da mesma história com o mesmo `sprite`.
- **Expressões e boca:** o desenho nunca muda; por cena você escolhe `eyes` (`normal`, `arregalado`, `fechado`), `brows` (`preocupado`, `bravo`, `surpreso`, `neutro`) e `mouth` (`o`, `triste`). A boca **mexe sozinha** quando o personagem fala (`linhas` com a voz dele) e todos piscam e respiram. Varie as expressões conforme a emoção da cena.
- **TRAVA DOS CATÁLOGOS (regra do dono, sem exceção):** é proibido usar personagem fora dessas duas listas ou desenhar personagem novo. O `render_part.py` **recusa gerar o vídeo** se algum personagem não tiver `sprite` válido, se misturar os dois estilos ou se uma cena tiver personagem sem `ref`. Nunca tente contornar. Só o dono pode pedir personagens novos para o catálogo `andar` (são criados em `tools/catalogo_andar.py`).

## Coerência entre partes (obrigatório)

- **Séries antigas retomadas** (`elevador`, `cidade-sirene`): as partes 1 e 2 foram feitas antes deste sistema e não têm `script`; use o `resumo`, as `opcoes` e a `biblia` delas. A Parte 3 começa com uma recapitulação de 1 cena ("Nas partes anteriores...") e segue a escolha mais votada da Parte 2. A partir daí, tudo igual às outras histórias.

- **Personagens nunca mudam.** Depois que a Parte 1 sai, o bloco `personagens` daquela história fica congelado: mesma pele, roupa, cabelo, acessórios, nome, voz, pitch e speed em todas as partes. Na cena use sempre o `ref`; só mude expressão (`eyes`, `mouth`, `look`), posição e tamanho. Personagem novo no meio da história ganha uma entrada nova e também fica congelado. O `render_part.py` guarda uma cópia em `personagens_travados` e **recusa renderizar** se algum personagem existente mudar; nesse caso, desfaça a mudança (nunca edite `personagens_travados`).

Antes de escrever qualquer parte, leia `APRENDIZADOS.md` e aplique as recomendações (gancho, duração, ritmo, tipo de final, horário). Leia também a `biblia` e o texto de **todas** as partes anteriores. Mantenha nomes, aparências (use sempre os mesmos `ref` de personagens), lugares, horários e fatos. Na `votacao`, depois de escrever a parte, acrescente à `biblia` uma linha com o que ficou decidido ("Parte 3: escolheram B, Lia abriu a porta e ..."). A parte 6 tem que fechar o mistério de verdade.

## Responder antes de apurar

- **Registro único de respostas:** `comentarios_respondidos.json` guarda `{comment_id: data}` de todo comentário já respondido por qualquer tarefa. Antes de responder, pule os que já estão lá (os dados do Windsor podem demorar para mostrar nossas respostas). Logo depois de responder, acrescente o `comment_id` e faça commit + push.

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
- `cam`: `in`, `out`, `zoom_forte`, `pan_l`, `pan_r`, `shake` (sustos), `zoom_rosto` (aproxima rápido no rosto do personagem) e `zoom_tremido` (zoom no rosto tremendo). **Cenas de tensão** (`"tensao": true`, `hook`, susto, revelação, ameaça) devem ter zoom no rosto; se a cena tiver personagem e `hook`/`tensao` sem `cam`, o zoom no rosto entra sozinho. `"foco_em": "REF"` escolhe em qual personagem o zoom foca.
- **Gancho visual na abertura (obrigatório):** a cena 1 tem `"hook": true` e mostra a imagem mais forte da parte já no primeiro segundo (personagem assustado em close, ameaça, objeto revelador), com a primeira frase sendo o gancho. O vídeo entra sozinho com flash, zoom forte e tremida nos primeiros 0,6 s.
- `prop.type`: `lista`/`carta` (title + lines; linha começando com `!` fica vermelha), `bilhete` (lines), `celular` (title + lines), `placa` (title). Use em cenas sem personagens.
- Personagens: use os desenhos das cartelas (veja "Estilos de personagens"). Na cena use `ref` + `x`, `scale`, `eyes`, `brows`, `mouth`, `flip`. No máximo 2 personagens por cena. (Os campos antigos `skin`, `cloth`, `hairstyle`... só valem para as histórias antigas que já usavam desenho próprio.)
- `tint`: [r,g,b] opcional para clima (ex.: vermelho no clímax).
- **Tela de votos (histórias com votação, automática no fim do vídeo):** fundo vinho, "COMENTA A OU B", quadro A (azul) e quadro B (amarelo), cada um com o rosto de um personagem e a opção, a chamada embaixo e "Segue @mundoemhistorias pra ver a Parte N". Defina no `script`: `"opcoes_rostos": [{"ref": "MEDICO", "brows": "bravo", "mouth": "aberta"}, {"ref": "PORTEIRO", "eyes": "arregalado", "mouth": "o"}]` (o personagem ligado a cada opção, com expressão) e `"chamada": "Marca quem sairia desse elevador sem pensar"` (frase curta para marcar amigos). Sem isso, usa os personagens da última cena.
- `"filtro": "tv"`: cena vista por câmera de segurança / TV velha (cor lavada, linhas, chiado, "CAM 03", REC piscando e relógio). Use em cenas de câmera, gravação, lembrança ou quando alguém observa de longe (ex.: o porteiro na câmera do prédio). No máximo 1 ou 2 cenas por parte.

### Vozes e falas (cada personagem tem a sua voz)

- No `historia.json`, defina `narrador` (o `ref` de quem conta a história em 1ª pessoa) e, em cada personagem, `nome` (aparece na etiqueta da fala), `voz`, `pitch` e `speed`.
- Vozes disponíveis (grátis, tratadas para soar naturais): `kokoro:pf_dora` (feminina), `kokoro:pm_alex` (masculina), `kokoro:pm_santa` (masculina grave), `piper:faber`, `piper:cadu`, `piper:jeff` (outros timbres masculinos, misturas) e misturas próprias `kokoro:mix:pm_alex*0.6+pm_santa*0.4`. O `pitch` fica entre 0.93 e 1.08 (mais que isso soa robótico): criança/jovem 1.04–1.08, adulto 0.97–1.02, idoso 0.93–0.96; `speed` 0.88–1.08 (idoso mais lento, jovem mais rápido).
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


## Textos na tela no estilo `andar`

Nas histórias de estilo `andar`, o vídeo usa o visual dos episódios originais: @ no canto de cima, faixa branca "PARTE N · VOCÊS ESCOLHERAM B" (ou "PARTE N · <título da parte>"), faixa amarela "NO FINAL VOCÊ DECIDE: A ou B" nas histórias com votação, legenda em letra normal branca com contorno azul-marinho e o nome de quem fala num selo azul-claro. Isso é automático; para trocar o texto da faixa branca use `script.faixa`.

## Trava do elenco (regra do dono, 23/11)
- `elencos_travados.json` guarda, para cada história, os personagens com físico (`sprite`, `escuro`), voz (`voz`, `pitch`, `speed`) e nome. **Nunca altere nem apague nada desse arquivo.** Só é permitido acrescentar história nova ou personagem novo (o `tools/render_part.py` faz isso sozinho na primeira renderização).
- Em `historia.json`, `personagens` e `personagens_travados` têm que ficar idênticos ao arquivo. Nas cenas, nunca use `sprite`, `cloth`, `skin`, `hair`, `hairstyle`, `escuro`, `voz`, `pitch`, `speed` ou `nome` dentro de um personagem: físico e voz vêm só de `personagens`.
- `render_part.py` e `cartaz.py` param com erro se algo disso mudar. Se der esse erro, restaure o personagem; nunca edite o arquivo da trava para "passar".

## Cenários (30 personalizáveis, `cenarios.py`)
Além dos fundos antigos (rua_noite, rua_amanhecer, onibus_dentro, onibus_fora, casa_noite, escuro, corredor_predio, elevador, quarto_noite, floresta_noite, sala_aula), use estes em `bg`. Prefira um cenário de verdade a `escuro`: varie os lugares para a história ficar mais rica, mas mantenha o mesmo lugar quando a cena continua no mesmo ambiente.
Parâmetros em `bg_params` (todos opcionais, valem para todos): `hora` (dia, tarde, noite, amanhecer), `luz` (acesa, apagada), `cor` [r,g,b], `texto` (placa/quadro/letreiro), `chuva`, `neblina`, `alerta` (luz vermelha de sirene), `seed`.

- `cozinha`: cozinha com azulejos, armários, janela e fogão
- `sala_estar`: sala com sofá, TV, cortinas, janela e quadro (texto = escrito no quadro)
- `banheiro`: banheiro com espelho grande e pia (texto = escrito no espelho (vermelho))
- `porao`: porão de tijolos com escada, caixas e lâmpada pendurada (texto = escrito na caixa)
- `sotao`: sótão de madeira com janela redonda, baú e móvel coberto
- `hospital_quarto`: quarto de hospital com cama, monitor cardíaco e soro
- `delegacia`: delegacia com quadro de suspeitos ligados por fio vermelho e mesa (texto = título do quadro)
- `escritorio`: escritório com janelão para a cidade e computadores (texto = nome da empresa)
- `biblioteca`: biblioteca com estantes de livros coloridos
- `mercadinho`: mercadinho com prateleiras e letreiro (texto = letreiro (padrão MERCADINHO))
- `lanchonete`: lanchonete anos 50 com letreiro neon, balcão e chão xadrez (texto = neon (padrão LANCHES 24H); cor = cor do neon)
- `laboratorio`: laboratório com telão, bancada e frascos brilhando (texto = escrito no telão; cor = cor da tela)
- `nave_espacial`: nave espacial com janela para o espaço, planeta e painel (texto = aviso no painel; cor = cor do planeta)
- `recepcao_hotel`: recepção de hotel antigo com quadro de chaves e balcão (texto = placa (padrão RECEPÇÃO))
- `gabinete`: gabinete (prefeito, diretor, chefe) com bandeira, retrato e mesa grande (texto = plaquinha na mesa; cor = cor da bandeira)
- `ginasio`: ginásio com arquibancada, placar e quadra (texto = placar (padrão CASA 0 x 0 VISITA))
- `teatro`: palco de teatro com cortina e holofote (texto = título no alto; cor = cor da cortina)
- `estacao_metro`: plataforma de metrô com placa e trilhos (texto = nome da estação; cor = faixa da parede)
- `caverna`: caverna com estalactites, túnel escuro e luz de tocha (luz_cor = cor da tocha)
- `ponte`: ponte suspensa de madeira entre penhascos, rio lá embaixo (quebrada = true (ponte caída); texto = placa)
- `rio`: margem de rio com árvores e pedras (texto = placa)
- `praia`: praia com mar, coqueiro e guarda-sol (texto = escrito na areia; cor = guarda-sol)
- `praca`: praça com coreto, bancos, árvores e poste (texto = placa (padrão PRAÇA))
- `parque_diversoes`: parque de diversões com roda-gigante e barraca listrada (texto = nome na barraca; cor = listras)
- `estrada`: estrada deserta até o horizonte com placa (texto = placa (padrão KM 47))
- `posto_gasolina`: posto de gasolina com bombas e painel de preços (texto = nome do posto; cor = cobertura)
- `cemiterio`: cemitério com lápides, grade e árvore seca (texto = escrito no portão)
- `beco`: beco entre prédios com escada de incêndio, caçamba e pichação (texto = pichação (padrão NÃO OLHE); cor = paredes)
- `telhado`: telhado de prédio com caixa d'água e cidade ao fundo (texto = escrito na caixa d'água)
- `fazenda`: fazenda com celeiro, cerca e campo (texto = nome no celeiro; cor = celeiro)

## Cenário, zoom e efeitos (regra do dono, 23/11)
A preparação (`tools/preparar.py`) recusa a parte se: mais de 2 cenas com `escuro`; menos de 3 cenários diferentes; menos de 3 cenas com zoom/tremida (`zoom_rosto`, `zoom_tremido`, `zoom_forte`, `shake`, ou `hook`/`tensao` sem `cam`); menos de 2 cenas com efeito (`tint`, `"filtro": "tv"`, ou `bg_params` com `chuva`, `neblina`, `alerta` ou `"luz": "apagada"`). Personalize os cenários com `bg_params` (hora, texto, cor) para combinarem com a história. Ao corrigir, nunca mude o cenário da cena de capa (`cover`) se o cartaz EM BREVE já saiu.
