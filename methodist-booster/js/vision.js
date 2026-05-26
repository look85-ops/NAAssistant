// ============ Vision Wizard — Lean / JTBD ============

const VISION_MIN_CHARS = 20;
const visionLabels = [
    'Боль',
    'Пользователь и заказчик',
    'Job-to-be-done',
    'Альтернативы / конкуренты',
    'Решение и сценарии',
    'MVP (и что НЕ входит)',
    'Критерий успеха'
];

function nextStep(current) {
    const val = document.getElementById('vision' + current).value.trim();
    if (val.length < VISION_MIN_CHARS) {
        alert(`Слишком коротко. Минимум ${VISION_MIN_CHARS} символов — иначе ответ непроверяемый. Сейчас: ${val.length}.`);
        return;
    }
    document.getElementById('step' + current).style.display = 'none';
    document.getElementById('step' + (current + 1)).style.display = 'block';
}

function auditVision(answers) {
    const issues = [];
    const wins = [];

    // 1. Боль
    const pain = answers[0].toLowerCase();
    if (pain.length < 60) issues.push('Боль описана коротко. Конкретная ситуация — это люди, контекст, последствия. Если получается одной фразой — скорее всего, ты описываешь симптом, а не боль.');
    if (!/(\d|часа?|недел|месяц|раз|процент|%|штук)/i.test(answers[0])) {
        issues.push('В описании боли нет цифр или конкретики (сколько раз, как долго, кому). Без этого боль остаётся «ощущением», а не задачей.');
    } else {
        wins.push('Боль описана с конкретикой (есть цифры или измеримые маркеры).');
    }

    // 2. Пользователь vs заказчик
    const user = answers[1].toLowerCase();
    if (!/(заказчик|плати|руководител|клиент|спонсор|бизнес)/.test(user)) {
        issues.push('Не назван заказчик / тот, кто платит. Пользователь и заказчик часто разные — без обоих решение может «угодить пользователю и не пройти у бизнеса».');
    } else {
        wins.push('Различены пользователь и заказчик.');
    }

    // 3. JTBD
    const job = answers[2].toLowerCase();
    const hasJobFormat = /когда/.test(job) && /(хочу|нужно|надо)/.test(job) && /чтобы/.test(job);
    if (!hasJobFormat) {
        issues.push('Job-to-be-done не в каноническом формате «Когда … я хочу … чтобы …». Это не страшно, но без триггера и желаемого результата задача может «расплыться».');
    } else {
        wins.push('Job-to-be-done сформулирован в каноническом формате.');
    }

    // 4. Альтернативы
    const alt = answers[3].toLowerCase();
    if (alt.length < 40 || (/(нет|никак|никто|отсутств)/.test(alt) && alt.length < 80)) {
        issues.push('Альтернатив мало или «никак нет». Если люди никак не справляются — проверь, действительно ли проблема острая (возможно, они её просто терпят). Если есть конкуренты — нужно понять, чем мы иначе.');
    } else {
        wins.push('Альтернативы описаны — есть с чем сравниваться.');
    }

    // 5. Сценарии
    const scenarios = answers[4].toLowerCase();
    const hasMultiple = /(1\.|сценарий 1|первый|сначала|потом|затем|во-первых)/.test(scenarios) || (scenarios.match(/\./g) || []).length >= 3;
    if (!hasMultiple) {
        issues.push('Сценарии описаны общо. Хороший vision содержит 2–3 разных сценария «от первого касания до результата» — иначе непонятно, как продукт встраивается в жизнь.');
    } else {
        wins.push('Сценарии описаны достаточно подробно.');
    }

    // 6. MVP
    const mvp = answers[5].toLowerCase();
    const hasNotIn = /(не вход|не дела|исключ|вне scope|потом|во второй|не делаем|откладыва)/.test(mvp);
    if (!hasNotIn) {
        issues.push('MVP описан только в виде «что входит», без «что НЕ входит». Это типичная ловушка: MVP раздувается, потому что нет границы. Добавь явный список исключений.');
    } else {
        wins.push('MVP описан с границей: видно, что не входит в первую версию.');
    }

    // 7. Критерий
    const success = answers[6];
    const hasMetric = /(\d|%|процент|раз|штук|часа?|дне?й|недел|месяц|квартал)/i.test(success);
    const hasTimeframe = /(к |через |за |в течение|до |за квартал|за месяц|за неделю|за год)/i.test(success.toLowerCase());
    if (!hasMetric) issues.push('В критерии успеха нет числа. «Стало лучше» — это не критерий. Назови метрику и целевое значение.');
    if (!hasTimeframe) issues.push('В критерии нет срока. Через какое время мы проверяем результат — через месяц, квартал, год? Без срока критерий не работает.');
    if (hasMetric && hasTimeframe) wins.push('Критерий успеха измерим и со сроком.');

    return { issues, wins };
}

