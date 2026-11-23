# PLANO — 23/11/2026 (segunda)

Estação 1 (Planejamento). Horários no fuso de **Campo Grande** (o dono pediu manter 23/11 no fuso antigo; a partir de 24/11 tudo passa para o horário de Brasília). Fichas em `fabrica/2026-11-23/HHMM.json` (status `planejado`).

## Cronograma do dia

| Horário | História | Parte | Tipo | Estilo | Versão padrão | Capa |
|---|---|---|---|---|---|---|
| 08:52 | A Ponte Caída (`a-ponte-caida`) | 1 | votação A/B | cartela | unica | A Ponte Caída · Parte 1 — A corda foi cortada |
| 11:52 | O Último Ônibus (`ultimo-onibus`) | 2 | contínua | cartela | unica | O Último Ônibus · Parte 2 — A parada do que você escondeu |
| 14:52 | O Andar que Não Existe (`elevador`) | 3 | votação A/B | andar | B | O Andar que Não Existe · Parte 3 — Alguém no meu lugar |
| 17:52 | Nessa Cidade, a Sirene Toca às 18h (`cidade-sirene`) | 4 | votação A/B | cartela | A | Nessa Cidade, a Sirene Toca às 18h · Parte 4 — O dono do caderno |
| 20:52 | O Sombra da Sala 12 (`o-sombra-da-sala-12`) | 2 | contínua | andar | unica | O Sombra da Sala 12 · Parte 2 — O giz azul |

**Por que esta ordem:** segue `estado.json > vez` (= 4, A Ponte Caída) e a fila `ativas` girando; com 5 histórias e 5 horários, cada uma fica fixa no seu horário daqui pra frente (Ponte 8h52, Ônibus 11h52, Elevador 14h52, Sirene 17h52, Sombra 20h52). Trava de 20 h conferida: nenhuma delas publicou nas 20 h anteriores ao seu horário de hoje (a mais justa é a Sirene: última às 21:57 UTC de 22/11, hoje 21:52 UTC = 23h55 depois).

Nenhuma história terminou e há 5 ativas (2 contínuas: Último Ônibus, Sombra; 3 votação: Elevador, Sirene, Ponte), então **nenhuma história nova hoje**. Próxima história nova deve usar o estilo `andar` (`ultimo_estilo` = cartela).

## Regras aplicadas (APRENDIZADOS + dono)

- 1ª frase com algo pessoal em jogo; nada de "A ou B?" na abertura nem na 1ª linha da legenda.
- Partes 2+: retomada do gancho em ≤3 s na cena 1.
- Gatilho de compartilhar no fim e na legenda (shares seguem 0).
- Nunca dizer que ninguém votou: `{RESULTADO_SE_HOUVER_VOTOS}` na legenda vira "Vocês escolheram X (a a b)! " ou some.
- Nunca dizer que a próxima parte já está no perfil; frase padrão "A Parte N+1 fica no perfil @mundoemhistorias (sai em até 24h)".
- 9 cenas e 200–232 palavras por versão (≈55–65 s).


---

## 08h52 — A Ponte Caída · Parte 1

_Estreia. Roteiro já pronto no historia.json (9 cenas, 232 palavras); mantido igual, só legenda/chamada ganharam gatilho de compartilhar e a pergunta 'quem cortou' vem antes do voto._

### Versão única

