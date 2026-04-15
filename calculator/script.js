(() => {
  const display = document.getElementById('display');

  const state = {
    a: null,      // first operand
    op: null,     // operator: "+", "-", "*", "/"
    b: null,      // second operand being typed
    overwrite: true,
  };

  const fmt = (n) => {
    if (typeof n !== 'number' || !isFinite(n)) return 'Ошибка';
    const s = n.toString();
    // Limit length to avoid overflow
    return s.length > 14 ? Number(n.toPrecision(10)).toString() : s;
  };

  const readDisplay = () => display.textContent.replace(',', '.');
  const writeDisplay = (val) => {
    const text = (typeof val === 'number') ? fmt(val) : String(val);
    // Show comma as decimal separator for RU locale
    display.textContent = text.replace('.', ',');
  };

  const inputDigit = (d) => {
    const cur = readDisplay();
    if (state.overwrite || cur === '0') {
      writeDisplay(d);
      state.overwrite = false;
    } else {
      writeDisplay(cur + d);
    }
  };

  const inputDecimal = () => {
    const cur = readDisplay();
    if (!cur.includes('.')) writeDisplay(cur + '.');
    state.overwrite = false;
  };

  const setOperator = (op) => {
    const cur = Number(readDisplay());
    if (state.op && !state.overwrite) {
      // Chain operations: compute previous first
      compute();
    } else {
      state.a = cur;
    }
    state.op = op;
    state.overwrite = true;
  };

  const compute = () => {
    if (state.op == null) return;
    const a = (state.a == null) ? Number(readDisplay()) : state.a;
    const b = Number(readDisplay());
    let res = 0;
    switch (state.op) {
      case '+': res = a + b; break;
      case '-': res = a - b; break;
      case '*': res = a * b; break;
      case '/': res = b === 0 ? NaN : a / b; break;
      default: return;
    }
    state.a = res;
    state.op = null;
    writeDisplay(res);
    state.overwrite = true;
  };

  const clearAll = () => {
    state.a = null;
    state.op = null;
    state.b = null;
    state.overwrite = true;
    writeDisplay('0');
  };

  const del = () => {
    const cur = readDisplay();
    if (state.overwrite) return;
    const next = cur.length > 1 ? cur.slice(0, -1) : '0';
    writeDisplay(next);
  };

  const toggleSign = () => {
    const cur = readDisplay();
    if (cur === '0') return;
    if (cur.startsWith('-')) writeDisplay(cur.slice(1));
    else writeDisplay('-' + cur);
  };

  document.querySelector('.keys').addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const action = btn.dataset.action;
    if (action === 'digit') inputDigit(btn.dataset.digit);
    else if (action === 'decimal') inputDecimal();
    else if (action === 'operator') setOperator(btn.dataset.op);
    else if (action === 'equals') compute();
    else if (action === 'clear') clearAll();
    else if (action === 'delete') del();
    else if (action === 'sign') toggleSign();
  });

  // Keyboard support
  window.addEventListener('keydown', (e) => {
    if (/[0-9]/.test(e.key)) inputDigit(e.key);
    else if (e.key === '.' || e.key === ',') inputDecimal();
    else if (['+', '-', '*', '/'].includes(e.key)) setOperator(e.key);
    else if (e.key === 'Enter' || e.key === '=') compute();
    else if (e.key === 'Backspace') del();
    else if (e.key.toLowerCase() === 'c') clearAll();
  });
})();
