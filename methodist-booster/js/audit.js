// ============ Audit Wizard — Mager & Pipe ============

const auditCauses = [
    { id:'no_knowledge', label:'Не знают / не умеют',
      hint:'Если бы от этого зависела их зарплата на 100% — они всё равно бы не справились. Нет навыка или знания, как делать.', learning:true },
    { id:'no_practice', label:'Знают, но не отработано',
      hint:'Слышали, читали, проходили — но в реальной ситуации не делают. Нет тренировки в безопасной среде или нет фидбека.', learning:true },
    { id:'no_resources', label:'Знают, но не могут (среда не даёт)',
      hint:'Нет полномочий, инструментов, времени, доступа к данным; правила процесса противоречат нужному поведению.', learning:false, kind:'environment' },
    { id:'no_motivation', label:'Знают и могут, но не хотят',
      hint:'Нет ясных целей или метрик; нет признания за правильное поведение; неправильное поведение не имеет последствий; нет смысла лично для них.', learning:'partial', kind:'motivation' },
    { id:'no_feedback', label:'Делают вслепую — нет обратной связи',
      hint:'Не получают сигналов «сработало / не сработало»; узнают об ошибках поздно или случайно. Корректировать поведение нечем.', learning:'partial', kind:'feedback' },
    { id:'system', label:'Системная / культурная причина',
      hint:'Проблема массовая, в разных подразделениях, повторяется годами. Симптомы у людей — причины в системе/культуре/стратегии.', learning:false, kind:'culture' }
];

function changeOwnerBy(causeId) {
    return ({
        no_knowledge:  'для руководителя функции и владельца обучения',
        no_practice:   'для руководителя и наставников',
        no_resources:  'для владельца процесса и руководителя функции',
        no_motivation: 'для руководителя команды и HR',
        no_feedback:   'для руководителя команды',
        system:        'для топ-менеджмента и держателей функций'
    })[causeId] || '';
}

function audienceAdjustments(audience, causeId) {
    const adj = [];
    if (audience === 'experts') {
        if (causeId === 'no_knowledge' || causeId === 'no_practice') {
            adj.push({ title:'Формат экспертного обмена, не «обучение сверху»', detail:'Эксперты учатся у других экспертов, не у тренера. Формат: мастермайнд, peer-learning, разбор кейсов друг друга. Тренер — модератор.' });
        } else if (causeId === 'no_motivation') {
            adj.push({ title:'Работа через лидеров мнений и систему признания', detail:'Симуляции «о последствиях» для экспертов неуместны. Работайте через peer-pressure: какие коллеги их уважают, что говорит им сообщество. Параллельно — пересборка системы признания со стороны HR.' });
        } else if (causeId === 'no_feedback') {
            adj.push({ title:'Peer-ревью между экспертами', detail:'ОС от руководителя экспертам часто «не считается». Работает регулярный peer-review и публичный обмен решениями.' });
        } else {
            adj.push({ title:'Учёт зрелости аудитории', detail:'Эксперты — равноправные участники процесса изменений, не «обучаемые». Вовлекайте в проектирование решения.' });
        }
    }
    if (audience === 'new') {
        if (causeId === 'no_knowledge' || causeId === 'no_practice') {
            adj.push({ title:'Адаптационная программа + buddy/наставник', detail:'Для новых работает связка: 1-2 базовых блока обучения + наставник на 1–3 месяца. Без наставника новый сотрудник «забывает» половину уже на второй неделе.' });
            adj.push({ title:'Welcome-инструктаж и чек-листы первого месяца', detail:'Структурированные ожидания по неделям: что должен уметь к концу 1-й/2-й/4-й недели. Снижает тревогу и ускоряет вход.' });
        } else if (causeId === 'no_resources' || causeId === 'system') {
            adj.push({ title:'Внимание: новый сотрудник = индикатор', detail:'Если новые «не могут» в среде, где старые «могут» — значит, среда требует негласного опыта. Это сигнал для онбординга и описания скрытых правил.' });
        }
    }
    if (audience === 'cross') {
        adj.push({ title:'Формат для кросс-функциональной команды', detail:'Учить только одну роль бесполезно — нужен общий язык. Подходят: общий воркшоп по процессу, ролевые с разными ролями за одним столом, совместный разбор кейса.' });
        if (causeId === 'no_resources' || causeId === 'system') {
            adj.push({ title:'Воркшоп по «стыкам ролей»', detail:'Часто проблема не в самих ролях, а на границах. Соберите все роли в одной комнате — определите, кто что ожидает и где пробуксовывает.' });
        }
    }
    if (audience === 'trainers') {
        adj.push({ title:'T3 — train-the-trainer', detail:'Аудиторию учим не теме, а как её передавать: дидактика, методика подачи, работа с возражениями и сложными группами. Это методический трек поверх содержания.' });
        if (causeId === 'no_knowledge' || causeId === 'no_practice') {
            adj.push({ title:'+ Содержательный модуль (если экспертиза не глубокая)', detail:'Сначала закрываем тему, затем учим её передавать. Иначе тренер сам «плавает» и группа это видит.' });
        }
    }
    if (audience === 'executives') {
        if (causeId !== 'system') {
            adj.push({ title:'Учёт уровня: формат для топ-менеджмента', detail:'Лекции и стандартные тренинги топ-менеджмент игнорирует. Работают: стратсессия, мастермайнд, разбор кейса с привлечением внешнего эксперта, индивидуальный коучинг.' });
        }
    }
    return adj;
}

