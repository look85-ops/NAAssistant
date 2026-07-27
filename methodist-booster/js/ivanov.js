// ============ DATA (v2.1) ============
// Категории: intro | theory | practice | debrief | discussion | test | break | meal | energizer | reflect
const gameActions = [
    { id:'intro', text:"👋 Знакомство", category:'intro', duration:20, cap:1, maxStart:90,
      dE:+5, dK:+2, dT:+5,
      reply:"Группа представилась, Иванов почувствовал, что он не один такой.",
      method:{ why:'Знакомство — это не «формальность на 5 минут», а инвестиция в безопасность группы на весь день. Если сэкономить (3–5 мин «по кругу»), участники не успевают: 1) услышать друг друга и снять тревогу; 2) увидеть, что их боли совпадают, — это база для дискуссий и кейсов позже; 3) понять контекст соседа, чтобы давать релевантный фидбек в парах и ролевых; 4) принять правила работы (контракт группы). Без этого Иванов первые 2–3 часа будет «закрыт» — теория не зайдёт, в практике он не рискнёт пробовать, в дискуссии промолчит. На урезанном знакомстве вы сэкономите 15 минут утром и потеряете 1–2 часа эффективности до обеда.', do:'Закладывай 20 мин минимум. Задай 2–3 фокусных вопроса по теме дня («что у вас сейчас болит по теме», «какой кейс хотите разобрать»), а не «расскажите о себе». На больших группах (>12 чел) — знакомство в малых группах, иначе не уложишься.' } },

    { id:'micro_lecture', text:"📖 Мини-лекция 20 мин", category:'theory', duration:20,
      dE:-6, dK:+8, dT:+2,
      reply:"Иванов слушает, делает пару заметок.",
      method:{ why:'Короткая подача удерживает внимание.', do:'Сразу после — короткое применение (пара/вопрос).' } },
    { id:'theory_block', text:"📚 Блок теории 40 мин", category:'theory', duration:40,
      dE:-15, dK:+10, dT:+1,
      reply:"Иванов держится, но к концу зевает.",
      method:{ why:'Длинная подача — риск перегрузки. Особая опасность: если методика вне зоны влияния участника (например, изменения культуры компании или решения уровня руководства) — знания дают фрустрацию и роняют мотивацию.', do:'Бей на 2×20 мин с микропрактикой между; проверь, что инструмент применим в рамках полномочий участника.' } },
    { id:'long_instruction', text:"📋 Инструкция 15 страниц", category:'theory', duration:25,
      dE:-12, dK:+3, dT:-2,
      reply:"Иванов уснул.",
      method:{ why:'Большие инструкции не читают.', do:'Чеклист 1 стр. + walkthrough.' } },

    { id:'case', text:"🧩 Кейс 25 мин", category:'practice', duration:25,
      dE:-8, dK:+7, dT:+4,
      prereq:{ knowledge: 8 },
      reply:"Иванов разбирает ситуацию, выписывает варианты решения.",
      method:{ why:'Кейс активирует знание, но без разбора критерии «не оседают».', do:'Сразу после кейса дай де-бриф (5–10 мин) — без него половина пользы теряется.' } },
    { id:'role_play', text:"🎭 Ролевая игра 25 мин", category:'practice', duration:25,
      dE:-7, dK:+5, dT:+8,
      prereq:{ knowledge: 10 },
      reply:"Иванов включился, попробовал на себе.",
      method:{ why:'Ролевая = опыт + фидбек → высокий перенос. Без де-брифа закрепление слабое.', do:'Закрой де-брифом с критериями, иначе участник остаётся в эмоциях, а не в выводах.' } },
    { id:'pairwork', text:"🤝 Работа в парах 15 мин", category:'practice', duration:15, cap:3,
      dE:-3, dK:+6, dT:+6,
      reply:"Иванов оживился, обсудил с соседом.",
      method:{ why:'Парная работа — быстрый фидбек, снижает тревогу.', do:'Не злоупотребляй (≤3/день), меняй пары и задание.' } },

    { id:'debrief', text:"🔍 Де-бриф 15 мин", category:'practice', duration:15,
      dE:-3, dK:+3, dT:+5,
      reply:"Иванов проговорил, что сработало и почему. Стало понятно, что брать в работу.",
      requiresDebriefable:true,
      method:{ why:'Де-бриф закрепляет критерии после практики и превращает опыт в навык.', do:'Делай сразу после кейса/ролевой/симуляции; задавай 3 вопроса: что произошло → почему → как сделаю в следующий раз.' } },

    { id:'discussion_managed', text:"💬 Фасилитируемая дискуссия 10 мин", category:'discussion', duration:10, cap:2,
      dE:-3, dK:+3, dT:+3,
      reply:"Группа обсудила по фокус-вопросу, Иванов услышал чужой опыт и привязал к своему.",
      method:{ why:'Управляемая дискуссия даёт осмысление и перенос: фокус-вопрос → 1 круг мнений → собранный вывод.', do:'10 минут — оптимально. Длиннее — теряется фокус, скатывается в свободную дискуссию.' } },
    { id:'discussion_free', text:"🗣 Свободная дискуссия 10 мин", category:'discussion', duration:10, cap:2,
      dE:-5, dK:+1, dT:-2,
      reply:"Группа поговорила «обо всём», Иванов потерял нить.",
      method:{ why:'Без фокус-вопроса и фасилитации дискуссия превращается в болтовню. Энергия тратится, знания не закрепляются, мотивация падает: «зачем мы это обсуждали?»', do:'Добавь фокус-вопрос, временной лимит и шаг сбора вывода — превратится в фасилитируемую.' } },

    { id:'test_short', text:"✅ Формативный тест 5 мин", category:'test', duration:5,
      dE:-2, dK:+4, dT:+3,
      reply:"Иванов проверил себя, увидел пробел.",
      method:{ why:'Короткая проверка закрепляет знание и подсвечивает дефицит. Лучше всего работает как «маркер» границы блока.', do:'Ставь перед перерывом или сразу после. Обязательно дай мгновенный фидбек и разбор неправильных ответов.' } },
    { id:'test_long', text:"📊 Итоговый тест 25 мин", category:'test', duration:25,
      dE:-12, dK:+3, dT:+1,
      reply:"Иванов отвечает наугад — устал.",
      method:{ why:'Итоговый тест нужен для оценки усвоенных знаний — это условие обучения. Но он бьёт по мотивации, особенно к концу дня.', do:'Сократи до 15–20 ключевых вопросов, ставь ближе к концу дня, но не последним блоком. Сразу после — короткий разбор.' } },

    { id:'coffee', text:"☕ Кофе-брейк 15 мин", category:'break', duration:15, cap:2, minGap:90,
      dE:+15, dK:0, dT:0,
      reply:"Иванов ожил, размялся, поболтал.",
      method:{ why:'Пауза восстанавливает внимание.', do:'Макс 2 за день, ≥ 90 мин между ними.' } },
    { id:'lunch', text:"🍽 Обед 60 мин (12:30–14:00)", category:'meal', duration:60, cap:1, windowStart:210, windowEnd:300,
      dE:+25, dK:0, dT:+2,
      reply:"Иванов поел и выдохнул.",
      method:{ why:'Обед в правильное окно — поддерживает работоспособность во второй половине дня.', do:'Окно 12:30–14:00; до — слишком рано, после — провал внимания.' } },
    { id:'energizer', text:"⚡ Разминка", category:'energizer', duration:10, cap:1, minStart:270,
      dE:+10, dK:0, dT:+2,
      reply:"Группа размялась, сонливость ушла.",
      method:{ why:'После обеда падает внимание — короткий энергайзер возвращает фокус.', do:'Проводи в первые 30 мин после обеда; формат активный, без долгих инструкций.' } },

    { id:'reflection', text:"📝 Рефлексия дня 10 мин", category:'reflect', duration:10, cap:1, minStart:420,
      dE:-2, dK:+3, dT:+12,
      prereq:{ knowledge: 20 },
      reply:"Иванов записал, что унесёт и что сделает завтра.",
      method:{ why:'Рефлексия → план действий → высокий перенос.', do:'Используй в конце дня, после содержательных блоков.' } }
];

