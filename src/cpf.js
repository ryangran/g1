/**
 * Validacao de CPF: confere APENAS os digitos verificadores (algoritmo oficial).
 * Nao consulta nenhuma base externa nem retorna dados da pessoa.
 * Serve so para evitar que o pagador digite um CPF invalido no formulario.
 */
export function isValidCPF(value) {
  const cpf = String(value || '').replace(/\D/g, '');
  if (cpf.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(cpf)) return false; // rejeita 000..., 111..., etc.

  const digits = cpf.split('').map(Number);

  const calcCheckDigit = (len) => {
    let sum = 0;
    for (let i = 0; i < len; i++) {
      sum += digits[i] * (len + 1 - i);
    }
    const rest = (sum * 10) % 11;
    return rest === 10 ? 0 : rest;
  };

  return calcCheckDigit(9) === digits[9] && calcCheckDigit(10) === digits[10];
}