- **Resumo:** A ponte pênsil cai com a corda cortada, o Júnior some no vale e o Rafa precisa escolher entre buscá-lo no escuro ou proteger as duas que ficaram.
- **Tamanho:** 9 cenas, 223 palavras · **zoom/tensão:** cenas 1, 7, 9
- **Final:** Apito de emergência três vezes e silêncio; chuva; Rafa entre buscar o Júnior e deixar as duas com quem talvez cortou a corda. 'E você, o que faria?' + tela de votos 'Segue @mundoemhistorias pra ver a Parte 2'.
- **Gatilho de compartilhar:** Chamada da tela de votos e legenda: 'Marca quem você levaria nessa trilha'.
- **Próxima votação:** 🅰️ Buscar o Júnior no escuro × 🅱️ Ficar e montar abrigo · chamada: "Marca quem largaria todo mundo na trilha"

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | floresta_noite (zoom_forte) | RAFA | A ponte caiu *dez segundos* antes da gente atravessar. E quando eu puxei a corda do rio... ela estava *cortada*. |
| 2 | floresta_noite (pan_r) | RAFA | Eu sou guia na Serra do Vento há oito anos. Hoje eu levava três pessoas numa trilha de um dia. Fácil. Volta antes do escuro. |
| 3 | floresta_noite (in) | CELIA, MARINA | A Dona Célia, aposentada, que parava pra cheirar a terra. A Marina, que disse ser médica. E o Júnior, dezessete anos, que só queria sinal de celular. |
| 4 | escuro (zoom_forte) [lista: SITUAÇÃO] | — | Do outro lado do rio, o carro e o caminho de volta. Do nosso lado, mata fechada. E um trovão que já roncava atrás do morro. |
| 5 | floresta_noite (in) | RAFA, CELIA | **Rafa:** Alguém cortou essa corda. Alguém aqui. / **Dona Célia:** Calma, rapaz. Às vezes, uma ponte que cai é *sorte*. |
| 6 | floresta_noite (pan_l) | MARINA | **Rafa:** Eu ia perguntar o que ela quis dizer. Mas a Marina gritou. / **Marina:** Cadê o Júnior? Ele subiu a encosta procurando sinal faz vinte minutos! |
| 7 🔥 | escuro (shake) [placa: FIIIIU...] | — | Lá longe, no fundo do vale, um apito. O apito de emergência que eu dei pra cada um de manhã. Três vezes. E depois, *silêncio*. |
| 8 | floresta_noite (in) | MARINA, RAFA | **Marina:** Eu torci o tornozelo, Rafa. Eu não consigo andar rápido. / **Rafa:** Se eu for atrás dele, deixo as duas sozinhas. Com quem cortou a corda, talvez. |
| 9 🔥 | floresta_noite (shake) | RAFA | A chuva começou. Se eu for buscar o Júnior no escuro, a Marina e a Célia ficam sem abrigo. Se eu ficar, o Júnior passa a noite *sozinho* lá embaixo. E você, o que faria? |

**Legenda:**

```
A ponte caiu dez segundos antes da gente atravessar… e a corda estava cortada. 🌧️🌉

A Ponte Caída · Parte 1 — A corda foi cortada

Quem você acha que cortou a corda? Chuta aqui 👇

E no fim, vota: 🅰️ Buscar o Júnior no escuro ou 🅱️ Ficar e montar abrigo. A mais votada decide a Parte 2.

Marca quem você levaria nessa trilha (e quem largaria todo mundo) 👀

A Parte 2 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#sobrevivencia #suspense #historiasempartes #trilha #serra
```


---

## 11h52 — O Último Ônibus · Parte 2

_O roteiro 'pronta' do historia.json tinha só 6 cenas/81 palavras: este pré-roteiro expande para 9 cenas sem mudar fatos nem o gancho (lista com o nome dela e a data de hoje). Substituir o script da parte 2 por este. Seu Ivo: não citar cor do boné (P1 falou 'verde', o desenho é quepe azul)._

### Versão única

