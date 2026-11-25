# PLANO — 25/11/2026 (quarta) · SEMANA ECONÔMICA

Estação 1 (Planejamento). Horários de **Brasília** (America/Sao_Paulo). **Semana Econômica** (pedido do dono em 23/11, vale até ele mandar voltar ao normal): só 3 posts, só as 3 histórias abaixo. **A Ponte Caída** (parou na Parte 1) e **O Último Ônibus** (parou na Parte 2) seguem PAUSADAS. Nenhuma história nova. Fichas só `1152.json`, `1752.json`, `2052.json`.

## Cronograma do dia

| Horário (Brasília) | História | Parte | Tipo | Estilo | Versão padrão | Capa | 1ª frase (padrão) |
|---|---|---|---|---|---|---|---|
| 11:52 | O Andar que Não Existe (`elevador`) | 5 | votação A/B | andar | B | O Andar que Não Existe · Parte 5 — O espelho cobra | Onze e cinquenta e nove. Eu empurrei o porteiro pro elevador. |
| 17:52 | Nessa Cidade, a Sirene Toca às 18h (`cidade-sirene`) | 6 · FINAL | votação A/B | cartela | B | Nessa Cidade, a Sirene Toca às 18h · Parte 6 · FINAL — O relógio parado | Cinco e cinquenta e nove. Eu subi a torre do relógio correndo. |
| 20:52 | O Sombra da Sala 12 (`o-sombra-da-sala-12`) | 4 | contínua | andar | unica | O Sombra da Sala 12 · Parte 4 — Debaixo do número 12 | Sete e vinte e quatro. Debaixo da placa da sala doze, o chão fez oco. |

**Por que esta ordem (desempenho):** mantém o horário fixo de cada série (regra de 1 parte por dia no mesmo horário) e a mais forte às 20:52: **O Sombra da Sala 12** tem a melhor retenção da conta (P1 1.451 views, pulo 28,5%, 26,4 s). A **Sirene** (melhor série no total) fecha com o FINAL às 17:52; o **Elevador** (P3/P4 com o pior tempo médio) fica às 11:52.
**Trava de 20 h:** Elevador P4 saiu 24/11 15:55 UTC → 11:52 (14:52 UTC) = 22h57 ✔; Sirene P5 24/11 21:55 UTC → 17:52 (20:52 UTC) = 22h57 ✔; Sombra P3 25/11 00:55 UTC → 20:52 (23:52 UTC) = 22h57 ✔.
**⚠ Decisão do dono:** a Sirene termina amanhã (Parte 6). Pela regra da Semana Econômica não entra história nova e Ponte/Ônibus estão pausadas, então **a partir de 26/11 o horário 17:52 fica vago** (só 2 posts/dia) até o dono decidir (liberar uma pausada, criar nova ou ficar com 2).

## Regras aplicadas (REGRAS DOS VIRAIS + APRENDIZADOS)

- Frase 1 = conflito + algo pessoal + hora concreta (23:59, 17:59, 19:24); retomada ≤3 s com fato novo; sem "Nas partes anteriores"; `gancho_tela` (até 5 palavras) no 1º quadro.
- Sem currículo; 17–20 cenas curtas (≤15 palavras nas primeiras 6 cenas), 191–203 palavras.
- Relógio na tela em ≥3 cenas avançando; ≥1 celular/papel legível; final com virada de quem sabe mais (mensagem da mãe / porteiro no interfone / Prefeito / outro eu / SMS do Sombra).
- Votação: A/B com custo claro + "Comenta A ou B"; contínua: "Comenta PARTE CINCO pra saber se o Caio é o Sombra"; final da Sirene sem tela de votos; Sirene B testa o FINAL EM LOOP (ponteiro volta pra 17:59 = 1ª frase).
- Legenda: linha 1 = gancho; `{RESULTADO_SE_HOUVER_VOTOS}` só na linha 2 (vira "Vocês escolheram X (a a b)!" ou some; nunca dizer que ninguém votou); linha "Manda pra quem...".
- Conferido com `tools/preparar.py` numa cópia (cada versão inserida no historia.json): todas "Tudo certo: pode gerar o vídeo" (aviso proposital na Sirene A cena 16: "a sirene nunca mais tocou", sem alerta). `checar_catalogos` ok.


---

## 11h52 — O Andar que Não Existe · Parte 5

_Votos da Parte 4 (media 18077993924592764) ainda chegando: a Produção e a Publicação recontam. Padrão B (prender o porteiro no -1): a série teve B em todas as votações e B lidera (kevin_12_zn). SEM recapitulação. Faixa do topo = 'PARTE 5 · <título>'. Legenda: linha 1 = gancho; {RESULTADO_SE_HOUVER_VOTOS} na linha 2 vira 'Vocês escolheram X (a a b)!' ou some (nunca dizer que ninguém votou). Quem sabe mais: na B, a mensagem da mãe ('não confia no médico') contra o médico; na A, o porteiro que já saiu do -1. A mãe NÃO tem personagem nem voz (só aparece em mensagem/câmera), porque andar_mae já é da Lia mais velha no Último Ônibus. Cena de capa: Você em close (B na portaria, A no elevador -1)._

