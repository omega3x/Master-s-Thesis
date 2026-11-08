# Шлюзы и потоки в BPMN (OMG)

Источник: OMG BPMN 2.0, разделы Gateways, Sequence Flow, Message Flow, Connection Rules.

---

## Gateway (шлюз)

**Gateway** управляет **ветвлением и слиянием** sequence flows.

Графически: **ромб** с маркером типа.

---

## Типы шлюзов

| Шлюз | Маркер | Поведение |
|------|--------|-----------|
| **Exclusive (XOR)** | X | Только **одна** исходящая ветвь |
| **Parallel (AND)** | + | **Все** исходящие ветви одновременно |
| **Inclusive (OR)** | O | **Одна или несколько** ветвей |
| **Complex** | * | Сложная логика (редко) |
| **Event-Based** | Пентagon + circle | Выбор по **первому** наступившему событию |

---

## Exclusive Gateway

- На **split**: выбирается одна ветвь по условию или default flow.
- На **join**: ждёт **одну** incoming ветвь (merge без синхронизации) или sync в зависимости от использования.

**Условия:** `conditionExpression` на sequence flow, `default` на gateway.

**Пример:** `Gateway_Eligible` — «Meets requirements?» Yes/No в `test3.bpmn`.

**Ошибка в проекте:** `test4.bpmn` — XOR с одной исходящей ветвью (нет rejection path).

---

## Parallel Gateway

- **Split:** token **дублируется** на все исходящие ветви.
- **Join:** ждёт завершения **всех** incoming ветвей.

**Оптимизация:** независимые проверки выполняются **параллельно**, а не последовательно.

**Примеры:**

- ERP + LMS checks в `test3.bpmn`;
- три анализа в `табельныйучёт1.bpmn`;
- post-issuance notify + audit в `test3.bpmn`.

---

## Inclusive Gateway

- Split: активируются **все ветви с true условием** (одна или больше).
- Join: ждёт все **активированные** ветви.

**Пример:** `Gateway_Inclusive_Join` в `табельныйучёт2.bpmn` — слияние потоков из department и HR.

---

## Event-Based Gateway

После gateway процесс **ждёт** одно из нескольких events (message, timer). Используется для эскалации и ожидания внешних сигналов.

Camunda: Three solutions in `08-two-step-escalation.md`.

---

## Sequence Flow

| Свойство | Описание |
|----------|----------|
| `sourceRef` | Откуда |
| `targetRef` | Куда |
| `conditionExpression` | Условие (optional) |
| `default` | На gateway — ветвь по умолчанию |

**Правила OMG (упрощённо):**

- sequence flow соединяет flow objects **внутри** одного process;
- не соединяет pool с pool напрямую;
- start event — только outgoing;
- end event — только incoming.

---

## Message Flow

- Между **pools** или между pool и activity;
- передаёт **message**, не token;
- асинхронная коммуникация между участниками.

---

## Association и Data Association

- **Association** — пунктирная линия к text annotation, group, data object;
- **Data Association** — направление потока данных к/от activity.

---

## Default Flow

На exclusive/inclusive gateway рекомендуется **default** sequence flow для случая «ни одно условие не подошло».

В `test3.bpmn`: `default="Flow_NotEligible"` и `default="Flow_NotApproved"`.

---

## Оптимизация через шлюзы

| Цель | Шлюз |
|------|------|
| Ускорить независимые проверки | Parallel split/join |
| Ветвление по решению | Exclusive |
| Несколько optional paths | Inclusive |
| Ожидание первого из событий | Event-based |

---

## Проверка модели

1. У каждого split есть соответствующий join (для parallel/inclusive).
2. У XOR все исходящие ветви **покрывают** случаи (включая reject).
3. Условия **формальны** для executable process.
4. Нет «мёртвых» ветвей без end event.

ИИ часто создаёт gateway без второй ветви — это нарушение практики OMG и Camunda.