function resolveScopeConflict(scope, urgency) {
    const heavy = ['day','week','long'].includes(scope);
    if (heavy && urgency === 'now') {
        return {
            title:'Разрешение конфликта объёма и срочности',
            detail:'Запрошен объём ≥ 1 дня, но срок «на этой неделе» — не получится подготовить качественно. Предлагаем двухходовку: на этой неделе — микро-формат 1–2 часа (инструктаж/чек-лист/экспресс-кейс), полный модуль — через 3–4 недели с нормальной подготовкой.'
        };
    }
    if (scope === 'long' && urgency === 'month') {
        return {
            title:'Разрешение конфликта длительности и срочности',
            detail:'Программа от месяца с горизонтом «месяц» — значит, ждать результата к концу программы нельзя. Договоритесь с заказчиком о промежуточных метриках в первые 2–3 недели.'
        };
    }
    return null;
}

function relevantConstraints(input, causeId) {
    const c = [];
    const learningPath = (causeId === 'no_knowledge' || causeId === 'no_practice');
    if (input.budget === 'none') {
        c.push(learningPath
            ? 'Бюджет = 0: фокус на внутренних ресурсах — внутренние тренеры, наставники, экспертный обмен, кейсы из практики.'
            : 'Бюджет = 0: внешнего консультанта нанять не получится. Реалистично: воркшоп силами руководителей, ретро, внутренняя фасилитация.');
    }
    if (input.urgency === 'now' && learningPath) {
        c.push('Срочность «на этой неделе»: реалистичны только короткие форматы (1–4 часа), микро-инструктажи и чек-листы.');
    } else if (input.urgency === 'now' && !learningPath) {
        c.push('Срочность «на этой неделе»: системные изменения за неделю не делаются. Реалистично — старт диагностики или первая встреча с владельцем процесса.');
    }
    if ((input.format === 'distributed' || input.format === 'online') && learningPath) {
        c.push('Распределённая аудитория: выбирайте форматы, которые не теряют качества онлайн (фасилитация, малые группы, чёткие задания, асинхронные части).');
    }
    if (input.people === 'xlarge' && learningPath) {
        c.push('500+ человек: личная фасилитация невозможна. Либо тиражируемый продукт (онлайн-курс/видео-инструкции), либо T3 (учим внутренних тренеров).');
    } else if (input.people === 'xlarge' && !learningPath) {
        c.push('500+ человек: системные изменения такого масштаба идут через каскад — топ-менеджмент → руководители функций → команды. Готовьте коммуникационный план.');
    }
    if (input.goalType === 'culture' && causeId !== 'system') {
        c.push('Тип результата «культура»: даже если есть учебный компонент, без работы со средой и поведением руководителей результат не закрепится.');
    }
    if (causeId === 'no_knowledge' && input.goalType === 'culture') {
        c.push('Проверьте связку: тип результата «культура», а причина — «не знают». Чаще культурные сдвиги требуют не знаний, а работы с системой и поведением лидеров. Уточните диагноз с заказчиком.');
    }
    const conflict = resolveScopeConflict(input.scope, input.urgency);
    if (conflict) c.push(`<strong>${conflict.title}:</strong> ${conflict.detail}`);
    return c;
}

