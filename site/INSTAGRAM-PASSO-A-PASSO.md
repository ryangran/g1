# Ligar a votação ao vivo (comentários do Instagram → site)

Você faz isto uma vez, em uns 10 minutos, no computador. É grátis. A sua conta precisa ser profissional (Criador ou Comercial).

> Os nomes dos botões na Meta mudam de vez em quando. Se algum não bater, procure o mais parecido ou me mande um print.

## 1. Criar o app
1. Entre em **https://developers.facebook.com/apps** com a sua conta do Facebook. Na primeira vez, ele pede para "Começar" como desenvolvedor: aceite.
2. Clique em **Criar app**.
3. Nome: algo como `Votacao Serie`. Caso de uso: **Outro**. Tipo: **Empresa** (Business).
4. No painel do app, em **Adicionar produtos**, ache **Instagram** e clique em **Configurar**.

## 2. Gerar o token
1. Dentro de Instagram, abra **Configuração da API com login do Instagram** (API setup with Instagram login).
2. Na etapa **Gerar tokens de acesso**, clique em **Adicionar conta** e entre com o seu Instagram da série.
   Se ele pedir para adicionar a conta como **testador**, faça isso. Depois, no app do Instagram, vá em **Configurações → Apps e sites → Convites de testador** e aceite.
3. Clique em **Gerar token** ao lado da conta e autorize as permissões. Elas precisam incluir **ler comentários** (`instagram_business_basic` e `instagram_business_manage_comments`).
4. Copie o token. É um texto longo que começa com `IG…`. **Não mande esse token no chat.**

## 3. Colocar na Vercel
1. No projeto do site na Vercel, vá em **Settings → Environment Variables**.
2. Adicione as variáveis abaixo e depois clique em **Redeploy**:

| Nome | Valor | Obrigatória |
|---|---|---|
| `IG_TOKEN` | o token copiado | sim |
| `VOTO_OPCOES` | as palavras da votação, separadas por vírgula. Ex.: `CIPÓ,PEDRA` | sim |
| `VOTO_FECHA` | quando a votação fecha. Ex.: `2026-10-30T15:00:00-03:00` | não |
| `IG_MEDIA_ID` | id do Reel. Sem isso, o site usa **o post mais recente** | não |

A cada parte nova, troque `VOTO_OPCOES` e `VOTO_FECHA` (e `votacao` no `serie.js`). Depois, redeploy.

## Como a contagem funciona
- O site consulta os comentários **no máximo 1 vez por minuto** (cache da Vercel), e o placar se atualiza sozinho na tela a cada 30 s.
- **Um voto por pessoa:** vale o último comentário feito antes do fechamento.
- O comentário precisa citar **uma** das opções. Acento e maiúsculas não importam: "cipo", "CIPÓ" e "Cipó!!" valem igual. Quem escreve as duas opções juntas não conta.
- Os outros comentários (palpites do 3º jeito, conversa) aparecem num contador separado.
- Enquanto não houver token, o placar mostra **"DADOS DE TESTE"**.

## O token vence
O token dura cerca de **60 dias**. Perto disso, gere um novo (passo 2.3) e troque o `IG_TOKEN` na Vercel.
Se ele vencer, o placar some do site, mas nada mais quebra.
