import fetch from 'node-fetch';

export const handler = async (event) => {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ error: 'OPENROUTER_API_KEY is not set' }) };
  }
  const baseUrl = process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';

  try {
    const body = event.body ? JSON.parse(event.body) : {};
    const message = body.message;
    const messages = body.messages;
    const model = body.model || 'deepseek/deepseek-chat';

    const payload = {
      model,
      messages: messages || [{ role: 'user', content: String(message || '') }]
    };

    const resp = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json; charset=utf-8'
      },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const text = await resp.text();
      return { statusCode: 502, body: JSON.stringify({ error: 'upstream_error', status: resp.status, body: text }) };
    }
    const data = await resp.json();
    const out = data?.choices?.[0]?.message?.content || '';
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ model, output: out, raw: data })
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: 'internal_error', detail: String(e) }) };
  }
};
