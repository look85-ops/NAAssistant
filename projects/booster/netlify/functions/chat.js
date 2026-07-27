const KEY = process.env.OPENROUTER_KEY; // Set in Netlify env vars

export async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }
  try {
    if (!KEY) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Missing OPENROUTER_KEY env variable' }) };
    }
    const body = JSON.parse(event.body || '{}');
    const messages = body.messages || [];

    const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': process.env.DEPLOY_URL || 'http://localhost',
        'X-Title': 'Methodist Booster'
      },
      body: JSON.stringify({ model: 'openai/gpt-4o-mini', messages })
    });

    const data = await res.json();
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: e.message }) };
  }
}