function getMethodicalFeedback(action) {
    const f = action.method;
    if (!f) return '';
    return `<div><strong>Почему:</strong> ${f.why}</div><div style="margin-top:6px"><strong>Что сделать:</strong> ${f.do}</div>`;
}

// ============ GAME LOGIC ============
const DAY_BUDGET = 540;
const DAY_START_MIN = 9 * 60;
const WIN = { energy: 30, knowledge: 70, transfer: 60 };

let state = null;
function initState() {
    state = {
        energy: 80, knowledge: 0, transfer: 0,
        elapsed: 0, timeline: [], counts: {},
        lastBreakAt: -999,
        pendingDebrief: null,
        practiceWithoutDebrief: 0,
        active: true
    };
}
initState();

function fmtClock(mins) {
    const total = DAY_START_MIN + mins;
    const h = Math.floor(total / 60);
    const m = total % 60;
    return String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0');
}

function setMessage(msg) {
    document.getElementById('messageBox').innerHTML = "💬 " + msg;
}

function setMethodBox(html) {
    const box = document.getElementById('methodBox');
    if (!html) { box.style.display='none'; box.innerHTML=''; return; }
    box.style.display = 'block';
    box.innerHTML = html;
}

function updateMood() {
    const e = state.energy;
    const mood = document.getElementById('moodIcon');
    if (e >= 80) mood.textContent = '😄';
    else if (e >= 60) mood.textContent = '🙂';
    else if (e >= 40) mood.textContent = '😕';
    else if (e >= 20) mood.textContent = '😫';
    else mood.textContent = '😵‍💫';
}