- **Resumo:** Na Parada 1, Lia vê a si mesma criança escondendo um envelope sob o piso, e descobre que o último nome da lista de passageiros é o dela, com a data de hoje.
- **Retomada do gancho:** Cena 1: 'Eu entrei no ônibus sem número... e o Seu Ivo me contou a regra' (~3s).
- **Tamanho:** 9 cenas, 206 palavras · **zoom/tensão:** cenas 1, 3, 6, 8, 9
- **Final:** Parada Dois acendendo; Lia precisa descer antes da última parada e não sabe se a porta abre (a Parte 3 abre com ela correndo pra porta).
- **Gatilho de compartilhar:** Fala final + legenda: 'Manda pra quem guarda um segredo desde criança'.

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | onibus_dentro (zoom_rosto) | IVO, LIA | **Lia:** Eu entrei no ônibus sem número. E o Seu Ivo, que morreu ano passado, me contou a regra: / **Seu Ivo:** Ele para onde você *escondeu alguma coisa*. |
| 2 | escuro (in) [placa: PARADA 1] | — | Um letreiro vermelho acendeu no teto: *Parada Um*. O ônibus freou sem fazer barulho. Ninguém desceu. Ninguém subiu. |
| 3 🔥 | casa_noite (zoom_forte) | LIA | Lá fora não era a Rua Nove. Era a *minha casa* de infância. A mesma cerca torta. E na janela, uma menina de oito anos. *Eu.* |
| 4 | casa_noite (in) | LIA | Eu vi a mim mesma ajoelhada na sala, tirando uma tábua solta do chão. E escondendo um *envelope* branco lá embaixo. Eu tinha esquecido disso. Ou fingia que tinha. |
| 5 | onibus_dentro (in) | LIA, IVO | **Lia:** O que tem nesse envelope, Seu Ivo? / **Seu Ivo:** Você sabe, minha filha. Só não quer *lembrar*. |
| 6 🔥 | onibus_dentro (zoom_rosto) | MOTORISTA, LIA | **Lia:** Lá na frente, o motorista falou sem virar o rosto. / **Motorista:** Quem não desce... *continua*. |
| 7 | onibus_dentro (in) | IVO, LIA | **Seu Ivo:** A última parada é onde *ninguém desce*. Guarda isso. / **Lia:** E ele me entregou um papel dobrado, frio feito gelo. |
| 8 🔥 | escuro (shake) [lista: PASSAGEIROS] | — | Era a lista de passageiros. Os nomes de cima estavam riscados. E o último nome era o *meu*. Com a data de *hoje*. |
| 9 🔥 | onibus_dentro (zoom_tremido) | LIA | No teto, *Parada Dois* já estava acendendo. Eu precisava descer antes da última. Só não sabia se a porta ainda abria. Manda pra quem guarda um segredo desde criança. A Parte Três sai amanhã, segue o perfil. |

**Legenda:**

```
O último nome da lista de passageiros era o meu. Com a data de hoje. 🚌

O Último Ônibus · Parte 2 — A parada do que você escondeu

O que você acha que tem no envelope? Chuta aqui 👇

Manda pra alguém que guarda um segredo desde criança 👀

A Parte 3 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#historiasempartes #suspense #misterio #onibus #segredos
```


---

## 14h52 — O Andar que Não Existe · Parte 3

_Série antiga: Parte 3 traz 1 cena de recapitulação ('Nas partes anteriores'). Votos registrados na bíblia até agora: B 2 x 0 A (nathalia_5003, kevin_12_zn) -> padrão B; a Produção/Publicação reconta. {RESULTADO_SE_HOUVER_VOTOS} = 'Vocês escolheram X (a a b)! ' ou vazio se 0 votos (nunca dizer que ninguém votou). Fato novo da Parte 3 (registrar na bíblia ao produzir): a mãe do Você saiu do prédio há 10 anos e nunca voltou; o porteiro diz que ela espera na portaria (liga com a ideia do -1 guardar quem 'saiu' do prédio)._

### Versão A — se ganhar A

- **Resumo:** Escolheram empurrar o médico: Você sai no 20º, o espelho avisa que o -1 é a portaria e o porteiro diz que a mãe dele, que saiu do prédio há dez anos, espera na portaria.
- **Retomada do gancho:** Cena 1: 'Eu empurrei o médico de volta pro espelho' (~3s).
- **Tamanho:** 9 cenas, 209 palavras · **zoom/tensão:** cenas 1, 4, 6, 8, 9
- **Final:** A mãe que sumiu há dez anos 'espera' na portaria; o elevador volta com o médico; um minuto pra escolher. Tela de votos 'Segue @mundoemhistorias pra ver a Parte 4'.
- **Gatilho de compartilhar:** Chamada da tela de votos + legenda: 'Marca quem desceria essa escada sozinho'.
- **Próxima votação:** 🅰️ Voltar e tirar o médico × 🅱️ Descer e encarar o porteiro · chamada: "Marca quem desceria essa escada sozinho"

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | elevador (zoom_rosto) | PROTAGONISTA | Eu empurrei o médico de volta pro espelho. E ele *me olhou* enquanto afundava. |
| 2 | escuro (in) [placa: -1] | — | Nas partes anteriores: o elevador parou no *menos um*, o andar que não existe. Eu fiquei, como o porteiro mandou. E o médico do sétimo tentou me levar com ele. |
| 3 | elevador (pan_r) | PROTAGONISTA | A porta abriu no vigésimo andar e eu saí correndo. Atrás de mim, o vidro do espelho ainda *tremia*. |
| 4 🔥 | escuro (zoom_forte) [bilhete: ] | — | No embaçado do espelho, alguém escreveu com o dedo, de dentro pra fora: *ele mentiu*. E embaixo: o menos um é a *portaria*. |
| 5 📺 | corredor_predio (in) | PORTEIRO | **Porteiro:** Muito bem. Fez a coisa certa. Agora desce aqui na portaria. / **Você:** Por que eu? O que tem aí embaixo? |
| 6 🔥 📺 | elevador (zoom_rosto) | MEDICO | **Você:** Na câmera três, o elevador descia. E o médico batia no espelho. / **Médico:** Não desce! Ele precisa de *alguém* no lugar dele! |
| 7 📺 | corredor_predio (in) | PORTEIRO | **Porteiro:** Não escuta ele. Desce pela escada. A sua *mãe* está te esperando aqui. |
| 8 🔥 | corredor_predio (zoom_rosto) | PROTAGONISTA | E aí eu gelei. A minha mãe *saiu desse prédio* faz dez anos. E nunca mais voltou. |
| 9 🔥 | corredor_predio (zoom_tremido) | PROTAGONISTA | No visor, o elevador já estava *subindo* de novo, com o médico dentro. Eu tinha um minuto. A: voltar pro elevador e tirar o médico do espelho, mesmo que ele me leve pro menos um. B: descer a escada e encarar o porteiro, deixando o médico pra trás. E você, o que faria? |

