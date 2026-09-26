/**
 * Adaptador do NOMAPAY Gateway (https://nomaofficial.com.br/api/v1)
 * para a interface PixProvider usada pelo checkout.
 *
 * Implementa createCharge / getCharge / parseWebhook conforme a doc oficial.
 * Valores monetarios sao inteiros em centavos, como a API exige.
 */

import crypto from 'node:crypto';

const DEFAULT_BASE_URL = 'https://nomaofficial.com.br/api/v1';

// Normaliza o status do gateway para o vocabulario da interface.
function mapStatus(raw) {
  switch (String(raw || '').toUpperCase()) {
    case 'PAID':
      return 'paid';
    case 'WAITING_PAYMENT':
    case 'PROCESSING':
    case 'PENDING':
      return 'pending';
    case 'EXPIRED':
      return 'expired';
    case 'FAILED':
    case 'REFUSED':
    case 'CANCELED':
    case 'CANCELLED':
      return 'canceled';
    default:
      return 'pending';
  }
}

export class NomapayPixProvider {
  /**
   * @param {Object} opts
   * @param {string} opts.publicKey   fsp_pk_live_...
   * @param {string} opts.secretKey   fsp_sk_live_...
   * @param {string} [opts.baseUrl]
   * @param {string} [opts.webhookSecret] Segredo para validar HMAC do webhook.
   * @param {string} [opts.postbackUrl]   URL que o gateway chama nos eventos.
   */
  constructor({ publicKey, secretKey, baseUrl, webhookSecret, postbackUrl }) {
    if (!publicKey || !secretKey) {
      throw new Error('NOMAPAY: defina NOMAPAY_PUBLIC_KEY e NOMAPAY_SECRET_KEY.');
    }
    this.baseUrl = (baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '');
    this.webhookSecret = webhookSecret || secretKey;
    this.postbackUrl = postbackUrl;
    this.authHeader =
      'Basic ' + Buffer.from(`${publicKey}:${secretKey}`).toString('base64');
  }

  async _request(method, path, body, extraHeaders = {}) {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: {
        Authorization: this.authHeader,
        'Content-Type': 'application/json',
        ...extraHeaders,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    const text = await res.text();
    let data;
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { raw: text };
    }

    if (!res.ok) {
      const msg = data?.message || data?.error || `HTTP ${res.status}`;
      throw new Error(`NOMAPAY ${method} ${path} falhou: ${msg}`);
    }
    return data;
  }

  async createCharge(input) {
    const payload = {
      amount: input.amountCents,
      payment_method: 'PIX',
      customer: {
        name: input.payer.name,
        email: input.payer.email,
        phone: input.payer.phone || '11999999999',
        document: {
          number: String(input.payer.cpf).replace(/\D/g, ''),
          type: 'CPF',
        },
      },
      items: [
        {
          title: input.description,
          unit_price: input.amountCents,
          quantity: 1,
          tangible: false,
        },
      ],
    };
    if (this.postbackUrl) payload.postback_url = this.postbackUrl;

    const data = await this._request('POST', '/transactions', payload, {
      // Previne cobrancas duplicadas em caso de retry.
      'x-idempotency-key': crypto.randomUUID(),
    });

    const pix = data.pix || {};
    return {
      id: data.id || data.transaction_id,
      status: mapStatus(data.status),
      qrCode: pix.copy_paste || data.pix_copy_paste,
      qrCodeImage: pix.qr_code || data.pix_qr_code,
      amountCents: data.amount ?? input.amountCents,
      expiresAt: pix.expires_at,
    };
  }

  async getCharge(chargeId) {
    const res = await this._request('GET', `/transactions/${chargeId}`);
    const data = res.data || res; // a doc envelopa em { data: {...} }
    const pix = data.pix || {};
    return {
      id: data.id || chargeId,
      status: mapStatus(data.status),
      qrCode: pix.copy_paste || data.pix_copy_paste,
      qrCodeImage: pix.qr_code || data.pix_qr_code,
      amountCents: data.amount,
      expiresAt: pix.expires_at,
    };
  }

  /**
   * Valida a assinatura HMAC SHA-256 do webhook e extrai id + status.
   * Header: x-nomapay-signature: sha256={hex}
   */
  async parseWebhook(rawBody, headers = {}) {
    const sigHeader =
      headers['x-nomapay-signature'] || headers['X-Nomapay-Signature'] || '';
    const received = String(sigHeader).replace(/^sha256=/, '').trim();

    const expected = crypto
      .createHmac('sha256', this.webhookSecret)
      .update(rawBody, 'utf8')
      .digest('hex');

    const ok =
      received.length === expected.length &&
      crypto.timingSafeEqual(
        Buffer.from(received, 'hex'),
        Buffer.from(expected, 'hex')
      );

    if (!ok) {
      throw new Error('NOMAPAY: assinatura de webhook invalida.');
    }

    const body = JSON.parse(rawBody || '{}');
    const event = body.event || body.type || '';
    const obj = body.data || body.transaction || body;
    const chargeId = obj.id || obj.transaction_id;

    // Deriva o status do evento; cai para o campo status quando presente.
    let status;
    if (/paid$/i.test(event)) status = 'paid';
    else if (/failed$/i.test(event)) status = 'canceled';
    else if (/created$/i.test(event)) status = 'pending';
    else status = mapStatus(obj.status);

    return { chargeId, status };
  }
}
