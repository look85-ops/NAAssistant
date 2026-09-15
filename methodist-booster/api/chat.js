export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const KEY = process.env.OPENROUTER_KEY;
  try {
    if (!KEY) {
      return res.status(500).json({ error: 'Missing OPENROUTER_KEY env variable' });
    }
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const messages = body.messages || [];

    const r = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://vercel.app',
        'X-Title': 'Methodist Booster'
      },
      body: JSON.stringify({ model: 'openai/gpt-4o-mini', messages })
    });

    const data = await r.json();
    return res.status(200).json(data);
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}