**Legenda:**

```
{RESULTADO_SE_HOUVER_VOTOS}Eu empurrei o médico de volta pro espelho... e o espelho escreveu: ele mentiu. 🛗

O Andar que Não Existe · Parte 3 — Alguém no meu lugar

Quem está esperando lá na portaria? Teoria aqui 👇

🅰️ Voltar e tirar o médico do espelho
🅱️ Descer e encarar o porteiro
A mais votada decide a Parte 4.

Marca quem desceria essa escada sozinho 👀

A Parte 4 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#terror #elevador #historiasempartes #vocedecide #suspense #misterio
```

### Versão B (PADRÃO se não houver votos) — se ganhar B

- **Resumo:** Escolheram correr pra porta: Você sai no 20º, o elevador desce sozinho com o médico, e o porteiro diz que alguém precisa entrar no lugar dele, dizendo que a mãe dele, que saiu do prédio há dez anos, espera na portaria.
- **Retomada do gancho:** Cena 1: 'Eu corri pra porta primeiro e deixei o médico preso no espelho' (~3s).
- **Tamanho:** 9 cenas, 204 palavras · **zoom/tensão:** cenas 1, 6, 8, 9
- **Final:** A mãe que sumiu há dez anos 'espera' na portaria; o elevador volta com o médico; um minuto pra escolher. Tela de votos 'Segue @mundoemhistorias pra ver a Parte 4'.
- **Gatilho de compartilhar:** Chamada da tela de votos + legenda: 'Marca quem desceria essa escada sozinho'.
- **Próxima votação:** 🅰️ Voltar e tirar o médico × 🅱️ Descer e encarar o porteiro · chamada: "Marca quem desceria essa escada sozinho"

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | elevador (zoom_rosto) | PROTAGONISTA | Eu corri pra porta primeiro. E deixei o médico *preso no espelho*. |
| 2 | escuro (in) [placa: -1] | — | Nas partes anteriores: o elevador parou no *menos um*, o andar que não existe. Eu fiquei, como o porteiro mandou. E o médico do sétimo acabou preso *dentro do espelho*. |
| 3 | corredor_predio (pan_r) | PROTAGONISTA | Eu caí de joelhos no corredor do vigésimo andar. Atrás de mim, a porta fechou. E o elevador começou a *descer sozinho*. |
| 4 | escuro (zoom_forte) [placa: 20... 10... 1... -1] | — | No visor do corredor, os números foram caindo. Dez. Cinco. Um. E parou no *menos um*. |
| 5 📺 | corredor_predio (in) | PORTEIRO | **Porteiro:** Muito bem. Você saiu. Agora *alguém* precisa entrar no seu lugar. / **Você:** No meu lugar? Como assim, no meu lugar? |
| 6 🔥 📺 | elevador (zoom_rosto) | MEDICO | **Você:** Na câmera três, o médico batia no espelho, me chamando. / **Médico:** Ele mente pra você desde o *primeiro andar*! |
| 7 📺 | corredor_predio (in) | PORTEIRO | **Porteiro:** Não escuta ele. Desce pela escada e vem pra portaria. A sua *mãe* está te esperando aqui. |
| 8 🔥 | corredor_predio (zoom_rosto) | PROTAGONISTA | E aí eu gelei. A minha mãe *saiu desse prédio* faz dez anos. E nunca mais voltou. |
| 9 🔥 | corredor_predio (zoom_tremido) | PROTAGONISTA | No visor, o elevador já estava *subindo* de novo. Com o médico dentro. Eu tinha um minuto. A: voltar pro elevador e tirar o médico do espelho, mesmo que ele me leve pro menos um. B: descer a escada e encarar o porteiro, deixando o médico pra trás. E você, o que faria? |

