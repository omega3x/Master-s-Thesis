# Задачи и активности в BPMN (OMG)

Источник: OMG BPMN 2.0, глава 10, Activities.

---

## Activity vs Task

**Activity** — общий термин для **единицы работы** в процессе.

**Task** — атомарная activity (не разбивается на подпроцесс на этой диаграмме).

**Sub-Process** — activity, содержащая вложенный процесс.

---

## Основные типы Task (по OMG / BPMN 2.0)

| Тип | Иконка | Кто/что выполняет |
|-----|--------|-------------------|
| **User Task** | Человек | Пользователь через UI / task list |
| **Manual Task** | Рука | Человек **вне** BPMS (не отслеживается системой) |
| **Service Task** | Шестерёнка | Автоматический сервис, API, интеграция |
| **Script Task** | Скript | Скрипт в движке процесса |
| **Business Rule Task** | Таблица | Движок правил (DMN, rule engine) |
| **Send Task** | Отправка | Отправка сообщения |
| **Receive Task** | Получение | Ожидание сообщения |
| **Task (generic)** | Без иконки | Когда тип не уточнён |

---

## Когда какой тип использовать

### User Task
- Согласование, проверка документов, ввод данных человеком.
- **Пример:** «Department chair signs transcript» в `test3.bpmn`.

### Manual Task
- Работа выполняется, но **не через** систему процесса.
- **Пример:** «фиксация рабочего времени» в `табельныйучёт2.bpmn`.

### Service Task
- Вызов LMS, ERP, генерация PDF, отправка email.
- **Пример:** «Pull final grades from LMS», «Verify academic debts in ERP».

### Business Rule Task
- Решение по правилам (GPA, eligibility).
- **Пример:** «Evaluate graduation requirements» в `test3.bpmn`.
- Camunda: правила **не** рисуют деревом в BPMN (`BPMN/01-bpmn-examples/01-business-rules-and-bpmn.md`).

### Script Task
- Небольшая автоматическая логика в движке.
- **Пример:** «Write immutable audit trail» в `test3.bpmn`.

---

## Маркеры Activity

| Маркер | Значение |
|--------|----------|
| **Loop** | Повторение задачи |
| **Multi-Instance** | Параллельное или последовательное выполнение N раз |
| **Ad-Hoc** | Набор задач без фиксированного порядка |
| **Compensation** | Компенсирующее действие при откате |

---

## Sub-Process (подпроцесс)

| Вид | Описание |
|-----|----------|
| **Embedded Sub-Process** | Вложен в родительский process в том же файле |
| **Call Activity** | Вызов **отдельного** process по ID |
| **Event Sub-Process** | Запускается событием |
| **Transaction Sub-Process** | С поддержкой compensation |

**Примеры в проекте:**

- `Subprocess_Registry` — embedded в `test3.bpmn`;
- `CallActivity_FormTabelya` → `Process_TabelnyUchet1` в `табельныйучёт2.bpmn`.

Подпроцессы — ключевой инструмент **оптимизации структуры**: декомposition без потери end-to-end view.

---

## Human Interaction (OMG)

BPMN 2.0 расширяет модель взаимодействия с людьми:

- potential owners, performers;
- humanPerformer, potentialOwner;
- формы и входные/выходные данные задачи.

На уровне XML в Camunda это часто выражается через extensions (`camunda:assignee`, formKey).

---

## Resource Assignment

Activity может ссылаться на **ресурсы** (люди, системы, роли). Lanes — визуальное выражение; semantic resource — в атрибутах XML.

---

## Оптимизация через типы задач

| Было (плохо) | Стало (лучше) |
|--------------|---------------|
| User Task «проверить в ERP вручную» | Service Task «Verify debts in ERP» |
| User Task «посчитать скидку» | Business Rule Task + rule engine |
| Одна огромная User Task | Разбиение + parallel service tasks |
| Вся логика в diagram | Call Activity на переиспользуемый subprocess |

---

## Для промпта ИИ

System Prompt перечисляет: userTask, serviceTask, scriptTask, businessRuleTask, manualTask, subprocess, callActivity. OMG требует: у каждой activity — id, name, incoming, outgoing, и для executable — исполняемая семантика.