function updateResourcesUI() {
    const set = (key, valueEl, fillEl) => {
        const v = Math.max(0, Math.min(100, state[key]));
        document.getElementById(valueEl).textContent = Math.round(v);
        document.getElementById(fillEl).style.width = v + '%';
    };
    set('energy', 'energyValue', 'energyFill');
    set('knowledge', 'knowledgeValue', 'knowledgeFill');
    set('transfer', 'transferValue', 'transferFill');
    document.getElementById('dayClock').textContent = fmtClock(state.elapsed);
    document.getElementById('dayRemain').textContent = Math.max(0, DAY_BUDGET - state.elapsed);
    renderLimits();
    renderTimeline();
    updateMood();
    renderActions();
}

function renderLimits() {
    const coffees = state.counts['coffee'] || 0;
    const lunch = state.counts['lunch'] || 0;
    const chips = [
        { label: `👋 Знакомство ${state.counts['intro']?1:0}/1`, cls: state.counts['intro'] ? 'cap' : '' },
        { label: `☕ Кофе ${coffees}/2`, cls: coffees >= 2 ? 'cap' : (coffees > 0 ? 'used' : '') },
        { label: `🍽 Обед ${lunch}/1`,  cls: lunch >= 1 ? 'cap' : '' },
        { label: `⚡ Разминка ${(state.counts['energizer']||0)}/1`, cls: (state.counts['energizer']||0) >= 1 ? 'cap' : '' },
        { label: `📝 Рефлексия ${(state.counts['reflection']||0)}/1`, cls: (state.counts['reflection']||0) >= 1 ? 'cap' : '' }
    ];
    document.getElementById('dayLimits').innerHTML =
        chips.map(c => `<span class="chip ${c.cls}">${c.label}</span>`).join('');
}

function renderTimeline() {
    const track = document.getElementById('timelineTrack');
    const segs = state.timeline.map(s => {
        const left = (s.start / DAY_BUDGET) * 100;
        const width = (s.duration / DAY_BUDGET) * 100;
        const label = s.duration >= 25 ? s.short : '';
        return `<div class="seg ${s.category}" style="left:${left}%;width:${width}%" title="${s.title}">${label}</div>`;
    }).join('');
    track.innerHTML = segs;
}