**Legenda:**

```
{RESULTADO_SE_HOUVER_VOTOS}Eu corri pra porta primeiro... e deixei o médico preso no espelho. 🛗

O Andar que Não Existe · Parte 3 — Alguém no meu lugar

Quem está esperando lá na portaria? Teoria aqui 👇

🅰️ Voltar e tirar o médico do espelho
🅱️ Descer e encarar o porteiro
A mais votada decide a Parte 4.

Marca quem desceria essa escada sozinho 👀

A Parte 4 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#terror #elevador #historiasempartes #vocedecide #suspense #misterio
```


---

## 17h52 — Nessa Cidade, a Sirene Toca às 18h · Parte 4

_Sem votos registrados na Parte 3 até agora -> padrão A (mais pessoal: o narrador perde algo de si; o caderno vira dele). Se não houver votos, a legenda NÃO fala de empate nem de 0 a 0 (contraria o AGENTE.md antigo, segue APRENDIZADOS + regra do dono). Protagonista é o chibi 'protagonista' da cartela do dono a partir desta parte (decisão do dono). As duas versões amarram a chave perdida da Parte 1 (o outro eu leva o caminho de casa) e convergem no mesmo dilema da Parte 5._

### Versão A (PADRÃO se não houver votos) — se ganhar A

- **Resumo:** Escolheram trocar: o outro eu some levando o caminho de casa do narrador, o Prefeito volta e passa o caderno pra ele, minutos antes da sirene da manhã.
- **Retomada do gancho:** Cena 1: 'Eu troquei o nome do Prefeito pelo do meu outro eu' (~3s).
- **Tamanho:** 9 cenas, 203 palavras · **zoom/tensão:** cenas 1, 4, 6, 8, 9
- **Final:** Sirene da manhã em um minuto, ninguém manda não olhar pra cima; dilema caderno x olhar. Tela de votos 'Segue @mundoemhistorias pra ver a Parte 5'.
- **Gatilho de compartilhar:** Chamada + legenda: 'Marca quem olharia pra cima sem pensar'.
- **Próxima votação:** 🅰️ Ficar com o caderno × 🅱️ Olhar pra cima na sirene · chamada: "Marca quem olharia pra cima sem pensar"

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | rua_noite (zoom_rosto) | PROTAGONISTA | Eu troquei o nome do Prefeito pelo do *meu outro eu*. E ele começou a sumir *sorrindo*. |
| 2 | casa_noite (in) | PREFEITO | Na janela, as mãos do Prefeito voltaram a ter cor. Depois os pés. Ele respirou fundo, como quem sai de baixo d'água. |
| 3 | rua_noite (in) | OUTRO_EU, PROTAGONISTA | **O outro eu:** Não fica triste. Eu levo só *uma coisa* comigo. / **Eu:** Que coisa? |
| 4 🔥 | escuro (shake) | PROTAGONISTA | Ele virou fumaça. Eu tentei lembrar o caminho de casa. A rua. A cor da porta. *Nada*. Eu não sabia mais onde eu morava. |
| 5 | rua_noite (pan_l) | POLICIAL, PROTAGONISTA | **Policial:** Foi isso que ele levou, menino. A sua casa. Por isso você perdeu a chave na primeira noite. / **Eu:** Então ele já estava me levando *antes*? |
| 6 🔥 | casa_noite (zoom_rosto) | PREFEITO | **Prefeito:** Trinta anos eu segurei esse caderno. Quem troca um nome vira o *dono* dele. Agora é você. |
| 7 | escuro (zoom_forte) [carta: O CADERNO] | — | Na última página, a tinta vermelha escreveu sozinha: *dono novo*. E embaixo, o meu nome. |
| 8 🔥 | rua_amanhecer (zoom_tremido) | PROTAGONISTA | O céu começou a clarear. O ponteiro vermelho do relógio agora corria pra frente. A sirene da manhã ia tocar em *um minuto*. E dessa vez ninguém mandou eu não olhar pra cima. |
| 9 🔥 | escuro (shake) | PROTAGONISTA | A: ficar com o caderno e escrever um nome por ano, como o Prefeito fez. B: olhar pra cima quando a sirene tocar e descobrir o que vem lá de cima, sem proteção nenhuma. E você, o que faria? |

