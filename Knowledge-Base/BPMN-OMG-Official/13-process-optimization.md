# Оптимизация бизнес-процессов через BPMN (OMG + практика)

Источник: OMG BPMN Scope/Overview + практические паттерны (см. Camunda-BPMN-Practice).

---

## Что значит «оптимизация» в контексте BPMN

OMG не defines отдельный chapter «optimization». Оптимизация — **применение элементов BPMN** для улучшения процесса:

| Направление | BPMN-механизм |
|-------------|---------------|
| Сократить время | Parallel gateway, service tasks |
| Снизить ошибки | Business rule task, validation gateways |
| Улучшить контроль | Timers, boundary events, escalation |
| Повысить прозрачность | Lanes, data objects, audit script tasks |
| Упростить поддержку | Subprocess, call activity |
| Обработать отказы | XOR branches, reject end events |

---

## 1. Параллелизация независимых работ

**До:** последовательные проверки A → B → C.

**После:** parallel split → A, B, C → parallel join.

**Эффект:** время ≈ max(A,B,C) вместо A+B+C.

**Пример:** ERP debts + LMS grades в `test3.bpmn`.

---

## 2. Автоматизация ручных шагов

**До:** user task «зайти в LMS и выписать оценки».

**После:** service task «Pull final grades from LMS».

**Эффект:** меньше ручного труда, меньше ошибок ввода.

---

## 3. Вынос правил из диаграммы

**До:** дерево XOR для каждого критерия скидки (Camunda wrong way, image2).

**После:** businessRuleTask + rule engine (image1).

**Эффект:** diagram остаётся читаемой; правила меняются без redraw.

---

## 4. SLA и эскалация

**До:** задача «ждёт подписи» без контроля.

**После:** user task + boundary timer → escalation path.

**Эффект:** процесс не «зависает» бесконечно.

**Пример:** 5-day SLA → dean в `test3.bpmn`.

---

## 5. Декомposition

**До:** одна giant diagram на 50 tasks.

**После:** main process + call activities / subprocesses.

**Эффект:** проще анализировать, переиспользовать, поручать командам.

**Пример:** табельный учёт 1 + 2.

---

## 6. Явные пути отказа

**До:** только happy path.

**После:** XOR + notify + end rejected.

**Эффект:** полная модель для compliance и симуляции.

**Контрпример:** `test4.bpmn` — XOR без reject (нужно доработать).

---

## 7. Audit trail

**До:** действия не фиксируются.

**После:** scriptTask / serviceTask «write audit log» + parallel с notify.

**Пример:** post-issuance в `test3.bpmn`.

---

## 8. Data objects для information clarity

Связь task ↔ document показывает **какие данные** нужны и **что производится**.

Помогает найти missing steps (semantic enhancement Ayad).

---

## Метрики оптимизации (вне BPMN, но для диплома)

BPMN diagram сам по себе **не считает** KPI. Метрики получают через:

- **simulation** (Bizagi, Camunda Optimize);
- **monitoring** runtime;
- сравнение as-is / to-be models.

В отчёте: оптимизация показана **структурно**; количественная — future work.

---

## As-Is vs To-Be

| As-Is (conceptual) | To-Be (BPMN) |
|--------------------|--------------|
| Все проверки вручную | Service tasks + rules |
| Линейный процесс | Parallel checks |
| Нет SLA | Boundary timer |
| Один end | Success + reject ends |

Сравнение `test4.bpmn` (simple) vs `test3.bpmn` (optimized) — наглядно для защиты.

---

## Роль ИИ в оптимизации

ИИ **не заменяет** метод BPMN. ИИ может:

- быстрее построить to-be draft;
- предложить missing activities (Ayad);
- генерировать XML по System Prompt.

**Человек** проверяет соответствие OMG semantics и бизнес-реality.
