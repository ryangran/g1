# Voz fixa do estúdio

Todas as narrações usam **a mesma voz**, para o perfil ter identidade sonora.

- **Motor:** Google Gemini TTS, modelo `gemini-2.5-flash-preview-tts`. Funciona no nível gratuito da chave; o modelo `pro` dá erro 429.
- **Voz:** `Orus`
- **Instrução de estilo:** o texto exato fica em `estudio/VOZ-ESTILO.txt`. Não mude esse arquivo entre episódios.
- **Como gerar:** o roteiro inteiro sai numa chamada só (mesmo tom do começo ao fim). Depois:
  - as pausas longas são encurtadas para 0,38 s;
  - o whisper (`hyperframes transcribe -m small -l pt`) mede o tempo de cada palavra para as legendas.
- **Modelo do fluxo:** `producoes/05-macaco-selva/tools/narracao_google.py`. Copie para o episódio novo e troque só a lista `FRASES`.
- O nível gratuito tem limite diário de chamadas. Gere a narração **só quando o roteiro estiver fechado**.
- A Kokoro (pm_alex) fica apenas como rascunho ou animatic. Ela é robótica demais para publicar.