**Legenda:**

```
{RESULTADO_SE_HOUVER_VOTOS}Eu troquei o nome... e esqueci onde eu moro. 🚨

Nessa Cidade, a Sirene Toca às 18h · Parte 4 — O dono do caderno

O que você acha que vem lá de cima? Teoria aqui 👇

🅰️ Ficar com o caderno
🅱️ Olhar pra cima na sirene
A mais votada decide a Parte 5.

Marca quem olharia pra cima sem pensar 👀

A Parte 5 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#distopia #sirene #historiasempartes #suspense #vocedecide
```

### Versão B — se ganhar B

- **Resumo:** Escolheram deixar o Prefeito sumir: o caderno fica sem dono, o outro eu tenta escrever o nome do narrador e ele recupera o caderno pela metade, minutos antes da sirene da manhã.
- **Retomada do gancho:** Cena 1: 'Eu não troquei o nome. E o Prefeito sumiu' (~3s).
- **Tamanho:** 9 cenas, 201 palavras · **zoom/tensão:** cenas 1, 4, 8, 9
- **Final:** Sirene da manhã em um minuto, ninguém manda não olhar pra cima; dilema caderno x olhar. Tela de votos 'Segue @mundoemhistorias pra ver a Parte 5'.
- **Gatilho de compartilhar:** Chamada + legenda: 'Marca quem olharia pra cima sem pensar'.
- **Próxima votação:** 🅰️ Ficar com o caderno × 🅱️ Olhar pra cima na sirene · chamada: "Marca quem olharia pra cima sem pensar"

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | rua_noite (zoom_rosto) | PROTAGONISTA | Eu não troquei o nome. E o Prefeito *sumiu* bem na minha frente. |
| 2 | casa_noite (in) | — | Primeiro as mãos, depois o sorriso. Na janela, ficou só o terno vazio, caindo devagar no chão. |
| 3 | rua_noite (pan_l) | POLICIAL, PROTAGONISTA | **Policial:** Trinta anos ele segurou isso. Agora o caderno *não tem dono*. / **Eu:** E o que um caderno sem dono faz? |
| 4 🔥 | rua_noite (zoom_rosto) | OUTRO_EU, PROTAGONISTA | **O outro eu:** Ele procura um. E eu cheguei *primeiro*. / **Eu:** E ele arrancou o caderno da minha mão. |
| 5 | escuro (shake) [carta: O CADERNO] | — | A caneta escreveu sozinha, em vermelho, um nome que eu conhecia muito bem. O *meu*. |
| 6 | rua_noite (in) | POLICIAL | **Policial:** Só o dono pode trocar! Pega de volta antes da sirene da manhã! |
| 7 | rua_noite (in) | PROTAGONISTA | Eu puxei o caderno de volta e o meu nome ficou pela metade. Mas eu senti: eu tinha esquecido o caminho de casa. Por isso eu perdi a chave naquela primeira noite. |
| 8 🔥 | rua_amanhecer (zoom_tremido) | PROTAGONISTA | O céu começou a clarear. O ponteiro vermelho do relógio agora corria pra frente. A sirene da manhã ia tocar em *um minuto*. E dessa vez ninguém mandou eu não olhar pra cima. |
| 9 🔥 | escuro (shake) | PROTAGONISTA | Agora o caderno era meu. A: ficar com o caderno e escrever um nome por ano, como o Prefeito fez. B: olhar pra cima quando a sirene tocar e descobrir o que vem lá de cima, sem proteção nenhuma. E você, o que faria? |

**Legenda:**

```
{RESULTADO_SE_HOUVER_VOTOS}O Prefeito sumiu... e o caderno escreveu o meu nome. 🚨

Nessa Cidade, a Sirene Toca às 18h · Parte 4 — O dono do caderno

O que você acha que vem lá de cima? Teoria aqui 👇

🅰️ Ficar com o caderno
🅱️ Olhar pra cima na sirene
A mais votada decide a Parte 5.

Marca quem olharia pra cima sem pensar 👀

A Parte 5 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#distopia #sirene #historiasempartes #suspense #vocedecide
```


