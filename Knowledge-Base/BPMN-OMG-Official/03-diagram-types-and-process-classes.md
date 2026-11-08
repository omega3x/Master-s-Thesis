# Типы диаграмм и классы процессов (OMG)

Источник: OMG BPMN 2.0, раздел 7.1.1 Uses of BPMN, главы 9–10.

---

## 1. Private (внутренние) бизнес-процессы

**Private Business Process** — процесс **внутри одной организации**.

Другие названия: workflow, BPM-процесс, orchestration сервисов.

### Два подтипа

| Тип | Назначение | Детализация |
|-----|------------|-------------|
| **Executable** | Для исполнения в BPM-движке | Полные условия, формальные выражения, исполняемая семантика |
| **Non-executable** | Для документирования | Уровень детализации задаёт моделировщик; условия могут быть неформальными |

На ранних этапах проектирования процесс часто non-executable. По мере уточнения он становится executable.

### Границы private process

- Поток **sequence flow** не выходит за пределы одного Pool.
- **Message flow** может пересекать границу Pool и показывать обмен с другими участниками.

**Пример в проекте:** `Output/test3.bpmn` (Graduate Diploma Issuance) — private executable process с тремя lanes внутри одного pool.

---

## 2. Public (публичные) процессы

**Public Process** показывает **внешнее поведение** private process: только те действия, через которые процесс общается с другими участниками.

- Внутренние действия **не показываются**.
- Видны message flows и порядок обмена сообщениями.
- В BPMN 1.2 назывался «abstract process».

**Зачем нужен:** контракт B2B, API-подобное описание «что снаружи видит партнёр».

---

## 3. Collaboration (коллаборация)

**Collaboration** — взаимодействие **два и более** business entity.

Содержит:

- два или более **Pool** (участники);
- **Message Flow** между pools;
- опционально: public processes, пустые pools («black box»), choreography между pools.

**Пример:** пациент и клиника обмениваются сообщениями; у каждого свой pool, но они связаны message flows.

**В проекте:** пример Four Eyes в `BPMN/01-bpmn-examples/03-four-eyes-principle.md` использует отдельные pools для approvers.

---

## 4. Choreography (хореография)

**Choreography** — описание **ожидаемого поведения** между участниками как процедурного контракта.

Отличия от обычного Process:

| Process | Choreography |
|---------|--------------|
| Внутри одного Pool | Между Pools |
| Есть центральный контроллер | Нет центрального контроллера |
| Activities — работа | Activities — взаимодействия (обмен сообщениями) |

Choreography полезна для B2B, где ни одна сторона не «владеет» всем процессом.

---

## 5. Conversation (разговоры)

**Conversation diagram** — упрощённый вид Collaboration.

- Показывает **логические группы** обмена сообщениями (hexagon «Conversation»).
- Даёт «вид сверху» на бизнес-сценарии: заказ, доставка, оплата.
- Обычно pools **не содержат** детальный process.

**Пример из спецификации:** логистика — sales orders, shipment, customs, payment как отдельные conversations.

---

## 6. Типы BPMN-диаграмм (сводка)

| Диаграмма | Что показывает | Когда использовать |
|-----------|----------------|-------------------|
| Process | Поток работ внутри организации | Основной кейс диплома |
| Collaboration | Взаимодействие участников | B2B, интеграции |
| Choreography | Контракт между сторонами | Межорганизационные контракты |
| Conversation | Группы сообщений | Высокоуровневый обзор |

---

## 7. Point of View (точка зрения)

Один и тот же Collaboration diagram **разные участники видят по-разному**:

- для Patient: «Go see doctor» — internal;
- для Doctor: «Receive symptoms» — internal;
- для другой стороны — external.

BPMN **не задаёт** графический способ выделить точку зрения. Это задача моделировщика или инструмента.

---

## 8. Token (фишка) для понимания поведения

OMG описывает поведение процесса через концепцию **token**:

- Start Event **создаёт** token;
- token **движется** по sequence flows через gateways и activities;
- End Event **поглощает** token;
- token **не идёт** по message flow (там передаются messages).

Инструменты **не обязаны** реализовывать token буквально. Это учебная модель для понимания семантики.

---

## Связь с нашим проектом

| Модель | Тип по OMG |
|--------|------------|
| `Output/test3.bpmn` | Private executable Process |
| `Output/test4.bpmn` | Private executable Process (упрощённый) |
| `XML код/табельныйучёт2.bpmn` | Private Process + CallActivity |
| `Literature/.../Medical2.xpdl` | Collaboration (Hospitalization) |
| Camunda Four Eyes | Collaboration (multi-pool) |

Для диплома достаточно уверенно владеть **Process** и базовым **Collaboration**. Choreography и Conversation — теоретическое дополнение.
