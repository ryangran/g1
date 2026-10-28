# Bíblia visual — 03-vagalume-apagao ("Apagão")

**Ideia central:** um vagalume minúsculo só quer apagar a luz para dormir. Cada tentativa apaga algo 10 vezes maior, até a cidade e o céu ficarem no escuro. A única luz que sobra é a dele.

## Personagem

### Lumi — vagalume (protagonista único)
- **Função:** quer dormir. É o causador involuntário do apagão.
- **Tamanho real:** 1,2 cm. A câmera sempre está na escala dele (macro) nas cenas internas.
- **Idade aparente:** adulto jovem, rabugento de sono.
- **Silhueta:** cabeça grande e redonda (40% do corpo), tórax curto, abdômen em gota que brilha. Seis patinhas finas: anda nas 4 de trás e gesticula com as 2 da frente como braços. Duas antenas longas em curva com uma bolinha na ponta.
- **Rosto e olhos:** olhos enormes e ovais (cada um com ~30% da largura da cabeça), íris âmbar `#f2a93b`, pupila grande preta com 2 brilhos. Pálpebras pesadas (sonolento). Boca larga, sem dentes visíveis, exceto no grito.
- **Cores e materiais:** corpo marrom-chocolate `#4a2f22` com leve brilho de quitina (roughness 0,35). Asas translúcidas, iridescentes, recolhidas em "capa" nas costas. Abdômen: vidro leitoso amarelo-esverdeado `#d8ff5a` com subsurface. Quando acende, emite `#e9ff7a` e ilumina o ambiente ao redor (raio ~10 cm).
- **Figurino:** pijama de flanela azul-marinho `#24386b` com estrelinhas amarelas `#ffd34d`, touca de dormir combinando com pompom amarelo. O pijama **não cobre o abdômen**: o brilho escapa por baixo da barra.
- **Personalidade e movimento:** dramático e impaciente. Movimentos curtos e rápidos, com antecipação exagerada (encolhe antes de chutar). Quando voa, as asas fazem um borrão e o corpo balança como um balão.
- **Expressões:** (1) olho semicerrado irritado, com uma sobrancelha-antena caída; (2) esforço, com bochechas infladas, olhos fechados com força e antenas tremendo; (3) triunfo, com sorriso enorme e braços para o alto; (4) horror, com pupilas encolhidas a pontinhos, boca em "O" e antenas eriçadas; (5) percepção, com olhar parado, pálpebras a meio mastro e um piscar lento; (6) vergonha, com sorriso amarelo, ombros encolhidos e antenas murchas.
- **Voz:** sem fala, só grunhidos curtos (esforço "nnnngh!", "hmpf", um "ops" mínimo).
- **Desejo:** dormir. **Medo:** passar a noite em claro. **Conflito:** a luz (ele mesmo).

## Cenários

1. **Criado-mudo (escala inseto):** madeira escura envernizada. A cama de Lumi é uma caixa de fósforos aberta, com uma meia listrada como cobertor e uma tampinha de garrafa como travesseiro. Ao lado, um **abajur de mesa gigante** (para ele, do tamanho de um prédio): base metálica redonda com **botão de pressão** vermelho, cúpula de tecido creme, luz quente `#ffd9a0`. O fio sai pelo fundo, vai até a parede e entra numa **régua de tomadas** com 4 plugues.
2. **Apartamento:** sala vista da porta do quarto: TV ligada, aquário com bomba e luz azul, geladeira na cozinha americana e **quadro de disjuntores** perto da porta.
3. **Prédio:** edifício residencial de 14 andares, fachada de concreto claro e janelas com luzes quentes variadas, na rua de uma metrópole brasileira genérica (sem marcos reais reconhecíveis).
4. **Cidade:** vista aérea noturna com grade de ruas, avenidas com faróis, torres com luz vermelha no topo e um outdoor luminoso. O horizonte termina em morros.
5. **Céu:** céu limpo cheio de estrelas e lua cheia grande.

## Paleta
Noite `#0b1022` · madeira `#3a2418` · luz quente do abajur `#ffd9a0` · brilho do Lumi `#e9ff7a` · pijama `#24386b` + `#ffd34d` · faíscas `#9fe7ff` · janelas `#ffb85c` / `#fff1c9` · cidade apagada `#05060c`.

## Iluminação (continuidade)
- Interior: o abajur é a luz-chave, quente, vinda da esquerda do quadro. Um contra azul frio entra pela janela. Quando o abajur apaga, a única chave passa a ser a faísca azul e depois o brilho do Lumi.
- Exterior: luz das janelas e postes. Cada apagão tira uma camada de luz, de baixo para cima na escala: janela → prédio → bairros → estrelas → lua.
- **Regra de ouro:** em todo plano interno, existe uma **luz amarelo-esverdeada fraca vindo de baixo do cobertor do Lumi**. Ela é o plant da reviravolta.

## Direção de arte
Animação 3D estilizada de longa-metragem: materiais macios, subsurface na quitina e no abdômen, profundidade de campo de lente macro com bokeh redondo nas cenas internas, e cores saturadas sobre um escuro profundo. Escala sempre explícita: objetos humanos gigantes em volta do Lumi.

## Câmera
- Interior: lente macro (equivalente a 100 mm), altura do Lumi, profundidade de campo curta, câmera na mão leve.
- Exterior: grande-angular (24 mm) para o prédio e drone (35 mm, muito alto) para a cidade.
- Movimentos permitidos: push-in (tensão), recuo/zoom-out (escalada), tilt-up (do prédio ao céu), whip-pan (transições de escala).

## Regras de continuidade
1. Lumi tem sempre o mesmo pijama, touca, olhos âmbar e o abdômen visível sob a barra do pijama.
2. O abajur fica à esquerda da cama; o fio sempre corre para a direita, até a régua.
3. O brilho do abdômen fica fraco (encoberto) até a cena 8 e nunca some.
4. A ordem do apagão nunca volta: o que apagou continua apagado.
5. Nenhuma pessoa aparece em quadro, só os objetos e a cidade.

## Referências reutilizáveis
- **Folha do personagem** (frente, perfil, costas, 3/4 e as 6 expressões), gerada primeiro e usada como imagem de referência em todas as cenas. Prompt em `CENAS.md`, seção 0.
- **Quadro final de cada cena** vira o **quadro inicial** da seguinte (ver `MONTAGEM.md`).
- Seed fixa por ferramenta, anotada em `MONTAGEM.md` na primeira geração aprovada.