---

## 20h52 — O Sombra da Sala 12 · Parte 2

_Roteiro 'pronta' mantido; só a cena 1 ganhou a retomada do gancho (prazo de 5 dias + chave perdida que a lousa previu) e a cena 9 troca 'A Parte Três fica no perfil' por um gancho pra noite na escola (P3) + gatilho de compartilhar. Aplicar essas 2 cenas no historia.json._

### Versão única

- **Resumo:** As chaves do Seu Bento somem como a lousa previu, o giz azul aponta para o professor Rui e um bilhete na letra do Teo mostra que o Sombra está sempre um passo à frente.
- **Retomada do gancho:** Cena 1: 'Cinco dias pra provar que eu não sou o Sombra' (~3s).
- **Tamanho:** 9 cenas, 231 palavras · **zoom/tensão:** cenas 1, 9
- **Final:** O Sombra sabia antes deles; para pegá-lo, Teo (que tem medo do escuro) vai ter que ficar na escola de noite.
- **Gatilho de compartilhar:** Fala final + legenda: 'Manda pro amigo que sempre sabe tudo antes de você'.

| # | Cenário | Personagens | Texto / falas |
|---|---|---|---|
| 1 🔥 | corredor_predio (zoom_forte) | BENTO | Cinco dias pra provar que eu não sou o Sombra. E às sete da manhã, o grito do *Seu Bento*: as chaves da escola tinham *sumido*. |
| 2 | corredor_predio (in) | BENTO, TEO | **Seu Bento:** Trinta anos nessa escola e eu nunca perdi uma chave. Nunca! / **Teo:** O senhor emprestou pra alguém, Seu Bento? / **Seu Bento:** Só pra quem pede *por favor*. E ontem muita gente pediu. |
| 3 | sala_aula (pan_r) | TEO | Na lousa, o Sombra tinha escrito: *eu avisei*. Mas dessa vez a Nina notou um detalhe que ninguém mais viu. A turma inteira ficou olhando pra mim de novo. |
| 4 | sala_aula (in) | NINA | **Nina:** Olha a cor, Teo. O giz é *azul*. Na escola inteira, só um professor usa giz azul. |
| 5 | sala_aula (pan_l) | RUI, TEO | O *professor Rui*. Chegou esse ano, ensina matemática, e guarda o giz azul trancado na gaveta como se fosse ouro. Ele sempre chega antes de todo mundo e sai por último. |
| 6 | sala_aula (in) | RUI | **Prof. Rui:** Alguém mexeu na minha gaveta, eu sei. Faltam três caixas. E vocês dois estão me olhando muito estranho. |
| 7 | corredor_predio (pan_r) | NINA, TEO | No intervalo, a gente voltou escondido pra sala dele. A gaveta estava *aberta*. Sem cadeado. Sem giz. Eu senti o estômago gelar. Se alguém visse a gente ali, era o fim. |
| 8 | escuro (zoom_forte) [bilhete: ] | — | No fundo, dobrado, tinha um bilhete. Escrito na *minha letra*. |
| 9 🔥 | sala_aula (shake) | TEO | O Sombra sabia que a gente vinha. Sabia *antes* da gente. Ou seja: estava perto. Muito perto. E pra pegar ele, eu ia ter que ficar na escola... *de noite*. Manda pro amigo que sempre sabe tudo antes de você. |

**Legenda:**

```
O giz era azul… e só um professor da escola usa giz azul. 🔵

O Sombra da Sala 12 · Parte 2 — O giz azul

Você confiaria no professor Rui? Chuta quem é o Sombra 👇

Manda pro amigo que sempre sabe tudo antes de você 👀

A Parte 3 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#misterio #escola #historiasempartes #detetive #comedia
```


---

## Elenco e vozes do dia (travados, nenhum personagem novo)

**A Ponte Caída** (`cartela`): Rafa (RAFA) = `fotografo`, `piper:cadu` 1.0/1.0; Dona Célia (CELIA) = `vovozinha`, `kokoro:pf_dora` 0.88/0.9; Júnior (JUNIOR) = `garoto_gorro_preto`, `kokoro:pm_alex` 1.12/1.06; Marina (MARINA) = `moca_loira`, `kokoro:pf_dora` 1.02/1.0

