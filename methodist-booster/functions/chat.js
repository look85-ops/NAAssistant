export async function onRequestPost(context) {
  const KEY = context.env.OPENROUTER_KEY;
  try {
    if (!KEY) {
      return Response.json({ error: 'Missing OPENROUTER_KEY env variable' }, { status: 500 });
    }
    const body = await context.request.json();
    const messages = body.messages || [];

    const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': context.request.headers.get('origin') || 'https://look85-ops.github.io',
        'X-Title': 'Methodist Booster'
      },
      body: JSON.stringify({ model: 'openai/gpt-4o-mini', messages })
    });

    const data = await res.json();
    return Response.json(data);
  } catch (e) {
    return Response.json({ error: e.message }, { status: 500 });
  }
}