function visionFallbackSuggestions(answers) {
    const all = answers.join(' ').toLowerCase();
    const suggestions = [];

    if (/совещ|митин|встреч|приоритет|время на задач|перегруж|выгоран/.test(all)) {
        suggestions.push({ title: 'Тренинг по делегированию и приоритезации', detail: 'Короткая программа для руководителей: матрица Эйзенхауэра, принципы делегирования, отказ от «обязательных» встреч. Цель — высвободить 30–40% управленческого времени за квартал.' });
        suggestions.push({ title: 'Аудит и пересборка календаря встреч', detail: 'Воркшоп 1–2 дня: разбираем фактический календарь, режем встречи без цели, договариваемся о форматах асинхронных согласований. Это не обучение — это пересборка процесса.' });
        suggestions.push({ title: 'AI-планировщик с блокировкой приоритетов', detail: 'Инструмент, который автоматически защищает «фокус-блоки» в календаре, сводит встречи в окна, отслеживает время на задачи. Связать с CRM/таск-трекером.' });
        suggestions.push({ title: 'Регулярная самодиагностика «куда уходит время»', detail: 'Чек-лист на 5 минут раз в неделю + дашборд по результатам. Сначала измеряем, потом меняем — без данных любой тренинг не закрепится.' });
    }
    if (/онбординг|адаптац|нов(ые|ого|ому) сотрудник|стажёр|стажер/.test(all)) {
        suggestions.push({ title: 'Структурированная адаптационная программа', detail: 'Чек-лист первых дней, недель, месяца + наставник на 1–3 месяца. Заранее описанные ожидания снимают 80% типовых вопросов.' });
        suggestions.push({ title: 'База знаний с поиском по типовым вопросам', detail: 'Вместо отвлечения коллег — внутренняя wiki или чат-бот, в котором ищут «как сделать X». Снимает нагрузку с команды.' });
    }
    if (/мотивац|не хотят|не дела|выгоран|признан|не вид(ят|ит) смысл/.test(all)) {
        suggestions.push({ title: 'Сессия по договорённостям с руководителями', detail: 'Стратсессия / мастермайнд: что считаем правильным поведением, как признаём, как корректируем. Без участия руководителей мотивация не лечится.' });
        suggestions.push({ title: 'Пересборка системы признания (с HR)', detail: 'Что подкрепляет нужное поведение в текущей системе, что демотивирует. Часто проблема не в людях, а в стимулах вокруг них.' });
    }
    if (/ошибк|качеств|медленн|не умеют|не знают|навык|компетенц/.test(all)) {
        suggestions.push({ title: 'Практикум с де-брифом на реальных кейсах', detail: 'Не лекция, а тренировка с разбором: 1 концепт → кейс → де-бриф. Закрывает дефицит навыка точечно.' });
        suggestions.push({ title: 'Чек-лист на рабочее место + наставник', detail: 'Раздаточный материал, к которому возвращаешься в реальной задаче. Без носителя после обучения навык откатится за 2–4 недели.' });
    }
    if (/согласован|коммуникац|процесс|стык|зон ответствен/.test(all)) {
        suggestions.push({ title: 'Воркшоп по «стыкам ролей»', detail: 'Соберите все роли в одной комнате, разберите конкретные процессы. Где правила противоречат, кто что ожидает. Это не обучение, это change-management.' });
        suggestions.push({ title: 'Автоматизация рутинных согласований', detail: 'Если 80% согласований типовые — пропишите правила и автоматизируйте. Сэкономит время и снимет фрустрацию.' });
    }
    if (/обратн|фидбек|feedback|поздно узна|вслепую/.test(all)) {
        suggestions.push({ title: 'Настройка регулярных 1:1 и ретро', detail: 'Раз в 1–2 недели короткий 1:1 + ретро команды раз в 2 недели. Делает обратную связь системной, а не случайной.' });
        suggestions.push({ title: 'Дашборды и метрики, видимые сотрудникам', detail: 'Когда сотрудник видит свои показатели сам — корректировка поведения происходит автоматически, без вмешательства руководителя.' });
    }
    if (!suggestions.length) {
        suggestions.push(
            { title: 'Точечный учебный продукт', detail: 'Если ключевой блокер — навык или знание: короткий практикум с де-брифом на реальных кейсах + чек-лист на рабочее место.' },
            { title: 'Инструмент / сервис', detail: 'Если ключевой блокер — повторяющаяся рутина или нет канала: цифровой инструмент, который снимает рутинную часть с человека.' },
            { title: 'Изменение процесса', detail: 'Если ключевой блокер — правила или среда: воркшоп с владельцем процесса и пересборка регламентов. Обучение — следующим шагом.' },
            { title: 'Стратегическая сессия', detail: 'Если проблема массовая и повторяется годами — корень в системе. Стратсессия с топ-менеджментом, затем точечные интервенции.' }
        );
    }
    return suggestions.slice(0, 5);
}