**O Último Ônibus** (`cartela`): Lia (LIA) = `garota_moletom_roxo`, `kokoro:pf_dora` 1.0/1.0; Seu Ivo (IVO) = `porteiro`, `kokoro:pm_santa` 0.94/0.92; Motorista (MOTORISTA) = `motorista` escurecido, `piper:jeff` 0.93/0.86; Lia mais velha (LIA_VELHA) = `mulher_vestido_roxo`, `kokoro:mix:pf_dora*0.8+pm_santa*0.2` 0.95/0.88; Menina (MENINA) = `menina_laco_vermelho`, `kokoro:pf_dora` 1.08/1.08; Bia (BIA) = `menina_vestido_rosa`, `kokoro:mix:pf_dora*0.85+pm_alex*0.15` 1.05/1.0

**O Andar que Não Existe** (`andar`): Você (PROTAGONISTA) = `andar_voce`, `kokoro:pm_alex` 1.04/1.0; Médico (MEDICO) = `andar_medico`, `piper:faber` 0.95/0.95; Porteiro (PORTEIRO) = `andar_porteiro`, `kokoro:pm_santa` 0.9/0.92

**Nessa Cidade, a Sirene Toca às 18h** (`cartela`): Eu (PROTAGONISTA) = `protagonista`, `piper:cadu` 1.0/1.0; O outro eu (OUTRO_EU) = `protagonista` escurecido, `piper:cadu` 0.88/0.92; Prefeito (PREFEITO) = `prefeito`, `kokoro:pm_santa` 0.92/0.9; Policial (POLICIAL) = `policial`, `piper:jeff` 0.97/1.0

**O Sombra da Sala 12** (`andar`): Teo (TEO) = `andar_menino`, `kokoro:pm_alex` 1.12/1.04; Nina (NINA) = `andar_leitora`, `kokoro:pf_dora` 1.14/1.05; Caio (CAIO) = `andar_rival`, `piper:faber` 1.1/1.04; Seu Bento (BENTO) = `andar_zelador`, `kokoro:pm_santa` 0.9/0.92; Prof. Rui (RUI) = `andar_professor`, `piper:jeff` 0.98/1.0; Diretora Marta (MARTA) = `andar_jornalista`, `kokoro:pf_dora` 0.92/0.95

## Arco planejado das votações (coerência)

- **O Andar que Não Existe:** P3 o porteiro diz que a mãe do Você (que saiu do prédio há 10 anos) o espera na portaria → P4 consequência (A: tira o médico e os dois descem juntos / B: desce sozinho e a portaria é o -1) → P5 revelação: o -1 guarda quem "saiu" do prédio e o porteiro precisa de alguém no lugar para poder sair → P6 final fecha o -1 (quem fica no lugar do porteiro).
- **Nessa Cidade, a Sirene Toca às 18h:** P4 o caderno vira do narrador e ele descobre que o outro eu levou o caminho de casa (a chave perdida da P1) → P5 (A: escreve um nome e vira o novo Prefeito / B: olha pra cima e vê o que a sirene esconde) → P6 o que vem lá de cima apaga quem está na rua; o ciclo só quebra quando o narrador aceita de volta tudo o que esqueceu (o outro eu) e o caderno perde a força.
- **A Ponte Caída:** segue a bíblia (escolhas de confiar somam pro Final A; desconfiar/separar pro Final B).

## Problemas / avisos

- `elevador` P3: a escolha da Parte 2 ainda não está registrada no `historia.json` (a preparação dá ERRO até a Produção contar os votos e gravar `votos`/`escolha`). Na bíblia: B 2 × 0 A.
- `ultimo-onibus` P2: o roteiro pronto tinha 81 palavras; usar o pré-roteiro expandido desta ficha.
- Vozes fora da faixa recomendada (0.93–1.08), mas já travadas em `personagens_travados` — não mudar no meio da história: Júnior 1.12, Dona Célia 0.88 (Ponte); Teo 1.12, Nina 1.14, Caio 1.10, Seu Bento 0.90, Marta 0.92 (Sombra); Porteiro 0.90 (Elevador); Outro eu 0.88, Prefeito 0.92 (Sirene). Vale a QC ouvir com atenção.
- `AGENTE.md` ainda manda escrever "Deu empate, então eu decidi..." quando há 0 votos; APRENDIZADOS e o dono pedem o contrário. As fichas seguem o dono.