function shortLabel(category) {
    return ({
        intro:'Знаком.', theory:'Теория', practice:'Практ.', debrief:'Де-бриф',
        discussion:'Дискус.', test:'Тест', break:'Кофе', meal:'Обед',
        energizer:'Раз.', reflect:'Рефл.'
    })[category] || '';
}

function effectiveDeltas(a) {
    const used = state.counts[a.id] || 0;
    const factor = Math.pow(0.7, used);
    const noDiminish = ['coffee','lunch','energizer','intro','reflection','debrief'];
    const f = noDiminish.includes(a.id) ? 1 : factor;
    return {
        dE: Math.round(a.dE * (a.dE > 0 ? 1 : f)),
        dK: Math.round(a.dK * f),
        dT: Math.round(a.dT * f),
        factor: f
    };
}

function canDo(a) {
    if (!state.active) return { ok:false, reason:'День завершён' };
    if (state.elapsed + a.duration > DAY_BUDGET) return { ok:false, reason:'Не хватит времени до 18:00' };
    if (a.cap && (state.counts[a.id] || 0) >= a.cap) return { ok:false, reason:`Лимит ${a.cap}/день` };
    if (a.id === 'coffee') {
        if (state.elapsed - state.lastBreakAt < 90 && state.lastBreakAt > -999) {
            return { ok:false, reason:'Слишком близко к прошлому кофе (нужно ≥ 90 мин)' };
        }
    }
    if (a.windowStart != null && state.elapsed < a.windowStart) return { ok:false, reason:`Окно с ${fmtClock(a.windowStart)}` };
    if (a.windowEnd != null && state.elapsed > a.windowEnd) return { ok:false, reason:`Окно закрыто после ${fmtClock(a.windowEnd)}` };
    if (a.minStart != null && state.elapsed < a.minStart) return { ok:false, reason:`Не раньше ${fmtClock(a.minStart)}` };
    if (a.maxStart != null && state.elapsed > a.maxStart) return { ok:false, reason:`Уже поздно (до ${fmtClock(a.maxStart)})` };
    if (a.prereq && a.prereq.knowledge != null && state.knowledge < a.prereq.knowledge) {
        return { ok:false, reason:`Нужно ≥ ${a.prereq.knowledge} знаний (сейчас ${Math.round(state.knowledge)})` };
    }
    if (a.requiresDebriefable && !state.pendingDebrief) {
        return { ok:false, reason:'Де-бриф нужен сразу после практики (кейс/ролевая/пары)' };
    }
    return { ok:true };
}