function buildVerdict(input) {
    const cause = auditCauses.find(c => c.id === input.causeId);
    const recommendations = [];
    let header = {}, why = '', questions = [], phrases = [], risks = [];
    const owner = changeOwnerBy(input.causeId);

    if (cause.id === 'no_knowledge') {
        header = { cls:'ok', label:'✅ Обучение уместно: нужен навык' };
        why = `У аудитории «${input.audienceLabel}» действительно нет нужного знания или навыка. Это базовый случай для обучения. Дальше выбираем формат под ${input.scopeLabel.toLowerCase()} и ${input.peopleLabel.toLowerCase()}.`;

        if (input.scope === 'short') recommendations.push({ title:'Микро-инструктаж + чек-лист на рабочее место', detail:'1–4 часа, фокус на 1 конкретном навыке. Обязательно — раздаточный чек-лист, который остаётся у человека.' });
        else if (input.scope === 'halfday') recommendations.push({ title:'Мини-практикум 4 часа', detail:'Короткая теория + 2 кейса с де-брифом. Подходит для одного навыка средней сложности.' });
        else if (input.scope === 'day') recommendations.push({ title:'Однодневный тренинг с практикой', detail:'Полный цикл: теория → практика → де-бриф → план переноса. См. модель «День Иванова» в инструменте симулятора.' });
        else if (input.scope === 'week') recommendations.push({ title:'Программа из 3–5 модулей', detail:'Модули по полдня с разрывом в 1–2 дня для применения. Между модулями — мини-задания.' });
        else recommendations.push({ title:'Программа развития: модули + практика + наставничество', detail:'Длительная программа с замером метрик на старте и в конце. Подходит для управленческих компетенций.' });

        if (input.people === 'xlarge') recommendations.push({ title:'+ Тиражируемый формат (онлайн-курс / сценарий для внутренних тренеров)', detail:'Под 500+ человек невозможна личная фасилитация. Готовим коробочное решение для масштабирования.' });

        questions = [
            'Какие конкретные ошибки/дефициты видны чаще всего?',
            'Кто сейчас умеет делать это хорошо — можем привлечь как экспертов?',
            'Как измерим успех (качество/время/ошибки) и через какой срок?',
            'Кто будет сопровождать перенос навыка в работу после обучения?'
        ];
        phrases = [
            `Предлагаю ${input.scopeLabel.toLowerCase()} в формате практикума с разбором кейсов и чек-листом на рабочее место.`,
            'Зафиксируем критерии качества на старте, проведём замер через 2–4 недели после обучения.'
        ];
        risks = ['Без де-брифа практика не закрепится', 'Без поддержки руководителя навык быстро откатится', 'Без замера успеха не сможем доказать ценность'];
    }
    else if (cause.id === 'no_practice') {
        header = { cls:'ok', label:'✅ Обучение уместно: нужна тренировка, не теория' };
        why = `Аудитория знает «как надо», но не делает это устойчиво. Учить теории — впустую, нужна тренировка в безопасной среде с обратной связью.`;
        recommendations.push({ title:'Симуляция / тренажёр / ролевые с де-брифом', detail:'Минимум теории. Многократные повторы с фидбеком. Можно делать как короткие подходы по 1–2 часа с разрывом в день.' });
        recommendations.push({ title:'Разбор реальных кейсов из практики', detail:'Берём кейсы от участников, разбираем в группах. Кейс должен быть свежий, не «учебный».' });
        if (input.audience === 'managers' || input.audience === 'executives') {
            recommendations.push({ title:'+ Коучинг / индивидуальное сопровождение', detail:'Для руководителей часто работает лучше, чем групповой тренинг — слишком разные ситуации.' });
        }
        questions = [
            'Где сейчас люди могут потренироваться безопасно — без риска для дела?',
            'Кто даёт обратную связь после реальных ситуаций? В каком формате?',
            'Какие кейсы из последнего месяца можно взять как материал для тренировки?'
        ];
        phrases = [
            'Предлагаю тренировку с многократным повтором и фидбеком, а не лекцию — теорию вы уже знаете.',
            'Замерим переносимость: соберём 3 кейса до и после.'
        ];
        risks = ['Без многократного повтора навык не закрепится', 'Без безопасной среды люди не будут пробовать'];
    }
    else if (cause.id === 'no_resources') {
        header = { cls:'warn', label:'⚙️ Обучение не лечит. Нужно править среду' };
        why = `Люди знают, что делать — но не могут: не хватает полномочий, инструментов, времени или процесс мешает. Тренинг тут даст обратный эффект: «вас научили, а делать всё равно нельзя». Это бьёт по доверию и мотивации.`;
        recommendations.push({ title:'Аудит процесса / снятие барьеров', detail:'Работа с владельцем процесса: где правила противоречат цели, что мешает в инструментах. Это change-management, не обучение.' });
        recommendations.push({ title:'Воркшоп по пересборке процесса', detail:'1–2 дня с владельцами функций и исполнителями. Цель — пересобрать процесс так, чтобы нужное поведение стало возможным. Тут уместен формат хакатона.' });
        recommendations.push({ title:'Поддержка владельца изменений', detail:'Помогаем руководителю/спонсору: что зафиксировать в правилах, как коммуницировать команде, как замерить эффект.' });
        recommendations.push({ title:'Обучение — после правок среды', detail:'Когда среда поправлена — короткий инструктаж + чек-лист, чтобы закрепить новые правила. Не наоборот.' });
        questions = [
            'Какие конкретные правила/инструменты/полномочия мешают?',
            'Кто владелец процесса и готов он править — или нет?',
            'Что произойдёт, если мы проведём обучение без правок? Какой риск?',
            'Кто будет сопровождать внедрение новых правил?'
        ];
        phrases = [
            'Мы можем начать обучение, но есть риск, что оно не сработает: люди уже знают, как надо — им не дают среда и процесс. После тренинга они вернутся в ту же систему и будут делать как раньше.',
            'В этой ситуации можем начать с короткого инструктажа и чек-листа перед выполнением задачи, но устойчивого изменения поведения скорее не произойдёт — потому что причина не в незнании.',
            `Рекомендуем ${owner}: воркшоп по пересборке (1–2 дня) — пересоберём правила и инструменты так, чтобы нужное поведение стало возможным. Обучение подключим следующим шагом, чтобы закрепить новые правила.`
        ];
        risks = ['Если провести обучение без правок среды — потеряем доверие к L&D на месяцы', 'Симптом вернётся через 2–4 недели', 'Заказчик подумает «обучение не работает», хотя проблема не в нём'];
    }
    else if (cause.id === 'no_motivation') {
        header = { cls:'warn', label:'⚙️ Обучение лечит частично. Нужны управленческие действия' };
        why = `Люди знают и могут — но не делают, потому что нет смысла или последствий. Это зона ответственности руководителя, не тренера. Обучение может поддержать, но без действий руководителя эффект краткосрочный.`;
        if (input.audience === 'managers' || input.audience === 'executives') {
            recommendations.push({ title:'Управленческая сессия / стратсессия', detail:'Для руководителей: договорённости по ожиданиям, обратной связи, признанию. Формат — фасилитированная сессия 1–2 дня с фиксацией решений.' });
        } else {
            recommendations.push({ title:'Симуляция с разбором последствий', detail:'Помогает связать поведение с результатом — для самих сотрудников. Но без подкрепления от руководителя эффект не сохранится.' });
        }
        recommendations.push({ title:'Управленческие инструменты для держателей функций', detail:'Помогаем руководителям: как ставить цели, давать обратную связь, признавать правильное поведение, корректировать неправильное. Это коучинг или мастер-класс для руководителей.' });
        recommendations.push({ title:'Пересборка системы мотивации', detail:'Совместно с HR: что подкрепляет нужное поведение, что демотивирует. Это HR-задача, не L&D.' });
        questions = [
            'Какие барьеры мотивации видите (нагрузка, признание, цели, обратная связь)?',
            'Какие сигналы от руководителей сейчас получают сотрудники по этой теме?',
            'Что происходит, когда сотрудник делает правильно? Когда неправильно?',
            'Готовы руководители поддержать изменения личным примером и коммуникацией?'
        ];
        phrases = [
            'Мы можем сделать обучение для сотрудников, но есть риск, что оно не сработает: люди знают и могут — но не видят смысла или последствий. Тренинг даст знание, поведение не изменится.',
            'В этой ситуации можем начать с симуляции «о последствиях», чтобы участники сами связали усилия с результатом. Это даст эмоциональный сдвиг на 2–4 недели — потом всё вернётся, если руководители и HR не поддержат изменения.',
            `Рекомендуем ${owner}: ${ (input.audience === 'executives' || input.audience === 'managers') ? 'стратсессию по договорённостям (ожидания, обратная связь, признание).' : 'управленческую сессию для руководителей и пересборку системы признания с HR.' } Обучение сотрудников запустим параллельно — иначе эффект краткосрочный.`
        ];
        risks = ['Без участия руководителей эффект краткосрочный', 'Если руководители своим поведением противоречат — обучение наоборот демотивирует', 'Сотрудники могут воспринять обучение как «нас опять учат, а проблема не в нас»'];
    }
    else if (cause.id === 'no_feedback') {
        header = { cls:'warn', label:'⚙️ Обучение лечит частично. Нужна система обратной связи' };
        why = `Люди что-то делают, но не получают сигналов «сработало или нет». Без обратной связи поведение не корректируется — никакой тренинг это не исправит, пока в работе нет встроенного механизма ОС.`;
        recommendations.push({ title:'Настройка системы фидбека', detail:'С руководителем: как и когда даём обратную связь, в каком формате, по каким критериям. Может включать обучение руководителей навыкам ОС.' });
        recommendations.push({ title:'Регулярные ретроспективы команды', detail:'Раз в 2 недели — короткое ретро: что сработало, что нет, что пробуем дальше. Формат, который запускается силами команды.' });
        recommendations.push({ title:'Метрики, видимые сотрудникам', detail:'Дашборды/отчёты, которые сотрудник видит сам, не через руководителя. Делает обратную связь автоматической.' });
        if (input.audience === 'managers' || input.audience === 'executives') {
            recommendations.push({ title:'+ Обучение руководителей навыкам ОС', detail:'Если руководители не дают ОС, потому что не умеют — это уже учебная задача. Короткий практикум с ролевыми.' });
        }
        questions = [
            'Кто сейчас даёт обратную связь и в каком формате?',
            'Как часто сотрудник узнаёт, что он сделал правильно/неправильно?',
            'Какие метрики/индикаторы сотрудник видит сам, без руководителя?',
            'Готовы ли руководители выделить время на регулярную ОС?'
        ];
        phrases = [
            'Мы можем провести тренинг по теме, но есть риск, что он не сработает: люди продолжат делать «как удобнее», потому что нет сигналов «правильно/неправильно».',
            'В этой ситуации можем начать с короткого практикума для руководителей по навыкам обратной связи. Это полезный шаг сам по себе, но устойчивое изменение поведения сотрудников произойдёт только когда система ОС реально заработает в команде.',
            `Рекомендуем ${owner}: настройка регулярной обратной связи (1:1, ретро раз в 2 недели), видимые сотрудникам метрики/дашборды. Обучение руководителей навыкам ОС — параллельный модуль, если выявится дефицит навыка.`
        ];
        risks = ['Без ОС любое обучение «забывается» за 2–4 недели', 'Сотрудники продолжат делать «как удобнее», не корректируя'];
    }
    else if (cause.id === 'system') {
        header = { cls:'bad', label:'🚫 Обучение не лечит. Это системная задача' };
        why = `Проблема массовая, повторяется годами, симптомы у людей — а причина в системе или культуре. L&D-инструменты здесь не помогут — нужна работа на уровне стратегии и культуры компании. Если возьмёмся за обучение — закроем симптом, причина останется.`;
        recommendations.push({ title:'Стратегическая сессия с топ-менеджментом', detail:'2–3 дня с фасилитатором: договоримся, что считаем проблемой, какой результат хотим, какие культурные сдвиги нужны. Это формат, который ведёт OD-консультант, не тренер.' });
        recommendations.push({ title:'Хакатон по пересборке процессов / культуры', detail:'1–3 дня кросс-функциональной командой: разбираем боли, пересобираем «как должно быть», фиксируем эксперименты. Формат для держателей функций и ключевых исполнителей.' });
        recommendations.push({ title:'Change-management программа', detail:'Системная работа: коммуникация изменений, работа с сопротивлением, точечные интервенции в подразделениях. Это программа на 3–6 месяцев.' });
        recommendations.push({ title:'OD-диагностика (organizational development)', detail:'Если не уверены, что причина действительно системная — короткая диагностика (интервью + опрос) поможет это подтвердить или отбросить.' });
        questions = [
            'Когда эта проблема появилась впервые? В каких подразделениях?',
            'Что уже пробовали и почему не сработало?',
            'Кто из топ-менеджмента готов взять на себя изменения?',
            'Готовы ли вы к тому, что решение займёт 3–6 месяцев, а не одну сессию?'
        ];
        phrases = [
            'Мы можем сделать обучающую программу, но есть риск, что она не сработает: проблема массовая и повторяется годами — это значит, что корень в системе или культуре, а не в людях. Тренинг закроет симптом, причина останется.',
            'Если важно показать движение быстро — можем начать с короткой обучающей серии (мини-курсы, инструктажи) перед типовыми задачами. Но устойчивого изменения поведения скорее не произойдёт, потому что среда возвращает людей к старому.',
            `Рекомендуем ${owner}: стратсессия 2–3 дня с фасилитатором — договоримся, что считаем проблемой и какие культурные сдвиги нужны. Или хакатон по пересборке (1–3 дня кросс-функциональной командой), если нужны быстрые эксперименты.`,
            'Если не уверены, что причина действительно системная — короткая OD-диагностика (интервью + опрос, 1–2 недели) подтвердит или отбросит эту гипотезу до больших инвестиций.'
        ];
        risks = ['Если возьмёмся за обучение — потратим бюджет и не получим результата', 'Заказчик потеряет доверие к L&D, хотя проблема не в обучении', 'Через год проблема всплывёт в другом виде'];
    }

    audienceAdjustments(input.audience, input.causeId).forEach(a => recommendations.push(a));
    const constraints = relevantConstraints(input, input.causeId);

    const list = arr => arr.length ? `<ul style="margin:6px 0 0 16px">${arr.map(x=>`<li>${x}</li>`).join('')}</ul>` : '<em style="color:var(--text-soft)">—</em>';
    const recList = recommendations.length
        ? `<ul style="margin:6px 0 0 16px">${recommendations.map(r=>`<li><strong>${r.title}.</strong> ${r.detail}</li>`).join('')}</ul>`
        : '<em style="color:var(--text-soft)">—</em>';

    const headerHtml = `<div class="verdict-header ${header.cls}"><strong>${header.label}</strong></div>`;
    const sumCard = `
        <div class="verdict-summary">
            <strong>Краткое саммари:</strong><br>
            ${input.desc}<br>
            <em>Цель (${input.goalTypeLabel}):</em> ${input.goal}<br>
            <em>Аудитория:</em> ${input.audienceLabel}<br>
            <em>Объём · бюджет · людей · срочность · формат:</em> ${input.scopeLabel} · ${input.budgetLabel} · ${input.peopleLabel} · ${input.urgencyLabel} · ${input.formatLabel}
        </div>`;

    return `
        ${headerHtml}
        ${sumCard}
        <div class="verdict-section"><strong>Почему такой вердикт:</strong> ${why}</div>
        <div class="verdict-section"><strong>Рекомендованные форматы:</strong>${recList}</div>
        ${constraints.length ? `<div class="verdict-section"><strong>Учёт ограничений:</strong>${list(constraints)}</div>` : ''}
        <div class="verdict-section"><strong>Вопросы заказчику:</strong>${list(questions)}</div>
        <div class="verdict-section"><strong>Репетиция формулировок:</strong>${list(phrases)}</div>
        <div class="verdict-section"><strong>Риски:</strong>${list(risks)}</div>
        <div style="margin-top:var(--s-3)"><button class="action-btn" onclick="copyAudit()">📋 Скопировать сводку</button></div>
        <div class="tool-links" style="margin-top: var(--s-4); padding-top: var(--s-3); border-top: 1px solid var(--border); font-size: var(--fs-small)">
            <strong style="color: var(--text-muted)">Другие инструменты:</strong>
            <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: var(--s-2)">
                <a class="action-btn" href="ivanov.html">🎭 Иванов</a>
                <a class="action-btn" href="activities.html">⚡ Активности</a>
                <a class="action-btn" href="cards.html">🎴 Карты</a>
                <a class="action-btn" href="vision.html">🎯 Видение</a>
                <a class="action-btn" href="index.html" style="border-color: var(--accent-blue); color: var(--accent-blue)">🏠 На главную</a>
            </div>
        </div>
    `;
}

