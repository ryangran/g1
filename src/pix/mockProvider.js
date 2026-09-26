/**
 * Provedor PIX de MOCK (desenvolvimento/testes).
 *
 * Simula o ciclo de vida de uma cobranca PIX SEM se conectar a nenhum banco:
 * - createCharge: gera uma cobranca "pending" com um QR Code de exemplo.
 * - getCharge: apos alguns segundos, marca a cobranca como "paid" para voce
 *   conseguir testar a tela de confirmacao ponta a ponta.
 *
 * NAO usar em producao. Troque por um provedor real via PIX_PROVIDER.
 */

import crypto from 'node:crypto';

/** Segundos ate o mock considerar a cobranca "paga" automaticamente. */
const AUTO_PAY_AFTER_SECONDS = 8;

export class MockPixProvider {
  constructor() {
    /** @type {Map<string, any>} */
    this.charges = new Map();
  }

  async createCharge(input) {
    const id = 'mock_' + crypto.randomUUID();
    const now = Date.now();
    // Payload "copia e cola" apenas ilustrativo (nao e um BR Code valido).
    const qrCode = `00020126MOCK-${id}-${input.amountCents}5204000053039865802BR6009SAO PAULO62070503***6304MOCK`;

    const charge = {
      id,
      status: 'pending',
      qrCode,
      qrCodeImage: undefined,
      amountCents: input.amountCents,
      description: input.description,
      payer: input.payer,
      createdAtMs: now,
      expiresAt: new Date(now + 30 * 60 * 1000).toISOString(),
    };

    this.charges.set(id, charge);
    return this._public(charge);
  }

  async getCharge(chargeId) {
    const charge = this.charges.get(chargeId);
    if (!charge) {
      throw new Error(`Cobranca nao encontrada: ${chargeId}`);
    }
    // Simula a confirmacao do pagamento passado o tempo configurado.
    if (
      charge.status === 'pending' &&
      Date.now() - charge.createdAtMs >= AUTO_PAY_AFTER_SECONDS * 1000
    ) {
      charge.status = 'paid';
    }
    return this._public(charge);
  }

  async parseWebhook(rawBody) {
    const body = JSON.parse(rawBody || '{}');
    return { chargeId: body.chargeId, status: body.status || 'paid' };
  }

  _public(charge) {
    return {
      id: charge.id,
      status: charge.status,
      qrCode: charge.qrCode,
      qrCodeImage: charge.qrCodeImage,
      amountCents: charge.amountCents,
      expiresAt: charge.expiresAt,
    };
  }
}