### Versão B — se ganhar B (PADRÃO)

- **Resumo:** Escolheram prender o porteiro: à meia-noite a mãe não sai; o médico diz que o espelho solta ela em troca do reflexo do Você (fecha às 00:06), mas chega mensagem da mãe: 'não confia no médico'.
- **Retomada:** Cena 1: 'Onze e cinquenta e nove. Eu empurrei o porteiro pro elevador.' (~3 s, fato novo: o empurrão)
- **Tamanho:** 20 cenas, 198 palavras · **zoom/tensão:** cenas 1, 2, 3, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 20
- **Relógio na tela:** cena 3 placa '-1 · 00:00'; cena 5 placa '00:02'; cena 12 carta 'NO ESPELHO:'; cena 15 celular '00:04 · DESCONHECIDO'; cena 17 placa '00:05'
- **Celular/papel:** cena 12 carta 'NO ESPELHO:': !O ESPELHO FECHA / !ÀS 00:06; cena 15 celular '00:04 · DESCONHECIDO': Filho, não confia / !no médico. / Ele quer o seu lugar. / — MÃE
- **Final:** Virada: mensagem de número desconhecido assinada MÃE ('Filho, não confia no médico. Ele quer o seu lugar.') contra o médico, que diz que é o porteiro escrevendo. 00:05, espelho embaçando. A/B com custo + 'Comenta A ou B'.
- **Compartilhar:** Manda pra quem nunca confia em ninguém
- **Opções:** A) Dar meu reflexo pra mãe sair · B) Soltar o porteiro e confiar nela
- **Capa:** O Andar que Não Existe · Parte 5 — O espelho cobra · **gancho na tela:** PRENDI O PORTEIRO
- **Cenários:** elevador, escuro, porao, recepcao_hotel

**Cenas:**

1. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam zoom_tremido hook cover · PROTAGONISTA(busto) — Onze e cinquenta e nove. Eu empurrei o porteiro *pro elevador*.
2. `elevador` {"floor": "T"} · cam shake tensao · PORTEIRO(busto) — [PORTEIRO] Garoto, não! Sem mim, *ninguém sai* de lá!
3. `escuro`  · cam zoom_forte tensao · sem personagem · prop placa '-1 · 00:00' — A porta fechou. O visor caiu direto no *menos um*. Meia-noite.
4. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam in  · PROTAGONISTA(busto) — Eu fiquei olhando a porta da rua. Esperando a minha mãe *entrar*.
5. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam out  · sem personagem · prop placa '00:02' — Meia-noite e dois. *Ninguém* entrou.
6. `elevador` {"floor": "-1"} · cam zoom_rosto filtro tv tensao · PORTEIRO(busto) — [PORTEIRO] Eu avisei. Quem prende o porteiro, *prende ela também*.
7. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam in  · PROTAGONISTA(busto) — [PROTAGONISTA] Então me fala como *tirar ela*!
8. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite", "luz": "apagada"} · cam shake tensao · sem personagem — O interfone chiou e morreu. E a luz da portaria *apagou*.
9. `elevador` {"floor": "T"} · cam pan_l  · sem personagem — Aí o elevador voltou. Vazio. E o espelho *batendo de dentro*.
10. `elevador` {"floor": "T"} · cam zoom_rosto  · MEDICO(busto) — [MEDICO] Ela tá aqui comigo. Do lado de cá do *espelho*.
11. `elevador` {"floor": "T"} · cam in  · PROTAGONISTA, MEDICO — [PROTAGONISTA] Então puxa ela! [MEDICO] O espelho só solta alguém se você der o seu *reflexo*.
12. `escuro`  · cam zoom_forte  · sem personagem · prop carta 'NO ESPELHO:' !O ESPELHO FECHA / !ÀS 00:06 — No vapor, mais um recado. Com hora *marcada*.
13. `elevador` {"floor": "T"} · cam zoom_rosto  · PROTAGONISTA(busto) — Meu reflexo. Eu nunca mais ia me ver em espelho *nenhum*.
14. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite", "luz": "apagada"} · cam zoom_rosto tensao · PROTAGONISTA(busto) — Meia-noite e quatro. Meu celular vibrou. *Número desconhecido*.
15. `escuro`  · cam zoom_forte hook · sem personagem · prop celular '00:04 · DESCONHECIDO' Filho, não confia / !no médico. / Ele quer o seu lugar. / — MÃE — Dez anos sem notícia. E agora, *uma mensagem dela*.
16. `elevador` {"floor": "T"} · cam shake tensao · MEDICO(busto) — [MEDICO] É mentira! É o porteiro *escrevendo por ela*!
17. `elevador` {"floor": "T"} · cam zoom_forte  · sem personagem · prop placa '00:05' — Meia-noite e cinco. O espelho começou a *embaçar de vez*.
18. `elevador` {"floor": "T"} · cam zoom_rosto hook · MEDICO(busto) — A: confio no médico e dou o meu reflexo pra minha mãe *sair*.
19. `porao` {"texto": "SUBSOLO"} · cam pan_r  · sem personagem — B: confio na mensagem e solto o porteiro. Mas ele pode *me prender lá*.
20. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite", "luz": "apagada"} · cam zoom_rosto hook · PROTAGONISTA(busto) — E você, em quem confiaria? Comenta *A ou B*.

