export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok', service: 'bot-mvp' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
      });
    }

    if (url.pathname === '/chat' && request.method === 'POST') {
      const apiKey = env.OPENROUTER_API_KEY;
      if (!apiKey) {
        return new Response(JSON.stringify({ error: 'OPENROUTER_API_KEY is not set' }), { status: 500 });
      }
      const baseUrl = env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';

      try {
        const body = await request.json();
        const model = body?.model || 'deepseek/deepseek-chat';
        const messages = body?.messages || [{ role: 'user', content: String(body?.message || '') }];

        const upstream = await fetch(`${baseUrl}/chat/completions`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json; charset=utf-8'
          },
          body: JSON.stringify({ model, messages })
        });
        if (!upstream.ok) {
          const txt = await upstream.text();
          return new Response(JSON.stringify({ error: 'upstream_error', status: upstream.status, body: txt }), { status: 502 });
        }
        const data = await upstream.json();
        const out = data?.choices?.[0]?.message?.content || '';
        return new Response(JSON.stringify({ model, output: out, raw: data }), {
          status: 200,
          headers: { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: 'internal_error', detail: String(e) }), { status: 500 });
      }
    }

    return new Response('Not found', { status: 404 });
  }
};