function applyAction(actionId) {
    const a = gameActions.find(x => x.id === actionId);
    if (!a) return;
    const check = canDo(a);
    if (!check.ok) { setMessage('⛔ ' + check.reason); return; }

    const eff = effectiveDeltas(a);

    let debriefBonus = 0;
    if (a.id === 'debrief' && state.pendingDebrief) debriefBonus = 3;

    let undebriefedPenalty = 0;
    // Де-бриф формально тоже в категории "practice" (чтобы был с кейсами/ролевыми в одной группе UI),
    // но логически он не "практика" — он её закрывает.
    const isPractice = (a.category === 'practice' && a.id !== 'debrief');
    if (isPractice && state.pendingDebrief && state.pendingDebrief.elapsedAt != null) {
        if (state.elapsed - state.pendingDebrief.elapsedAt > 30) {
            undebriefedPenalty = -3;
            state.practiceWithoutDebrief += 1;
            state.pendingDebrief = null;
        }
    }

    state.elapsed += a.duration;
    state.energy = Math.max(0, Math.min(100, state.energy + eff.dE));
    state.knowledge = Math.max(0, Math.min(100, state.knowledge + eff.dK));
    state.transfer = Math.max(0, Math.min(100, state.transfer + eff.dT + debriefBonus + undebriefedPenalty));
    state.counts[a.id] = (state.counts[a.id] || 0) + 1;

    if (a.id === 'coffee') state.lastBreakAt = state.elapsed;
    if (isPractice) state.pendingDebrief = { id: a.id, elapsedAt: state.elapsed };
    else if (a.id === 'debrief') state.pendingDebrief = null;

    state.timeline.push({
        id: a.id, category: a.category,
        start: state.elapsed - a.duration, duration: a.duration,
        short: shortLabel(a.category),
        title: `${a.text} · ${fmtClock(state.elapsed - a.duration)}–${fmtClock(state.elapsed)}`
    });

    let msg = `[${fmtClock(state.elapsed - a.duration)}–${fmtClock(state.elapsed)}] ` + a.reply;
    if (eff.factor < 1) msg += ` <em style="color:#94a3b8">(повтор: эффект × ${eff.factor.toFixed(2)})</em>`;
    if (debriefBonus) msg += ` <em style="color:#15803d">+3 переноса (закрыли практику де-брифом)</em>`;
    if (undebriefedPenalty) msg += ` <em style="color:#b34e4e">−3 переноса (предыдущая практика без де-брифа)</em>`;
    setMessage(msg);

    let extra = '';
    if (eff.factor < 1) extra += `<div style="margin-top:6px"><strong>Повтор формата:</strong> отдача снижается. Чередуй форматы.</div>`;
    if (isPractice) extra += `<div style="margin-top:6px"><strong>Совет:</strong> в течение 30 мин закрой практику де-брифом, иначе перенос просядет.</div>`;
    if (state.elapsed >= 300 && !(state.counts['lunch'])) extra += `<div style="margin-top:6px"><strong>⚠️ Обед пропущен:</strong> окно 12:30–14:00 закрылось — будет провал внимания.</div>`;
    if (a.id === 'lunch' && !state.counts['energizer']) extra += `<div style="margin-top:6px"><strong>Подсказка:</strong> после обеда внимание падает — поставь разминку.</div>`;

    setMethodBox(getMethodicalFeedback(a) + extra);

    if (state.energy <= 0) return endDay('burnout');
    if (state.elapsed >= DAY_BUDGET) return endDay('time');
    updateResourcesUI();
}

function finishDayManually() {
    if (!state.active) return;
    endDay('manual');
}

function endDay(reason) {
    state.active = false;
    updateResourcesUI();

    const e = Math.round(state.energy);
    const k = Math.round(state.knowledge);
    const t = Math.round(state.transfer);
    const hasLunch = (state.counts['lunch'] || 0) >= 1;

    const cell = (label, val, target) => {
        const cls = val >= target ? 'ok' : (val >= target * 0.7 ? 'warn' : 'bad');
        return `<div class="verdict-cell ${cls}">${label}<span class="num">${val}</span><span style="font-size:11px;color:var(--text-soft)">цель ≥ ${target}</span></div>`;
    };

    let title, quote;
    if (reason === 'burnout') {
        title = '😵‍💫 Иванов сгорел до конца дня';
        quote = '«Я больше так не выдержу. На завтра возьму отгул.»';
    } else if (!hasLunch) {
        title = '🍽 День без обеда — Иванов измотан';
        quote = '«Голодный, злой, ничего толком не помню.»';
    } else if (k < 40) {
        title = '🫥 День прошёл — Иванов уходит пустой';
        quote = '«Посидел, поел, поговорили. А что я унесу в работу — не понял.»';
    } else if (e >= WIN.energy && k >= WIN.knowledge && t >= WIN.transfer) {
        title = '🎉 Победа: Иванов живой, научился, готов применить';
        quote = '«Усталость хорошая. Завтра попробую разбор кейса — у меня как раз похожая ситуация.»';
    } else {
        title = '🟡 День прошёл, но цель не достигнута';
        quote = '«Что-то было полезно, что-то — нет. Осадок неровный.»';
    }

    const tips = [];
    if (!state.counts['intro']) tips.push('Не было знакомства: группа не «прогрелась» — снижается включённость в первой половине дня.');
    if (e < WIN.energy) tips.push('Энергия низкая: ставь больше микро-форматов (20 мин) и кофе-брейк во второй половине.');
    if (k < WIN.knowledge) tips.push('Знаний мало: добавь практику с де-брифом и формативные проверки.');
    if (t < WIN.transfer) tips.push('Перенос низкий: ролевая + де-бриф + рефлексия с планом «что сделаю завтра».');
    if (state.practiceWithoutDebrief) tips.push(`Практика без де-брифа (×${state.practiceWithoutDebrief}) — закрывай кейсы и ролевые разбором в течение 30 мин.`);
    if (!hasLunch) tips.push('Обед обязателен в окне 12:30–14:00.');
    if ((state.counts['coffee']||0) === 0) tips.push('Хотя бы 1 кофе-брейк нужен для восстановления внимания.');
    if (hasLunch && !(state.counts['energizer'])) tips.push('После обеда — разминка: иначе провал внимания.');

    document.getElementById('adviceBox').innerHTML = `
        <div class="dashboard">
            <h3>${title}</h3>
            <div class="verdict-row">
                ${cell('⚡ Энергия', e, WIN.energy)}
                ${cell('🧠 Знания', k, WIN.knowledge)}
                ${cell('🎯 Перенос', t, WIN.transfer)}
            </div>
            <div class="quote">${quote}</div>
            ${tips.length ? `<div style="margin-top:var(--s-3)"><strong>Что поправить:</strong><ul style="margin:6px 0 0 16px">${tips.map(x=>`<li>${x}</li>`).join('')}</ul></div>` : ''}
        </div>`;
}