function renderCauseOptions() {
    const box = document.getElementById('causeOptions');
    if (!box) return;
    box.innerHTML = auditCauses.map(c => `
        <label class="radio-card">
            <input type="radio" name="cause" value="${c.id}">
            <div>
                <strong>${c.label}</strong>
                <div class="radio-hint">${c.hint}</div>
            </div>
        </label>
    `).join('');
}

function showAuditStep(n) {
    if (n === 2) {
        if (!document.getElementById('auditDesc').value.trim()) { alert('Опиши ситуацию'); return; }
        document.getElementById('audit1').style.display = 'none';
        document.getElementById('audit2').style.display = 'block';
    } else if (n === 3) {
        if (!document.getElementById('auditAudience').value) { alert('Выбери аудиторию'); return; }
        document.getElementById('audit2').style.display = 'none';
        document.getElementById('audit3').style.display = 'block';
    } else if (n === 4) {
        if (!document.getElementById('auditGoal').value.trim()) { alert('Опиши цель/ожидаемое изменение'); return; }
        document.getElementById('audit3').style.display = 'none';
        document.getElementById('audit4').style.display = 'block';
    } else if (n === 5) {
        if (!document.querySelector('input[name="cause"]:checked')) { alert('Выбери основную причину'); return; }
        document.getElementById('audit4').style.display = 'none';
        document.getElementById('audit5').style.display = 'block';
    } else if (n === 6) {
        const audienceMap = {
            executives:'Топ-менеджмент / держатели функций',
            managers:'Руководители среднего звена',
            employees:'Сотрудники / исполнители',
            experts:'Эксперты',
            new:'Новые сотрудники',
            cross:'Кросс-функциональная команда',
            trainers:'Внутренние тренеры / наставники'
        };
        const scopeMap = { short:'1–4 часа', halfday:'Полдня', day:'1 день', week:'Неделя', long:'От месяца' };
        const budgetMap = { none:'Бюджет: нет', small:'Малый бюджет', medium:'Средний бюджет', large:'Большой бюджет' };
        const peopleMap = { '1':'1 человек', small:'2–10 чел', medium:'10–50 чел', large:'50–500 чел', xlarge:'500+ чел' };
        const urgencyMap = { now:'На этой неделе', month:'На месяц', quarter:'Квартал+' };
        const formatMap = { onsite:'Очно (один офис)', distributed:'Очно в разных городах', hybrid:'Гибрид', online:'Онлайн' };
        const goalTypeMap = { behavior:'поведение', knowledge:'знания/навык', outcome:'бизнес-результат', culture:'культура/отношения' };

        const input = {
            desc: document.getElementById('auditDesc').value.trim(),
            audience: document.getElementById('auditAudience').value,
            audienceLabel: audienceMap[document.getElementById('auditAudience').value] || '',
            goal: document.getElementById('auditGoal').value.trim(),
            goalType: document.getElementById('auditGoalType').value,
            goalTypeLabel: goalTypeMap[document.getElementById('auditGoalType').value] || '',
            causeId: document.querySelector('input[name="cause"]:checked').value,
            scope: document.getElementById('auditScope').value,
            scopeLabel: scopeMap[document.getElementById('auditScope').value] || '',
            budget: document.getElementById('auditBudget').value,
            budgetLabel: budgetMap[document.getElementById('auditBudget').value] || '',
            people: document.getElementById('auditPeople').value,
            peopleLabel: peopleMap[document.getElementById('auditPeople').value] || '',
            urgency: document.getElementById('auditUrgency').value,
            urgencyLabel: urgencyMap[document.getElementById('auditUrgency').value] || '',
            format: document.getElementById('auditFormat').value,
            formatLabel: formatMap[document.getElementById('auditFormat').value] || ''
        };

        document.getElementById('auditVerdict').innerHTML = buildVerdict(input);
        document.getElementById('audit5').style.display = 'none';
        document.getElementById('audit6').style.display = 'block';
    }
}

function resetAudit() {
    ['audit1','audit2','audit3','audit4','audit5','audit6'].forEach(id => {
        document.getElementById(id).style.display = (id === 'audit1') ? 'block' : 'none';
    });
    ['auditDesc','auditGoal'].forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
    const resetSelect = (id, value) => { const el = document.getElementById(id); if (el) el.value = value; };
    resetSelect('auditAudience', '');
    resetSelect('auditGoalType', 'behavior');
    resetSelect('auditScope', 'day');
    resetSelect('auditBudget', 'small');
    resetSelect('auditPeople', 'small');
    resetSelect('auditUrgency', 'month');
    resetSelect('auditFormat', 'hybrid');
    const checked = document.querySelector('input[name="cause"]:checked'); if (checked) checked.checked = false;
    document.getElementById('auditVerdict').innerHTML = '';
}

function copyAudit() {
    const el = document.getElementById('auditVerdict');
    navigator.clipboard.writeText(el.innerText);
}

document.addEventListener('DOMContentLoaded', () => {
    renderCauseOptions();
});