**Legenda:**
```
Meia-noite. Eu prendi o porteiro no -1... e a minha mãe não saiu. 🛗
{RESULTADO_SE_HOUVER_VOTOS}
O Andar que Não Existe · Parte 5 — O espelho cobra

O médico ou a mensagem: quem tá mentindo? Teoria aqui 👇

🅰️ Confiar no médico e dar meu reflexo (nunca mais me ver)
🅱️ Confiar na mensagem e soltar o porteiro (ele pode me prender)
A mais votada decide a Parte 6, o FINAL.

Manda pra quem nunca confia em ninguém 👀

A Parte 6 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#terror #espelho #historiasempartes #misterio #suspense #vocedecide
```

### Versão A — se ganhar A

- **Resumo:** Escolheram ficar no -1: a mãe sai pela portaria, mas o porteiro (que saiu do -1 dez anos atrás) abre a porta pra ela sorrindo; o médico avisa que às 00:10 o Você esquece a mãe para sempre.
- **Retomada:** Cena 1: 'Onze e cinquenta e nove. Eu entrei no elevador. E apertei o menos um.' (~3 s, fato novo: ele entrou)
- **Tamanho:** 19 cenas, 203 palavras · **zoom/tensão:** cenas 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 15, 16, 17, 19
- **Relógio na tela:** cena 2 placa '-1 · 00:00'; cena 8 placa '00:03'; cena 10 carta 'QUEM ENTROU NO -1'; cena 14 celular '00:06 · INTERFONE -1'; cena 16 placa '00:08'
- **Celular/papel:** cena 10 carta 'QUEM ENTROU NO -1': PORTEIRO · 1974 / !SAIU HÁ 10 ANOS /  / !VOCÊ · HOJE 00:00; cena 14 celular '00:06 · INTERFONE -1': Obrigado, garoto. / !Agora ela é minha / !lá em cima.
- **Final:** Virada: mensagem no interfone do -1, do porteiro (quem sabe mais): 'Obrigado, garoto. Agora ela é minha lá em cima.' 00:08. A/B com custo + 'Comenta A ou B'.
- **Compartilhar:** Manda pra quem faria tudo pela mãe
- **Opções:** A) Ficar e esquecer minha mãe · B) Subir pelo espelho com o médico
- **Capa:** O Andar que Não Existe · Parte 5 — Quem entrou no -1 · **gancho na tela:** EU ENTREI NO -1
- **Cenários:** corredor_predio, elevador, escuro, porao, recepcao_hotel

**Cenas:**

1. `elevador` {"floor": "-1"} · cam zoom_tremido hook cover · PROTAGONISTA(busto) — Onze e cinquenta e nove. Eu entrei no elevador. E apertei o *menos um*.
2. `elevador` {"floor": "-1"} · cam shake tensao · sem personagem · prop placa '-1 · 00:00' — Meia-noite. A porta abriu no andar que *não existe*.
3. `corredor_predio` {"luz": "apagada"} · cam pan_l  · PROTAGONISTA, MEDICO — Era o corredor do meu prédio. E o médico, *me esperando*.
4. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam zoom_forte filtro tv tensao · sem personagem — Na telinha do interfone, câmera três: minha mãe saindo na *portaria*.
5. `corredor_predio` {"luz": "apagada"} · cam zoom_rosto  · PROTAGONISTA(busto) — [PROTAGONISTA] Ela saiu. Dez anos depois, ela *saiu*.
6. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam in filtro tv  · PORTEIRO(busto) — Mas quem abriu a porta da rua pra ela foi o porteiro. *Sorrindo*.
7. `corredor_predio` {"luz": "apagada"} · cam zoom_rosto tensao · MEDICO(busto) — [MEDICO] A troca tem preço. À meia-noite e dez, você *esquece ela*.
8. `escuro`  · cam zoom_forte tensao · sem personagem · prop placa '00:03' — Meia-noite e três. Eu já não lembrava a *voz dela*.
9. `porao` {"texto": "SUBSOLO"} · cam in  · MEDICO, PROTAGONISTA — O médico me levou até o subsolo. Lá tinha um livro *aberto*.
10. `escuro`  · cam zoom_forte  · sem personagem · prop carta 'QUEM ENTROU NO -1' PORTEIRO · 1974 / !SAIU HÁ 10 ANOS /  / !VOCÊ · HOJE 00:00 — O porteiro entrou aqui em setenta e quatro. E saiu *no lugar dela*.
11. `porao` {"texto": "SUBSOLO"} · cam zoom_rosto  · PROTAGONISTA(busto) — [PROTAGONISTA] Tem que ter um jeito de sair *sem trocar*!
12. `porao` {"texto": "SUBSOLO"} · cam in  · MEDICO(busto) — [MEDICO] Tem. Pelo espelho do elevador. Mas aí ela volta pro *seu lugar*.
13. `porao` {"texto": "SUBSOLO", "luz": "apagada"} · cam shake tensao · sem personagem — Aí o interfone do subsolo acendeu. *Sozinho*.
14. `escuro`  · cam zoom_forte hook · sem personagem · prop celular '00:06 · INTERFONE -1' Obrigado, garoto. / !Agora ela é minha / !lá em cima. — Uma mensagem na telinha. Do único que *saiu* daqui.
15. `recepcao_hotel` {"texto": "PORTARIA", "hora": "noite"} · cam zoom_tremido filtro tv tensao · PORTEIRO(busto) — [PORTEIRO] Pode esquecer em paz. Eu cuido da sua mãe *aqui em cima*.
16. `elevador` {"floor": "-1"} · cam zoom_forte  · sem personagem · prop placa '00:08' — Meia-noite e oito. Dois minutos pra eu *esquecer ela* pra sempre.
17. `porao` {"texto": "SUBSOLO"} · cam zoom_rosto hook · PROTAGONISTA(busto) — A: fico aqui e esqueço tudo. Ela fica livre... *com ele*.
18. `elevador` {"floor": "-1"} · cam in  · MEDICO(busto) — B: subo pelo espelho com o médico. E ela *volta pra cá*.
19. `corredor_predio` {"luz": "apagada"} · cam zoom_rosto hook · PROTAGONISTA(busto) — E você, o que faria? Comenta *A ou B*.

