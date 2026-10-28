# Controle de qualidade — 01-proibido-dancar

Render: `renders/proibido-dancar.mp4` — 1080×1920, 30 fps, 38,5 s, 43,7 MB, renderizado em 18 min (GPU por software). Áudio medido (não ouvido): −16,6 LUFS integrado, pico −2,1 dBFS.

| Pergunta | Resultado | Evidência |
|---|---|---|
| O início desperta curiosidade? | Sim | Quadro 0 já tem a placa "PROIBIDO DANÇAR" e o Bolt balançando a cabeça |
| A história é compreensível sem explicação? | Sim | Sem fala; regra → transgressão → flagra → placa revela "MAL" |
| Cada cena faz a narrativa avançar? | Sim | 13 planos, cada um com nova informação (ver CENAS.md) |
| Personagens visualmente consistentes? | Sim | Mesmo modelo glTF e cores fixas por material em todos os quadros |
| Expressões e movimentos naturais? | Parcial | Animações do modelo são boas; o chefe desliza um pouco ao andar (velocidade fixa vs. passada) |
| Deformações, duplicações, erros de continuidade? | Não encontrados | Snapshots em 0,5–37,8 s revisados; a tábua aparece até 29,4 s; neon invisível até 36,2 s |
| Câmera ajuda a contar a história? | Sim | Push-in no gancho, contra-plongée na ameaça, ombro no cara a cara, inserto na revelação |
| Áudio sincronizado? | Sim (medido) | Danças em múltiplos da batida (144 BPM); SFX com pico 1 quadro depois da imagem |
| Legendas corretas? | N/A | Não há fala; textos estão no cenário |
| Enquadramento vertical funciona? | Sim | Assuntos centrados; nenhum texto essencial abaixo de 1330 px |
| O final entrega recompensa? | Sim | Reviravolta "MAL" + gancho "PROIBIDO PARAR" para o ep. 2 |
| Há momentos desnecessários? | Leve | Plano 4 (desconfiança, 2,6 s) poderia cair para 2 s numa versão mais curta |
| Exportação no formato pedido? | Sim | 9:16, 30–40 s |

## Limitações conhecidas
- Trilha sintetizada em código (não há banco de música acessível neste ambiente): substitua por uma faixa real a 144 BPM, ou ajuste `BEAT` em `cena.js`.
- Iluminação de festa deixa o laranja do Bolt acinzentado em alguns quadros; o foco quente no final compensa.
- O "verificador" do HyperFrames não enxerga o canvas 3D (por isso o `data-hold`); a revisão visual foi feita por snapshots.
