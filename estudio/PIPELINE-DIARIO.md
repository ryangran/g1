# O Bilhete — pipeline diário (automático)

Pedido do dono do perfil (03/11): **quando a votação fechar, já gerar o próximo vídeo e programar tudo**, sem esperar aprovação.
Horários (Brasília): votação fecha **15h** · leitura às **15h05** · publicação às **19h00** · comentário logo depois.

## Passo a passo (episódio N → N+1)
1. **Ler a votação** (respostas contam; o próprio perfil não vota):
   `python3 estudio/tools/comentarios.py --instagram --link <reel N> --opcoes A,B --jeito <palavras do 3º jeito> --fecha <hoje>T15:00:00-03:00 --saida estudio/producoes/<pasta N>/build/votacao.json`
   Empate ou zero votos: escolher o ramo que rende a melhor história e dizer isso ao usuário.
2. **Métricas** de todos os Reels (views, alcance, tempo médio) → anotar no relatório ao usuário. Nunca inventar números.
3. **Roteiro N+1** no ramo vencedor (~40–45 s, 10–12 frases):
   - 1ª frase entendível por quem nunca viu a série (gancho em 2 s);
   - 2ª frase: recap de 1 linha + cartão "PARTE N · VOCÊS DECIDIRAM";
   - virada; duas opções de **uma palavra**; 3º jeito escondido na cena (o atendente/o vídeo do posto é o fio da série);
   - última frase: "Hoje só vale X ou Y. A maioria escreve a parte N+2 amanhã."
   - Continuidade: docs/BIBLIA.md do episódio 06 (Clóvis oficial = poses em assets/clovis/*-noite.png; Seu Antônio 78 anos, boné bege, cardigã marrom, óculos grossos).
4. **Produção**: copiar a pasta do episódio anterior (assets, capa, tools, meta.json, hyperframes.json, package.json) para `estudio/producoes/NN-o-bilhete-pXX/`, trocar FRASES em tools/narracao_google.py (voz Orus, nunca outra), criar tools/cenasX.py com as cenas novas, ajustar PLANOS/cartões/selos em tools/montar.py.
   `python3 tools/narracao_google.py && python3 tools/montar.py && hyperframes check` (0 erros) → `hyperframes snapshot` e olhar → render **com Bash run_in_background** (render em subshell com & morre).
5. **Capa** (capa/index.html, sem spoiler do 3º jeito), **legenda** e **comentário** em docs/.
6. **Hospedar** mp4 + capa em /tmp/claude-0/vc/obilhete/assets/reel/ e `vercel deploy --prod --yes`; conferir 200.
7. **Publicar às 19h00**: espera até 21:59 UTC e roda
   `python3 estudio/tools/publicar_reel.py https://obilhete.vercel.app/assets/reel/parteN.mp4 --legenda … --capa … --comentario …`
8. **Site**: site/serie.js (reelAtual, decisão da parte anterior, nova parte, votação), Vercel `VOTO_OPCOES` e `VOTO_FECHA` (amanhã 15h), tirar o mp4 do site, redeploy, conferir /api/votos.
9. **Agendar** a leitura de amanhã 15h05 (send_later) com estas mesmas instruções, commit + push na branch.
10. Avisar o usuário: link do Reel, placar, números, e lembrar de **fixar o comentário** (a API não fixa).

Ferramentas (container): HyperFrames CLI em /tmp/claude-0/hf, faster-whisper em /tmp/claude-0/kvenv, Vercel CLI em /tmp/claude-0/vc (pasta de deploy /tmp/claude-0/vc/obilhete).
Se o container foi recriado e alguma ferramenta sumiu, reinstalar antes (ver estudio/RECURSOS.md) e avisar o usuário se a publicação atrasar.
