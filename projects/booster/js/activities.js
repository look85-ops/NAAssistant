// ============ Activities — генератор активных форм обучения ============

const staticActivities = [
    { title: "Одна задача — три решения", goal: "осмысление",
      run: "В парах: каждый предлагает 3 варианта решения по теме дня (3 мин), затем обмен (2 мин). В круге — какие варианты повторились, какие оказались неожиданными.",
      materials: "Стикеры или блокнот",
      watch: "Если все варианты одинаковые — тема слабо проработана; вернитесь к теории." },
    { title: "Самое важное за 90 секунд", goal: "осмысление",
      run: "Каждый участник по очереди говорит ровно 90 секунд: «что для меня сегодня было самым важным и почему». Остальные слушают молча.",
      materials: "Таймер",
      watch: "Тишина после — норма; не заполняйте её комментариями." },
    { title: "Чек-ин по шкале 1–10", goal: "включение",
      run: "По кругу: «насколько я понимаю тему по шкале 1–10 и почему такая цифра» (1 предложение). Фиксируете медиану на флипчарте.",
      materials: "Флипчарт",
      watch: "Не комментируйте оценки; это не оценка участника, а зеркало для группы." },
    { title: "Что я сделаю завтра", goal: "решение",
      run: "Индивидуально 3 мин: записать 1 конкретное действие, которое я сделаю завтра по результатам обучения. В парах — рассказать друг другу, проверить на конкретность (что, когда, как пойму, что сделал).",
      materials: "Карточки/блокнот",
      watch: "«Буду внимательнее» — не действие; помогайте довести до конкретики." },
    { title: "Группа экспертов", goal: "решение",
      run: "Поделите на 3 группы. Каждая получает свой вопрос/задачу, готовит ответ 5–7 мин. Затем каждая группа коротко защищает решение, остальные задают по 1 уточняющему вопросу.",
      materials: "Карточки с вопросами, флипчарт",
      watch: "Если вопросы из зала формальные — группе не ясна задача; уточните формулировку." },
    { title: "Карта решения", goal: "осмысление",
      run: "В группах: на флипчарте нарисовать схему — «как мы будем применять это в работе». 7 мин. Один представитель от группы показывает.",
      materials: "Флипчарт, маркеры",
      watch: "Схема без стрелок и связей — значит, понимания связей нет; задайте уточняющие вопросы." },
    { title: "Стоп-кадр", goal: "осмысление",
      run: "Покажите 1 рабочую ситуацию (кейс/видео/описание). Группа 2 мин обсуждает: «что не так и что бы сделали мы». Соберите 2–3 ответа.",
      materials: "Описание кейса",
      watch: "Не подгоняйте к «правильному» ответу — соберите варианты, потом сравните." },
    { title: "Два круга вопросов", goal: "включение",
      run: "В парах 5 мин: каждый задаёт партнёру 2 вопроса по теме. Затем смена пар, ещё 5 мин. В круге: «какой вопрос оказался самым полезным».",
      materials: "Нет",
      watch: "Не уточняйте «что считать полезным»; пусть участники сами договариваются." },
    { title: "Светофор понимания", goal: "осмысление",
      run: "Раздайте 3 стикера (красный/жёлтый/зелёный). Участник клеит цвет к месту на флипчарте, где описана тема. Обсудите 1–2 «красные» зоны.",
      materials: "Цветные стикеры, флипчарт",
      watch: "Если красных много — переходить дальше нельзя; вернитесь к разбору." },
    { title: "Чёрный/белый адвокат", goal: "решение",
      run: "Разделите группу на 2 части. Одни 3 мин аргументируют «за» предложенное решение, другие 3 мин — «против». В круге: «какой аргумент с другой стороны был самым сильным».",
      materials: "Нет",
      watch: "Тема должна быть реально спорной, иначе игра будет формальной." },
    { title: "Точка возврата", goal: "решение",
      run: "Индивидуально: «к чему из сегодняшнего материала я вернусь через неделю и зачем». 2 мин подумать, 1 мин — записать. По желанию — поделиться 2–3 ответами.",
      materials: "Блокнот",
      watch: "Если никто не хочет делиться — не давите; запись ценнее, чем озвучивание." },
    { title: "Ошибка из практики", goal: "осмысление",
      run: "В малых группах 5 мин: «опишите 1 ошибку из работы по теме дня — что произошло, почему, что сделали». Каждая группа делится 1 кейсом. Разбираете в формате «что предотвратило бы».",
      materials: "Нет",
      watch: "Не превращайте в разбор персоналий; фокус на «что мешало в системе»." },
    { title: "Перенос за 5 минут", goal: "решение",
      run: "Каждый записывает: 1 инструмент, который возьмёт в работу; 1 препятствие, которое может ему помешать; 1 человек/ресурс, который поможет его преодолеть.",
      materials: "Карточки",
      watch: "Препятствие = «нет времени» — слишком общо; уточняйте, что конкретно мешает." },
    { title: "Кто я для темы", goal: "включение",
      run: "По кругу 1 предложение: «по этой теме я — новичок / опытный / эксперт, потому что...». Фиксируете распределение группы.",
      materials: "Нет",
      watch: "Знание состава влияет на формат дальше; новичкам — больше базы, экспертам — больше кейсов." },
    { title: "Один вопрос к эксперту", goal: "осмысление",
      run: "Каждый записывает 1 вопрос по теме, на который пока нет ответа. Собираете на флипчарт, группируете похожие, отвечаете в нужный момент дня.",
      materials: "Стикеры, флипчарт",
      watch: "Если вопросов меньше 1 на участника — группа закрыта; начните с парного обсуждения." }
];