**Legenda:**
```
Meia-noite. Eu entrei no -1 pra minha mãe sair... e o porteiro abriu a porta pra ela. 🛗
{RESULTADO_SE_HOUVER_VOTOS}
O Andar que Não Existe · Parte 5 — Quem entrou no -1

O que o porteiro quer com ela lá em cima? Teoria aqui 👇

🅰️ Ficar e esquecer minha mãe (ela fica livre, com ele)
🅱️ Subir pelo espelho com o médico (ela volta pro -1)
A mais votada decide a Parte 6, o FINAL.

Manda pra quem faria tudo pela mãe 👀

A Parte 6 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#terror #elevador #historiasempartes #misterio #suspense #vocedecide
```


---

## 17h52 — Nessa Cidade, a Sirene Toca às 18h · Parte 6 (FINAL)

_PARTE 6 = FINAL (capa 'PARTE 6 · FINAL'). A versão depende dos votos da Parte 5 (media da ficha 24/11 1752): a Produção e a Publicação recontam. Padrão B (parar o relógio): é a mais dramática e a série vem de B. Sem tela de votos no fim (não há Parte 7): o vídeo termina na virada. Legenda: linha 1 = gancho; {RESULTADO_SE_HOUVER_VOTOS} na linha 2 vira 'Vocês escolheram X (a a b)!' ou some. Fecha o mistério (céu-espelho = sumidos; Prefeito escrevia nomes pra esconder o Policial, que olhou pra cima com ele aos 8 anos). B termina em LOOP (ponteiro volta pra 17:59 = 1ª frase), teste de reassistida do APRENDIZADOS; A termina com o outro eu (quem sabe mais) achando outro caderno. ATENÇÃO: depois desta parte a Sirene acaba e, na Semana Econômica, não pode entrar história nova; o horário 17:52 de 26/11 fica vago até o dono decidir._

### Versão B — se ganhar B (PADRÃO)

- **Resumo:** Escolheram parar o relógio: às 18h o ponteiro trava, os sumidos descem (o Prefeito primeiro), o narrador esquece o próprio nome; o Policial escreve o nome dele pela última vez e ele lembra; o Prefeito avisa que basta alguém dar corda e o ponteiro volta pra 17:59.
- **Retomada:** Cena 1: 'Cinco e cinquenta e nove. Eu subi a torre do relógio correndo.' (~3 s, fato novo: ele está na torre)
- **Tamanho:** 19 cenas, 194 palavras · **zoom/tensão:** cenas 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 16, 17, 18, 19
- **Relógio na tela:** cena 1 relógio do cenário 17:59; cena 2 relógio do cenário 17:59; cena 3 placa '17:59:50'; cena 4 relógio do cenário 18:00; cena 5 relógio do cenário 18:00; cena 6 relógio do cenário 18:00; cena 7 relógio do cenário 18:01; cena 10 relógio do cenário 18:02; cena 11 relógio do cenário 18:02; cena 12 relógio do cenário 18:03; cena 13 placa '18:03'; cena 15 relógio do cenário 18:03; cena 16 relógio do cenário 18:04; cena 17 relógio do cenário 18:04; cena 18 relógio do cenário 18:04; cena 19 placa '17:59'
- **Celular/papel:** cena 9 carta 'O CADERNO': Nome não se apaga. / Só se troca. /  / !SEU NOME: ________
- **Final:** Virada + loop: o Prefeito (quem sabe mais) avisa que o relógio parado só segura até alguém dar corda; 'Tic' e o ponteiro volta pra 17:59, ecoando a 1ª frase. Sem resumo.
- **Compartilhar:** Manda pra quem esquece o próprio nome quando tá nervoso
- **Capa:** Nessa Cidade, a Sirene Toca às 18h · Parte 6 · FINAL — O relógio parado · **gancho na tela:** PAREI O RELÓGIO
- **Cenários:** casa, escuro, praca, rua_noite

