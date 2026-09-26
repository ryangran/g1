const el = (id) => document.getElementById(id);

const state = { chargeId: null, poll: null };

// Formata centavos como "R$ 49,90".
function formatBRL(cents) {
  return (cents / 100).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });
}

// Mascara simples de CPF enquanto digita.
el('cpf').addEventListener('input', (e) => {
  let v = e.target.value.replace(/\D/g, '').slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
  v = v.replace(/(\d{3})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3-$4');
  e.target.value = v;
});

// Carrega nome e preco do produto.
async function loadProduct() {
  try {
    const res = await fetch('/api/product');
    const p = await res.json();
    el('product-name').textContent = p.name;
    el('product-price').textContent = formatBRL(p.amountCents);
  } catch {
    el('product-name').textContent = 'Programa Livre de Apostas';
  }
}

function showStep(step) {
  el('step-form').hidden = step !== 'form';
  el('step-pix').hidden = step !== 'pix';
  el('step-done').hidden = step !== 'done';
}

function renderQrCode(payload) {
  const box = el('qrcode');
  box.innerHTML = '';
  // qrcodejs (global QRCode) desenha o BR Code "copia e cola" como imagem.
  new QRCode(box, {
    text: payload,
    width: 220,
    height: 220,
    correctLevel: QRCode.CorrectLevel.M,
  });
  el('pix-code').value = payload;
}

// Consulta o status da cobranca a cada 3s ate ser paga/expirada.
function startPolling() {
  clearInterval(state.poll);
  state.poll = setInterval(async () => {
    if (!state.chargeId) return;
    try {
      const res = await fetch(`/api/charges/${state.chargeId}`);
      const charge = await res.json();
      if (charge.status === 'paid') {
        clearInterval(state.poll);
        showStep('done');
      } else if (charge.status === 'expired' || charge.status === 'canceled') {
        clearInterval(state.poll);
        el('pix-status').innerHTML =
          'A cobrança expirou. Recarregue a página para gerar outra.';
      }
    } catch {
      /* tenta de novo no proximo tick */
    }
  }, 3000);
}

el('checkout-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = el('pay-btn');
  const errEl = el('form-error');
  errEl.hidden = true;
  btn.disabled = true;
  btn.textContent = 'Gerando PIX…';

  try {
    const res = await fetch('/api/charges', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: el('name').value,
        email: el('email').value,
        cpf: el('cpf').value,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erro ao gerar a cobrança.');

    state.chargeId = data.id;
    renderQrCode(data.qrCode);
    el('pix-amount').textContent = formatBRL(data.amountCents);
    showStep('pix');
    startPolling();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.hidden = false;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Gerar PIX e pagar';
  }
});

el('copy-btn').addEventListener('click', async () => {
  const code = el('pix-code').value;
  try {
    await navigator.clipboard.writeText(code);
    el('copy-btn').textContent = 'Copiado!';
    setTimeout(() => (el('copy-btn').textContent = 'Copiar'), 1500);
  } catch {
    el('pix-code').select();
    document.execCommand('copy');
  }
});

loadProduct();
