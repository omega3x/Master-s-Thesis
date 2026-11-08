# Подпроцессы и хореография (OMG)

Источник: OMG BPMN 2.0, главы 9–10.

---

## Зачем Sub-Process

Большой процесс трудно читать и поддерживать. **Sub-Process** позволяет:

- скрыть детали (collapsed);
- переиспользовать логику (call activity);
- изолировать транзакции и compensation;
- обрабатывать исключения (event subprocess).

---

## Embedded Sub-Process

Вложен **внутри** родительского process в том же BPMN file.

| Режим | Вид |
|-------|-----|
| Expanded | Видны внутренние элементы |
| Collapsed | + маркер, детали скрыты |

**Пример:** `Subprocess_Registry` в `test3.bpmn`:

1. Generate diploma PDF
2. Apply digital signature
3. Archive record

Родительский process видит subprocess как **одну** activity.

---

## Call Activity

Вызывает **другой** process по `calledElement="Process_Id"`.

| Плюс | Минус |
|------|-------|
| Переиспользование | Два файла / два deployable process |
| Модульность | Нужна ссылка на существующий process id |

**Пример:** `табельныйучёт2.bpmn` вызывает `Process_TabelnyUchet1` из `табельныйучёт1.bpmn`.

При импорте в Camunda/Bizagi оба process должны быть доступны.

---

## Event Sub-Process

Запускается **событием**, а не incoming sequence flow.

- прерывающий (interrupting) — отменяет родительскую activity;
- непрерывающий — параллельная обработка.

Паттерн **exception handling** без загромождения main flow.

---

## Transaction Sub-Process

Группа activities с **compensation** при откате.

Для финансовых/критичных операций. В university models редко, но упоминается в OMG как advanced pattern.

---

## Choreography (кратко)

Choreography описывает **взаимодействие** без центрального orchestrator.

- Activities = **interactions** (обмен messages);
- Между participants, не внутри одного pool;
- Полезно для B2B контрактов.

В дипломном проекте **не моделируется**, но упоминается как часть полного стандарта OMG.

---

## Оптимизация структуры

| Проблема | Решение BPMN |
|----------|--------------|
| Диаграмма > 30 элементов | Call Activity + subprocess files |
| Повторяющийся блок в нескольких процессах | Reusable process + call |
| Сложная обработка ошибок | Event subprocess |
| Длинная «линия» задач HR | Embedded subprocess «формирование табеля» |

---

## Связь с generate_bpmn.py

Скрипт в `BPMN/xml/` **не генерирует** subprocess/callActivity — только linear chains. Сложная структура делается вручную или через LLM + System Prompt.