**Cenas:**

1. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "17:59", "alerta": true} · cam zoom_tremido hook cover · PROTAGONISTA — Cinco e cinquenta e nove. Eu subi a torre do relógio *correndo*.
2. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "17:59"} · cam shake tensao · POLICIAL — [POLICIAL] Se parar o relógio, você esquece o *próprio nome*!
3. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "17:59"} · cam zoom_forte tensao · sem personagem · prop placa '17:59:50' — Dez segundos. Eu agarrei o ponteiro *vermelho* com as duas mãos.
4. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "alerta": true} · cam shake tensao · PROTAGONISTA — Seis em ponto. A sirene tocou. E o ponteiro *travou*.
5. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "neblina": true, "ceu_espelho": true} · cam zoom_forte tensao · sem personagem — Lá em cima, a cidade de cabeça pra baixo começou a *descer*. Devagar.
6. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "ceu_espelho": true} · cam in  · PREFEITO — O primeiro a pisar na praça foi o *Prefeito*. Inteiro.
7. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:01", "ceu_espelho": true} · cam zoom_rosto  · PREFEITO — [PREFEITO] Você parou o relógio? Sabe o que isso *te custa*?
8. `rua_noite`  · cam zoom_tremido tensao · PROTAGONISTA — [PROTAGONISTA] Quem é você? E... quem sou *eu*?
9. `escuro`  · cam zoom_forte hook · sem personagem · prop carta 'O CADERNO' Nome não se apaga. / Só se troca. /  / !SEU NOME: ________ — Abri o caderno. Na linha do meu nome, *só um borrão*.
10. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:02", "ceu_espelho": true} · cam in  · POLICIAL, PREFEITO — [PREFEITO] Ele olhou pra cima comigo. A gente tinha *oito anos*.
11. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:02"} · cam zoom_rosto  · PREFEITO — [PREFEITO] Escrevi trinta anos de nomes pra ninguém *levar ele*.
12. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:03"} · cam zoom_rosto  · POLICIAL — [POLICIAL] Me dá a caneta, menino. É a *última vez*.
13. `escuro`  · cam zoom_forte  · sem personagem · prop placa '18:03' — Seis e três. Ele escreveu um nome, letra por letra. *O meu*.
14. `casa` {"hora": "noite", "luz": "acesa", "texto": "9", "porta": [40, 110, 210]} · cam in  · sem personagem — A porta azul. A rua nove. Eu *lembrei de tudo*.
15. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "18:03"} · cam out  · PROTAGONISTA, POLICIAL — Na praça, os sumidos se abraçavam. Centenas de famílias, *voltando pra casa*.
16. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "18:04"} · cam zoom_rosto  · POLICIAL — [POLICIAL] Agora sim. Ninguém mais some *nessa cidade*.
17. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "18:04"} · cam zoom_rosto tensao · PREFEITO — [PREFEITO] Relógio parado segura eles. Até alguém *dar corda* de novo.
18. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "18:04"} · cam zoom_tremido tensao · PROTAGONISTA — Aí, atrás de mim, a torre fez um barulho. *Tic*.
19. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "17:59", "alerta": true} · cam zoom_forte hook · sem personagem · prop placa '17:59' — O ponteiro andou pra trás. E marcou *cinco e cinquenta e nove*.

**Legenda:**
```
Eu parei o relógio da sirene... e esqueci o meu próprio nome. 🚨
{RESULTADO_SE_HOUVER_VOTOS}
Nessa Cidade, a Sirene Toca às 18h · Parte 6 — FINAL: O relógio parado

Você pararia o relógio sabendo o preço? 👇

Manda pra quem esquece o próprio nome quando tá nervoso 👀

FIM. Começa da Parte 1 no perfil @mundoemhistorias. Nova história em breve 🔔

#distopia #sirene #historiasempartes #final #misterio
```

### Versão A — se ganhar A

- **Resumo:** Escolheram escrever o nome do Policial: ele olha pra cima de propósito e sobe por vontade própria; os sumidos descem (o Prefeito primeiro), o narrador rasga o caderno e a sirene nunca mais toca; mas o outro eu manda mensagem: achou outro caderno na cidade vizinha.
- **Retomada:** Cena 1: 'Cinco e cinquenta e nove. Eu escrevi o nome do Policial.' (~3 s, fato novo: o nome escrito)
- **Tamanho:** 20 cenas, 191 palavras · **zoom/tensão:** cenas 1, 2, 3, 4, 5, 6, 7, 10, 13, 14, 15, 18, 19, 20
- **Relógio na tela:** cena 1 relógio do cenário 17:59; cena 3 relógio do cenário 17:59; cena 4 relógio do cenário 18:00; cena 5 relógio do cenário 18:00; cena 6 relógio do cenário 18:00; cena 7 relógio do cenário 18:00; cena 8 relógio do cenário 18:01; cena 9 relógio do cenário 18:01; cena 10 relógio do cenário 18:02; cena 11 relógio do cenário 18:02; cena 13 placa '18:03'; cena 14 relógio do cenário 18:03; cena 16 relógio do cenário 18:05; cena 19 celular '18:00 · DESCONHECIDO'
- **Celular/papel:** cena 2 carta 'O CADERNO': Nome não se apaga. / Só se troca. /  / !O POLICIAL; cena 15 carta 'O CADERNO': !RASGADO / página por página; cena 19 celular '18:00 · DESCONHECIDO': Achei outro caderno. / !Na cidade vizinha. / — O OUTRO EU
- **Final:** Virada: mensagem do outro eu (quem sabe mais) 'Achei outro caderno. Na cidade vizinha.' + 'Eu ainda não terminei você.' (eco da Parte 5). Sem resumo.
- **Compartilhar:** Manda pra quem guardaria um segredo por trinta anos
- **Capa:** Nessa Cidade, a Sirene Toca às 18h · Parte 6 · FINAL — O último nome · **gancho na tela:** ESCREVI O NOME DELE
- **Cenários:** casa, escuro, praca, rua_noite

