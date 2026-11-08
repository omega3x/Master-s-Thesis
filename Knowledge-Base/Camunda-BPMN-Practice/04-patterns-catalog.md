# Каталог BPMN-паттернов (Camunda examples)

Источник: `BPMN/01-bpmn-examples/` + `BPMN/xml/image*.bpmn`.

---

## 1. Business Rules and BPMN

**Файлы:** `01-business-rules-and-bpmn.md`, `image1.bpmn`, `image2.bpmn`

**Сценарий:** создание счёта со скидкой.

| Подход | Описание |
|--------|----------|
| ✓ Правильно | Process flow + businessRuleTask для скидки |
| ✗ Неправильно | Дерево XOR для каждого критерия скидки |

**Урок:** правила **выносить** из diagram. Иначе cardinality растёт экспоненциально.

**Применение:** `test4.bpmn` (GPA rule), `test3.bpmn` (graduation requirements).

---

## 2. Dependent Instances

**Файл:** `02-dependent-instances.md`, image3–5

**Сценарий:** credit check — ждать завершения другого instance того же customer.

**Три решения:** Signal, Message, Timer.

**Урок:** межэкземплярная координация через **events**, не через hack в sequence flow.

---

## 3. Four Eyes Principle

**Файл:** `03-four-eyes-principle.md`, image6–8

**Сценарий:** два разных approver'а должны одобрить payment/contract.

**Паттерн:**

- pools для engine и approvers;
- user tasks в engine pool;
- message flows к manual steps approvers.

**Урок:** dual control = **explicit** в модели.

**Применение:** multi-level approval в `test3.bpmn` (chair → dean escalation).

---

## 4. Monthly Invoicing

**Файл:** `04-monthly-invoicing.md`, image9–10

**Сценарий:** legal advice + time registration + invoicing.

| ✓ | ✗ |
|---|---|
| Correct pool modeling | Wrong: смешение pools |

**Урок:** **pool boundaries** matter для B2B и billing.

---

## 5. Additional Information Required

**Файл:** `05-additional-information-required.md`, image11–12

**Сценарий:** после user task нужны доп. данные.

**Варианты:** loop к user или service request.

**Урок:** processes с documents = **loops** и exception paths.

**Применение:** reject + notify в `test3.bpmn`; можно добавить resubmit loop.

---

## 6. Processing Batch Orders

**Файл:** `06-processing-batch-orders.md`, image13

**Сценарий:** каждые 10 минут — batch из marketplace → validate → ERP.

**Паттерн:** timer start + service task + validation gateway.

**Применение:** периодическая синхронизация LMS/ERP (conceptual link to university IT).

---

## 7. Reassigning User Tasks

**Файл:** `07-reassigning-user-tasks.md`, image14–16

**Сценарий:** определить assignee динамически.

**Варианты:** service, business rule, implicit.

**Урок:** **resource allocation** можно model explicitly.

---

## 8. Two Step Escalation

**Файл:** `08-two-step-escalation.md`, image17–19

**Сценарий:** pizza delivery SLA — complain, wait, cancel.

**Три modeling solutions:**

1. Two event-based gateways (explicit, verbose)
2. Receive task + attached timers (compact, dev-friendly)
3. One event-based gateway + generic timer (generic, less explicit)

**Применение:** boundary timer на chair sign в `test3.bpmn`.

---

## Сводная таблица для промпта

| Нужно в process | Паттерн | Example # |
|-----------------|---------|-----------|
| Formal rules | Business Rule Task | 1 |
| Dual approval | Four Eyes | 3 |
| SLA / timeout | Two Step Escalation | 8 |
| Missing data loop | Additional Info | 5 |
| Batch integration | Batch Orders | 6 |
| Dynamic assignee | Reassign | 7 |
| Multi-party | Monthly Invoicing pools | 4 |

---

## Ограничение локальных XML

`generate_bpmn.py` создаёт **linear simplified** версии. Полные multi-pool diagrams — в SVG + markdown; XML может требовать доработки в Modeler.

Для AI: использовать **markdown + SVG** как few-shot context, не только image6.bpmn.