async function generateVisionSuggestions(answers) {
    const system = `Ты — старший продакт-методист. На основе видения продукта предложи 3–5 конкретных направлений решения проблемы. Это могут быть РАЗНЫЕ типы решений: обучающий продукт, цифровой инструмент, изменение процесса, организационная мера, гибрид.

ТРЕБОВАНИЯ:
— Не выдумывай новую проблему — отвечай на ту, что описал пользователь.
— Не предлагай одни тренинги — если задача решается инструментом/процессом, предлагай это явно.
— Каждое направление с конкретикой: что это, как примерно работает, для кого, ожидаемый эффект.

ФОРМАТ (строго):
Направление: <короткое название, 3–6 слов>
Что это: <1–2 предложения>
Почему сработает: <привязка к боли пользователя>

Между направлениями — пустая строка.`;
    const user = `Боль: ${answers[0]}
Пользователь и заказчик: ${answers[1]}
Job-to-be-done: ${answers[2]}
Альтернативы: ${answers[3]}
Решение и сценарии: ${answers[4]}
MVP: ${answers[5]}
Критерий успеха: ${answers[6]}`;
    try {
        const response = await fetch('/.netlify/functions/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: [
                    { role: 'system', content: system },
                    { role: 'user', content: user }
                ]
            })
        });
        const data = await response.json();
        const text = data.choices?.[0]?.message?.content;
        if (!text) throw new Error('No AI');
        return { source: 'ai', text };
    } catch (e) {
        return { source: 'fallback', items: visionFallbackSuggestions(answers) };
    }
}

function renderSuggestions(result) {
    if (result.source === 'ai') {
        const html = result.text
            .replace(/(Направление|Что это|Почему сработает)\s*:/gi, '<strong>$1:</strong>')
            .replace(/\n/g, '<br>');
        return `<div>${html}</div><div class="activity-source">🤖 Сгенерировано AI</div>`;
    }
    const items = result.items.map(s =>
        `<li style="margin-bottom:0.5rem"><strong>${s.title}.</strong> ${s.detail}</li>`
    ).join('');
    return `<ul style="margin:0 0 0 16px;padding-left:4px">${items}</ul><div class="activity-source">📋 Из базы (AI недоступен)</div>`;
}

