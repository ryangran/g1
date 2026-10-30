# O BILHETE — Bíblia da série

**Conceito:** um taxista de madrugada acha no banco de trás um bilhete premiado de R$ 40 milhões. Todo dia sai uma parte, e os comentários decidem o que o Clóvis faz.
**Tudo é ficção:** os nomes, a cidade, a loteria e as regras. Nenhuma lei real.
**Bordão da série:** *"Todo prêmio tem dono."*

## Painel fixo (topo da tela, o episódio todo)
`NO BANCO DE TRÁS R$ 40.000.000` · `NO BOLSO R$ 0` · `RISCO 0%`
- O risco sobe com cada problema da parte (com "+N%" piscando em vermelho).
- Quando o bilhete muda de lugar, o primeiro campo muda junto (ex.: "NO PORTA-LUVAS").

## O Código da Madrugada (regras do mundo da série, numeradas e acumuladas)
Uma regra por parte, no cartão preto. As anteriores aparecem riscadas em cinza acima.
1. **Todo bilhete tem dois donos: quem comprou… e quem tá com ele.**

## Visual oficial do Clóvis (definitivo)
- **Referências:** `docs/clovis-folha.jpg` (frente, 3/4, lado, rostos, táxi) e `docs/clovis-poses.webp` (dirigindo, retrovisor, susto suando, segurando o bilhete, telefone, correndo).
- **Banco de poses recortadas:** `assets/clovis/*.png`, gerado por `tools/recortar_clovis.py`. Cada pose tem uma versão `-noite` já com a cor da madrugada. As cenas usam `pose()` em `tools/cenas.py`.
- Pose nova: peça ao Gemini **no mesmo chat da folha**, com fundo cinza liso e sem texto, e acrescente a caixa de recorte em `recortar_clovis.py`.
- O desenho vetorial antigo do Clóvis não é mais usado.

## Personagens (descrição definitiva: copie igual em todo prompt)

### Clóvis Ferreira — protagonista
- 52 anos, taxista há 22, sempre no turno da madrugada. Pai de uma filha adolescente (Bia, citada, ainda não aparece). A parcela do táxi está atrasada há 3 meses.
- **Visual:** brasileiro, pele morena clara, cabelo preto curto com as têmporas grisalhas, **bigode grosso grisalho**, olheiras, sobrancelhas grossas.
- **Roupa fixa:** camisa social **azul-clara de manga curta** com uma caneta no bolso, calça escura, relógio simples de pulseira de couro marrom.
- **Objetos:** **terço de madeira pendurado no retrovisor** e uma foto 3×4 da filha presa no painel.
- **Táxi:** sedã **branco**, luminoso vermelho "TÁXI" no teto, placa final **7**, banco de trás de tecido cinza.
- **Jeito:** calmo, honesto, cansado. Fala pouco. Coça o bigode quando está nervoso.

### O homem de terno — antagonista da Parte 1 (nome ainda desconhecido)
- Uns 35 anos, cabelo preto penteado para trás com gel, barba feita.
- **Terno azul-marinho amassado**, sem gravata, camisa branca aberta no colarinho, **relógio dourado grande**.
- Sorriso educado que não chega aos olhos. Fala ao telefone o tempo todo.

### Seu Antônio — o dono do nome no bilhete (aparece depois)
- 78 anos, magro, boné bege, cardigã marrom, óculos grossos. Mora na **Rua das Acácias, 51** (endereço do recibo de farmácia, o 3º jeito).

## Cenário
- Uma metrópole brasileira fictícia, de madrugada, depois da chuva: asfalto molhado refletindo neon vermelho e verde, postes de luz laranja.
- **Hotel Imperial:** fachada iluminada com toldo vinho e porteiro de uniforme.

## Direção de arte
- **Estilo:** ilustração de graphic novel com **contorno preto grosso**, cel shading e cores saturadas. Luz noturna dramática: laranja dos postes, verde do painel, vermelho do luminoso.
- **Paleta:** azul-noite `#0e1726`, laranja de poste `#f29b38`, verde de painel `#38e08a`, vermelho do luminoso `#e23b2e`, branco do táxi.
- **Câmera:** muito close (mãos, rosto, retrovisor) e planos de dentro do carro. O retrovisor e o espelho lateral são "telas" da história.
- **Sem texto nas imagens.** Os textos (painel, legendas, cartões) entram na montagem.

## Continuidade
- A camisa azul-clara, o bigode grisalho e o terço no retrovisor aparecem **em toda cena** com o Clóvis.
- O bilhete é **amarelo-claro com números em preto**. Os 6 números ficam circulados com caneta vermelha **só a partir da cena do celular**.
- Na Parte 1 o táxi está parado em frente ao Hotel Imperial, com o hotel atrás e à direita do carro.
