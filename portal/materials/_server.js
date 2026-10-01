const http = require('http');
const fs = require('fs');
const path = require('path');
const base = __dirname;
http.createServer((req, res) => {
  const urlPath = req.url === '/' ? '/first-agent-print.html' : req.url.split('?')[0];
  const file = path.join(base, urlPath);
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found: ' + file); return; }
    const mime = { '.html':'text/html','.css':'text/css','.js':'text/javascript','.md':'text/plain' };
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'text/plain' });
    res.end(data);
  });
}).listen(3456, () => console.log('Server on 3456'));