async function finishVision() {
    const val = document.getElementById('vision7').value.trim();
    if (val.length < VISION_MIN_CHARS) {
        alert(`Слишком коротко. Минимум ${VISION_MIN_CHARS} символов.`);
        return;
    }

    const answers = [];
    for (let i = 1; i <= 7; i++) {
        answers.push(document.getElementById('vision' + i).value.trim());
    }

    const { issues, wins } = auditVision(answers);

    const items = answers.map((a, i) => `<li><strong>${visionLabels[i]}:</strong> ${a}</li>`).join('');

    const winsBlock = wins.length
        ? `<div class="verdict-section"><strong style="color:var(--success)">✓ Что хорошо:</strong><ul style="margin:4px 0 0 16px">${wins.map(w=>`<li>${w}</li>`).join('')}</ul></div>`
        : '';
    const issuesBlock = issues.length
        ? `<div class="verdict-section"><strong style="color:var(--warning)">⚠ Что доработать перед презентацией заказчику или команде:</strong><div style="font-size:12px;color:var(--text-soft);margin:2px 0 4px">Эти места — типичные «дыры» в видении. Если оставить как есть, заказчик задаст вопросы или предложит своё решение вместо твоего. Лучше закрыть их заранее.</div><ul style="margin:4px 0 0 16px">${issues.map(w=>`<li>${w}</li>`).join('')}</ul></div>`
        : '<div class="verdict-section" style="color:var(--success)"><strong>Видение крепкое — методических дыр не нашёл. Можно нести заказчику.</strong></div>';

    const resultDiv = document.getElementById('visionResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div class="verdict-header" style="background: var(--tool-color-soft); color: var(--tool-color-deep)"><strong>🎯 Видение продукта</strong></div>
        <ul class="vision-summary">${items}</ul>
        ${winsBlock}
        ${issuesBlock}
        <div class="verdict-section">
            <strong>💡 Возможные направления решения:</strong>
            <div id="visionSuggestions" style="margin-top:0.4rem">
                <em style="color:var(--text-soft)">⏳ Подбираю варианты...</em>
            </div>
        </div>
        <div style="display:flex;gap:8px;margin-top:var(--s-3);flex-wrap:wrap">
            <button class="wizard-btn" onclick="copyVision()">📋 Скопировать</button>
            <button class="wizard-btn" style="background: var(--text-soft)" onclick="resetVision()">🔄 Начать заново</button>
        </div>
        <div class="tool-links" style="margin-top: var(--s-4); padding-top: var(--s-3); border-top: 1px solid var(--border); font-size: var(--fs-small)">
            <strong style="color: var(--text-muted)">Другие инструменты:</strong>
            <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: var(--s-2)">
                <a class="action-btn" href="ivanov.html">🎭 Иванов</a>
                <a class="action-btn" href="activities.html">⚡ Активности</a>
                <a class="action-btn" href="cards.html">🎴 Карты</a>
                <a class="action-btn" href="audit.html">🔍 Аудит</a>
                <a class="action-btn" href="index.html" style="border-color: var(--accent-blue); color: var(--accent-blue)">🏠 На главную</a>
            </div>
        </div>
    `;
    document.getElementById('step7').style.display = 'none';

    const result = await generateVisionSuggestions(answers);
    const box = document.getElementById('visionSuggestions');
    if (box) box.innerHTML = renderSuggestions(result);
}

function resetVision() {
    for (let i = 1; i <= 7; i++) {
        const el = document.getElementById('vision' + i);
        if (el) el.value = '';
        const step = document.getElementById('step' + i);
        if (step) step.style.display = (i === 1) ? 'block' : 'none';
    }
    document.getElementById('visionResult').style.display = 'none';
    document.getElementById('visionResult').innerHTML = '';
}

function copyVision() {
    const el = document.getElementById('visionResult');
    navigator.clipboard.writeText(el.innerText);
}
