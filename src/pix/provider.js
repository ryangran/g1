/**
 * Interface (contrato) que todo provedor de PIX deve implementar.
 *
 * O checkout inteiro (frontend + rotas do servidor) so conhece esta interface.
 * Para plugar o SEU provedor, crie um arquivo novo (ex: src/pix/meuProvider.js)
 * que implemente os 3 metodos abaixo e registre-o em `createProvider()`.
 *
 * Nenhum metodo aqui consulta dados pessoais a partir do CPF: o CPF do pagador
 * so e usado como dado de cobranca, como a propria API de PIX exige.
 */

/**
 * @typedef {Object} CreateChargeInput
 * @property {number} amountCents  Valor em centavos (ex: 4990 = R$ 49,90).
 * @property {string} description  Descricao curta do que esta sendo cobrado.
 * @property {Object} payer
 * @property {string} payer.name   Nome do pagador.
 * @property {string} payer.email  Email do pagador.
 * @property {string} payer.cpf    CPF do pagador (somente digitos), exigido pela cobranca PIX.
 */

/**
 * @typedef {Object} Charge
 * @property {string} id            Id da cobranca no provedor.
 * @property {'pending'|'paid'|'expired'|'canceled'} status
 * @property {string} qrCode        Payload "copia e cola" do PIX (BR Code / EMV).
 * @property {string} [qrCodeImage] Data URL (base64) da imagem do QR Code, se houver.
 * @property {number} amountCents
 * @property {string} [expiresAt]   ISO timestamp de expiracao, se houver.
 */

/**
 * Contrato do provedor de PIX.
 * @typedef {Object} PixProvider
 * @property {(input: CreateChargeInput) => Promise<Charge>} createCharge
 * @property {(chargeId: string) => Promise<Charge>} getCharge
 * @property {(rawBody: string, headers: Record<string,string>) => Promise<{chargeId: string, status: Charge['status']}>} parseWebhook
 */

import { MockPixProvider } from './mockProvider.js';

/**
 * Fabrica de provedor. Escolhe a implementacao pela env PIX_PROVIDER.
 * @returns {PixProvider}
 */
export function createProvider() {
  const name = (process.env.PIX_PROVIDER || 'mock').toLowerCase();

  switch (name) {
    case 'mock':
      return new MockPixProvider();

    // Quando voce me mandar a documentacao da sua API, crie
    // src/pix/meuProvider.js exportando uma classe que implemente a
    // interface acima e adicione o case aqui:
    //
    // case 'meu':
    //   return new MeuPixProvider({
    //     baseUrl: process.env.PIX_API_URL,
    //     apiKey: process.env.PIX_API_KEY,
    //   });

    default:
      throw new Error(`PIX_PROVIDER desconhecido: "${name}"`);
  }
}