**Cenas:**

1. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "17:59", "alerta": true} · cam zoom_tremido hook cover · PROTAGONISTA — Cinco e cinquenta e nove. Eu escrevi o nome *do Policial*.
2. `escuro`  · cam zoom_forte tensao · sem personagem · prop carta 'O CADERNO' Nome não se apaga. / Só se troca. /  / !O POLICIAL — A tinta ficou vermelha na hora. E o Policial *sorriu*.
3. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "17:59"} · cam zoom_rosto  · POLICIAL — [POLICIAL] Tudo bem, menino. Eu esperei trinta anos por *esse nome*.
4. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "alerta": true} · cam shake tensao · POLICIAL — Seis em ponto. A sirene tocou. E ele *não correu*.
5. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "neblina": true, "ceu_espelho": true} · cam zoom_forte tensao · POLICIAL — Ele olhou pra cima. *De propósito*.
6. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "ceu_espelho": true} · cam zoom_tremido tensao · PROTAGONISTA — [PROTAGONISTA] Não! Fecha os olhos! Foi você que me *ensinou isso*!
7. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:00", "ceu_espelho": true} · cam zoom_rosto  · POLICIAL — [POLICIAL] Eu olhei com oito anos. O Prefeito escreveu nomes pra *me esconder*.
8. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:01", "neblina": true, "ceu_espelho": true} · cam out  · sem personagem — Ele começou a subir. E os sumidos começaram a *descer*.
9. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:01", "ceu_espelho": true} · cam in  · PREFEITO — O primeiro a pisar na praça foi o *Prefeito*. Inteiro.
10. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:02", "ceu_espelho": true} · cam zoom_rosto  · PREFEITO — [PREFEITO] Trinta anos de nomes. Pra ele subir *por vontade própria*.
11. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:02", "ceu_espelho": true} · cam in  · PROTAGONISTA, PREFEITO — [PROTAGONISTA] E o meu nome? Ficou *pela metade*. [PREFEITO] Olha pra sua *porta*, menino.
12. `casa` {"hora": "noite", "luz": "acesa", "texto": "9", "porta": [40, 110, 210]} · cam in  · sem personagem — A porta azul. A rua nove. O meu nome inteiro *voltou*.
13. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:03", "ceu_espelho": true} · cam zoom_forte  · sem personagem · prop placa '18:03' — Seis e três. Centenas de pessoas na praça. *Voltando pra casa*.
14. `praca` {"hora": "tarde", "seed": 7, "relogio": true, "relogio_hora": "18:03", "ceu_espelho": true} · cam zoom_rosto  · POLICIAL — [POLICIAL] Rasga o caderno, menino. Ninguém mais *escreve nome*.
15. `escuro`  · cam zoom_forte  · sem personagem · prop carta 'O CADERNO' !RASGADO / página por página — Eu rasguei. Página por página. *Nome por nome*.
16. `praca` {"hora": "noite", "seed": 7, "relogio": true, "relogio_hora": "18:05"} · cam in  · PROTAGONISTA, PREFEITO — O ponteiro vermelho parou. E a sirene *nunca mais tocou*.
17. `rua_noite`  · cam in  · PROTAGONISTA — No dia seguinte, às seis, eu fiquei na rua. Olhando pra cima. *Sem medo*.
18. `rua_noite`  · cam zoom_rosto tensao · PROTAGONISTA — Até o meu celular vibrar. *Número desconhecido*.
19. `escuro`  · cam zoom_forte hook · sem personagem · prop celular '18:00 · DESCONHECIDO' Achei outro caderno. / !Na cidade vizinha. / — O OUTRO EU — Achei outro caderno. Na cidade *vizinha*.
20. `rua_noite` {"alerta": true} · cam zoom_tremido hook · OUTRO_EU — [OUTRO_EU] Eu ainda não terminei *você*.

**Legenda:**
```
Eu escrevi o nome do Policial... e ele olhou pra cima de propósito. 🚨
{RESULTADO_SE_HOUVER_VOTOS}
Nessa Cidade, a Sirene Toca às 18h · Parte 6 — FINAL: O último nome

Quem você escreveria no caderno? 👇

Manda pra quem guardaria um segredo por trinta anos 👀

FIM. Começa da Parte 1 no perfil @mundoemhistorias. Nova história em breve 🔔

#distopia #sirene #historiasempartes #final #suspense
```