function resetGame() {
    initState();
    setMessage("🔄 Новый день начался. 09:00, Иванов вошёл в аудиторию.");
    setMethodBox('');
    document.getElementById('adviceBox').innerHTML = '';
    updateResourcesUI();
}

function renderActions() {
    const grid = document.getElementById('actionsGrid');
    const groups = [
        { title:'Открытие',     cats:['intro'] },
        { title:'Теория',       cats:['theory'] },
        { title:'Практика',     cats:['practice'] },
        { title:'Дискуссия',    cats:['discussion'] },
        { title:'Проверка',     cats:['test'] },
        { title:'Паузы',        cats:['break','meal','energizer'] },
        { title:'Закрытие дня', cats:['reflect'] }
    ];
    const hasLunch = (state.counts['lunch'] || 0) >= 1;
    const lateEnough = state.elapsed >= 480;
    const canFinish = state.active && lateEnough && hasLunch;
    const finishReason = !state.active ? 'День уже завершён'
                      : !lateEnough ? 'Активно с 17:00'
                      : !hasLunch ? 'Не было обеда'
                      : '';

    const html = groups.map(g => {
        const list = gameActions.filter(a => g.cats.includes(a.category));
        if (!list.length) return '';
        const btns = list.map(a => {
            const check = canDo(a);
            const cls = (a.dT < 0) ? 'bad'
                      : (a.category === 'theory' || a.id === 'test_long') ? 'bad'
                      : (a.dK >= 6 && a.dT >= 5) ? 'good' : '';
            const title = check.ok ? '' : `title="${check.reason}"`;
            return `<button class="action-btn ${cls}" ${check.ok?'':'disabled'} ${title} onclick="applyAction('${a.id}')">${a.text}</button>`;
        }).join('');

        // К строке "Закрытие дня" дописываем кнопку "Завершить день"
        let extraBtn = '';
        if (g.title === 'Закрытие дня') {
            extraBtn = `<button class="action-btn good" ${canFinish ? '' : 'disabled'} title="${finishReason}" onclick="finishDayManually()">🏁 Завершить день</button>`;
        }
        return `<div class="group-title">${g.title}</div><div class="group-row">${btns}${extraBtn}</div>`;
    }).join('');

    grid.innerHTML = html;
}

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
    updateResourcesUI();
    document.getElementById('resetBtn').onclick = resetGame;
});