function formatStaticActivity(a) {
    return `<strong>${a.title}</strong><br>
            <strong>Ход:</strong> ${a.run}<br>
            <strong>Материалы:</strong> ${a.materials}<br>
            <strong>На что смотреть:</strong> ${a.watch}`;
}

const activityHistory = [];

function buildActivityPrompt() {
    const topic = document.getElementById('topicInput').value.trim();
    const goal = document.getElementById('goalSelect').value;
    const time = document.getElementById('timeSelect').value;
    const group = document.getElementById('groupSelect').value;

    const system = `Ты — методист, проектирующий обучение для взрослых в технических и управленческих ролях (например, инженеры, руководители среднего звена). Опирайся на принципы andragogy: связь с реальной работой, добровольность, безопасность, ясная польза.

ЧЕГО НЕ ДЕЛАТЬ:
— Не предлагай форматы с публичным унижением, «стены позора», обсуждение чужих ошибок поимённо.
— Не используй «детские» механики (рисовать, спорить про 2+2=5, угадывать на скорость с призом).
— Не предлагай соревнование без обучающей цели.
— Не требуй сложных материалов (флипчарт/стикеры/маркеры допустимы; проектор — по необходимости).
— Не выдавай абстрактные «обсудите тему» без конкретного хода.

ТРЕБОВАНИЯ:
— Активность должна быть проверенной, не «оригинальной ради оригинальности».
— Должна давать конкретный результат, проверяемый ведущим.
— Уровень сложности подходит взрослым с опытом.

ФОРМАТ ОТВЕТА (строго, без отступлений):
Название: <короткое название, 2–5 слов>
Цель: <одной фразой, что участник должен сделать/понять/решить>
Ход: <пошагово, 2–4 предложения; конкретные действия и тайминг внутри>
Материалы: <что нужно подготовить; если ничего — напиши «нет»>
На что смотреть: <методический маркер: что считать сигналом, что активность сработала или провалилась>`;

    const userParts = [
        `Длительность: до ${time} минут.`,
        `Формат группы: ${group}.`,
        `Тип цели: ${goal}.`
    ];
    if (topic) userParts.push(`Контекст/тема: ${topic}.`);
    if (activityHistory.length) {
        userParts.push(`Уже использованы в этой сессии (не повторяй и не предлагай близкие варианты): ${activityHistory.slice(-8).join('; ')}.`);
    }
    userParts.push('Дай ровно одну активность в указанном формате.');

    return { system, user: userParts.join('\n') };
}

function parseActivityResponse(text) {
    const m = text.match(/Название\s*:\s*(.+)/i);
    return m ? m[1].trim() : null;
}

function renderActivityAI(text) {
    return text
        .replace(/(Название|Цель|Ход|Материалы|На что смотреть)\s*:/gi, '<strong>$1:</strong>')
        .replace(/\n/g, '<br>');
}

async function generateActivityAI() {
    const btn = document.getElementById('genActivityBtn');
    const result = document.getElementById('activityResult');

    btn.disabled = true;
    btn.textContent = "⏳ Генерирую...";
    result.style.display = 'none';

    const { system, user } = buildActivityPrompt();

    try {
        // GitHub Pages: серверных функций нет; если понадобится — вынести в отдельный сервис
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
        const activity = data.choices?.[0]?.message?.content;
        if (!activity) throw new Error('No AI');

        const title = parseActivityResponse(activity);
        if (title) activityHistory.push(title);

        const meta = `⏱ до ${document.getElementById('timeSelect').value} мин · Формат: ${document.getElementById('groupSelect').value}`;
        result.innerHTML = renderActivityAI(activity)
            + `<div class="activity-meta">${meta}</div>`
            + '<div class="activity-source">🤖 Сгенерировано AI</div>';
        result.style.display = 'block';
    } catch (e) {
        let pool = staticActivities.slice();
        if (activityHistory.length) {
            pool = pool.filter(a => !activityHistory.includes(a.title));
            if (!pool.length) pool = staticActivities.slice();
        }
        const pick = pool[Math.floor(Math.random() * pool.length)];
        activityHistory.push(pick.title);
        result.innerHTML = formatStaticActivity(pick)
            + '<div class="activity-source">📋 Из базы (AI недоступен)</div>';
        result.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = "🎲 Сгенерировать";
    }
}

function applyPreset(key) {
    const topic = document.getElementById('topicInput');
    const goal = document.getElementById('goalSelect');
    const time = document.getElementById('timeSelect');
    const group = document.getElementById('groupSelect');
    const presets = {
        energizer:  { topic: 'включение группы',                         goal: 'включение',  time: '5',  group: 'в группах' },
        warmup:     { topic: 'разогрев дискуссии по теме занятия',       goal: 'осмысление', time: '10', group: 'в парах' },
        case10:     { topic: 'разбор 1 практического кейса',             goal: 'осмысление', time: '10', group: 'в группах' },
        retro:      { topic: 'быстрая ретроспектива прошедшего спринта', goal: 'осмысление', time: '10', group: 'в группах' },
        groupSolve: { topic: 'выработка решения для задачи заказчика',   goal: 'решение',    time: '15', group: 'в группах' },
        closure:    { topic: 'закрытие модуля и перенос в практику',     goal: 'решение',    time: '10', group: 'индивидуально' }
    };
    const p = presets[key];
    if (!p) return;
    topic.value = p.topic;
    goal.value = p.goal;
    time.value = p.time;
    group.value = p.group;
    generateActivityAI();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('genActivityBtn').onclick = generateActivityAI;
});