---

## 20h52 — O Sombra da Sala 12 · Parte 4

_O script 'pronta' da Parte 4 no historia.json tinha 9 cenas longas, cenários antigos (corredor_predio/sala_aula) e terminava com 'A Parte Cinco fica no perfil' (proibido). Este pré-roteiro reescreve em 20 cenas com as regras dos virais, mantendo os fatos da bíblia (ladrilho solto sob a placa SALA 12, chave pequena, foto TURMA 12 · 1996 com a Marta criança, demolição no mês que vem, turma dividida em 3, tênis de estrela do Caio). Continua direto da P3 (19:22 na porta da sala 12). Fato novo pequeno: SMS do Sombra 12:21 'Viu a estrela, né? Não conta pra ninguém. Ainda.' (coerente com Caio querendo salvar a sala). Relógio: 19:24 → QUARTA 07:30 FALTAM 2 DIAS → 12:20 → 12:21. A Produção deve substituir o script da parte 4 no historia.json por este. Caio só aparece no fim (não confessa antes da P6)._

### Versão única

- **Resumo:** Debaixo da placa da sala 12: chave e foto de 1996 com a Marta criança; ela revela a demolição e a turma dividida; na saída, Teo vê a estrela no tênis do Caio e o Sombra manda: 'Não conta pra ninguém. Ainda.'
- **Retomada:** Cena 1: 'Sete e vinte e quatro. Debaixo da placa da sala doze, o chão fez oco.' (~3 s, fato novo: o ladrilho oco)
- **Tamanho:** 20 cenas, 193 palavras · **zoom/tensão:** cenas 1, 2, 3, 5, 7, 8, 10, 11, 13, 14, 17, 18, 19, 20
- **Relógio na tela:** cena 4 relógio do cenário 19:26; cena 7 placa 'QUARTA · 07:30 · FALTAM 2 DIAS'; cena 15 placa '12:20'; cena 19 celular '12:21 · DESCONHECIDO'
- **Celular/papel:** cena 3 lista 'DEBAIXO DO 12': 1 chave pequena / !1 foto: TURMA 12 · 1996; cena 11 carta 'OFÍCIO DA ESCOLA': SALA 12: DEMOLIÇÃO / !DEZEMBRO / TURMA 12: DIVIDIDA EM 3; cena 19 celular '12:21 · DESCONHECIDO': Viu a estrela, né? / !Não conta pra ninguém. / Ainda. / — O SOMBRA
- **Final:** Virada: no segundo em que Teo vê a estrela no tênis do Caio, o Sombra (quem sabe mais, estava olhando) manda SMS 'Viu a estrela, né? Não conta pra ninguém. Ainda.' Chamada 'Comenta PARTE CINCO pra saber se o Caio é o Sombra'.
- **Compartilhar:** Manda pra quem ia ficar arrasado se a turma fosse dividida
- **Capa:** O Sombra da Sala 12 · Parte 4 — Debaixo do número 12 · **gancho na tela:** O CHÃO FEZ OCO
- **Cenários:** corredor_escola, escuro, gabinete, sala_escola

**Cenas:**

1. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "desvio": 120} · cam zoom_tremido hook cover · TEO(busto) — Sete e vinte e quatro. Debaixo da placa da sala doze, o chão fez *oco*.
2. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "desvio": -120} · cam zoom_rosto  · NINA(busto) — [NINA] O rejunte tá raspado. Alguém já *abriu isso*.
3. `escuro`  · cam zoom_forte tensao · sem personagem · prop lista 'DEBAIXO DO 12' 1 chave pequena / !1 foto: TURMA 12 · 1996 — Lá embaixo, uma chave enferrujada. E uma foto de *noventa e seis*.
4. `sala_escola` {"luz": "acesa", "texto": "TURMA 12\n1996", "relogio_hora": "19:26"} · cam pan_r  · sem personagem — Uma turma inteira na frente da sala doze. Os nomes, *riscados*.
5. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "desvio": 60} · cam zoom_rosto tensao · TEO(busto) — [TEO] Essa menina de trança... é a *Diretora Marta*!
6. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "desvio": -60} · cam in  · BENTO(busto) — [BENTO] Guarda isso. Amanhã cedo ela decide a sua *suspensão*.
7. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "seed": 4} · cam zoom_forte  · sem personagem · prop placa 'QUARTA · 07:30 · FALTAM 2 DIAS' — Quarta, sete e meia. Faltavam *dois dias* pra eu provar tudo.
8. `gabinete` {"texto": "DIRETORIA", "hora": "dia", "cor": [40, 90, 170]} · cam zoom_rosto tensao · MARTA(busto) — [MARTA] Onde vocês acharam *essa foto*?
9. `gabinete` {"texto": "DIRETORIA", "hora": "dia", "cor": [40, 90, 170]} · cam in  · TEO(busto) — [TEO] Debaixo da sala doze. A senhora estudou *lá*?
10. `gabinete` {"texto": "DIRETORIA", "hora": "dia", "cor": [40, 90, 170]} · cam zoom_rosto tensao · MARTA(busto) — [MARTA] Estudei. E no mês que vem, ela vai ser *demolida*.
11. `escuro`  · cam zoom_forte  · sem personagem · prop carta 'OFÍCIO DA ESCOLA' SALA 12: DEMOLIÇÃO / !DEZEMBRO / TURMA 12: DIVIDIDA EM 3 — Vai virar estacionamento. E a nossa turma, *dividida em três*.
12. `gabinete` {"texto": "DIRETORIA", "hora": "dia", "cor": [40, 90, 170]} · cam in  · NINA, TEO — Eu e a Nina, em salas diferentes. *Ninguém* tinha contado.
13. `gabinete` {"texto": "DIRETORIA", "hora": "dia", "cor": [40, 90, 170]} · cam zoom_rosto  · MARTA(busto) — [MARTA] Eu tentei impedir e perdi. E isso não te livra da *suspensão*, Teo.
14. `corredor_escola` {"luz": "acesa", "desvio": 140} · cam zoom_rosto tensao · NINA(busto) — [NINA] Teo... o Sombra sabia da demolição *antes da gente*.
15. `corredor_escola` {"luz": "acesa", "texto": "SAÍDA", "seed": 9} · cam out  · sem personagem · prop placa '12:20' — Meio-dia e vinte. Sinal da saída. E alguém veio *correndo*.
16. `corredor_escola` {"luz": "acesa", "desvio": -140} · cam pan_l  · CAIO, TEO — [CAIO] Sai da frente, Teo! *Tô com pressa*!
17. `corredor_escola` {"luz": "acesa", "seed": 11} · cam zoom_forte tensao · sem personagem · prop placa '★' — Eu olhei pro chão. Na sola do tênis dele: *uma estrela*.
18. `corredor_escola` {"luz": "acesa", "desvio": 100} · cam zoom_tremido tensao · TEO(busto) — [TEO] A mesma estrela. Da pegada *no escuro*.
19. `escuro`  · cam zoom_forte hook · sem personagem · prop celular '12:21 · DESCONHECIDO' Viu a estrela, né? / !Não conta pra ninguém. / Ainda. / — O SOMBRA — No mesmo segundo, meu celular vibrou. *Número desconhecido*.
20. `corredor_escola` {"luz": "acesa", "texto": "SALA 12", "desvio": -100} · cam zoom_rosto hook · TEO(busto) — Comenta PARTE CINCO pra saber se o Caio é *o Sombra*.

**Legenda:**
```
Debaixo da placa da sala 12 tinha uma foto... e a menina de trança era a diretora. 🔦

O Sombra da Sala 12 · Parte 4 — Debaixo do número 12

O Caio é o Sombra ou tá sendo usado? Teoria aqui 👇

Manda pra quem ia ficar arrasado se a turma fosse dividida 👀

A Parte 5 fica no perfil @mundoemhistorias (sai em até 24h). Segue pra não perder 🔔

#misterio #escola #historiasempartes #detetive #amizade
```


---

## Elenco e vozes (travados, sem personagem novo)

- **O Andar que Não Existe** (andar): Você `andar_voce` kokoro:pm_alex 1.04/1.0 · Médico `andar_medico` piper:faber 0.95/0.95 · Porteiro `andar_porteiro` kokoro:pm_santa 0.9/0.92. A mãe só por mensagem/câmera (sem personagem).
- **Nessa Cidade, a Sirene Toca às 18h** (cartela): Eu `protagonista` piper:cadu 1.0/1.0 · O outro eu `protagonista` escurecido piper:cadu 0.88/0.92 · Prefeito `prefeito` kokoro:pm_santa 0.92/0.9 · Policial `policial` piper:jeff 0.97/1.0.
- **O Sombra da Sala 12** (andar): Teo `andar_menino` kokoro:pm_alex 1.12/1.04 · Nina `andar_leitora` kokoro:pf_dora 1.14/1.05 · Caio `andar_rival` piper:faber 1.1/1.04 · Seu Bento `andar_zelador` kokoro:pm_santa 0.9/0.92 · Diretora Marta `andar_jornalista` kokoro:pf_dora 0.92/0.95 (Prof. Rui não aparece nesta parte).

## Cenários

- Elevador: `recepcao_hotel` (PORTARIA, noite, luz apagada depois do interfone), `elevador` (T e -1), `porao` (SUBSOLO), `corredor_predio` (luz apagada), filtro tv nas cenas da câmera/interfone.
- Sirene: `praca` (seed 7, torre com `relogio_hora` 17:59 → 18:05, `alerta` na sirene, `ceu_espelho` + neblina quando os sumidos descem), `rua_noite`, `casa` (porta azul nº 9), placas/carta do caderno.
- Sombra: `corredor_escola` (SALA 12 / SAÍDA, `desvio` variando o plano), `sala_escola` (lousa "TURMA 12 / 1996", relógio 19:26), `gabinete` (DIRETORIA, dia, bandeira azul), lista/ofício/celular.
