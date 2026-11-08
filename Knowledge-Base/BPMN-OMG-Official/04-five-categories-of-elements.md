# Пять категорий элементов BPMN (OMG)

Источник: OMG BPMN 2.0, раздел 7.2 BPMN Elements.

---

## Зачем категории

BPMN должен быть одновременно:

- **простым** для чтения бизнес-пользователем;
- **достаточно мощным** для сложных процессов.

Решение OMG: небольшое число **категорий** элементов. Читатель диаграммы сразу понимает тип элемента. Внутри категории допускаются варианты (маркеры, подтипы).

---

## Категория 1. Flow Objects (объекты потока)

**Главные элементы поведения процесса.** Три типа:

| Тип | Роль | Форма |
|-----|------|-------|
| **Events** | Что происходит | Круг |
| **Activities** | Что делается | Прямоугольник со скруглёнными углами |
| **Gateways** | Разветвление и слияние | Ромб |

Flow Objects соединяются **sequence flows** внутри одного process/pool.

---

## Категория 2. Data (данные)

Четыре элемента данных:

| Элемент | Назначение |
|---------|------------|
| **Data Object** | Информация, используемая в процессе |
| **Data Input** | Входные данные процесса |
| **Data Output** | Выходные данные процесса |
| **Data Store** | Хранилище данных (переживает процесс) |

BPMN **не моделирует** полную структуру данных. Показывается **связь** активности с документом или объектом.

**Пример в проекте:** в `test3.bpmn` — «Official transcript», «Diploma record»; в `табельныйучёт2.bpmn` — «табели», «больничные».

---

## Категория 3. Connecting Objects (соединяющие объекты)

| Объект | Назначение |
|--------|------------|
| **Sequence Flow** | Порядок выполнения внутри process |
| **Message Flow** | Обмен сообщениями между pools/participants |
| **Association** | Связь артефакта или данных с элементом |
| **Data Association** | Связь data object с activity |

**Правило:** sequence flow — внутри pool; message flow — между pools.

---

## Категория 4. Swimlanes (дорожки)

| Элемент | Назначение |
|---------|------------|
| **Pool** | Участник процесса (организация, система, роль верхнего уровня) |
| **Lane** | Подразделение ответственности внутри pool |

Lanes **не влияют** на семантику исполнения (token не «принадлежит» lane), но важны для **понимания** и **оптимизации** (кто делает работу).

---

## Категория 5. Artifacts (артефакты)

| Артефакт | Назначение |
|----------|------------|
| **Group** | Визуальная группировка без семантики |
| **Text Annotation** | Пояснение на диаграмме |

Артефакты **не участвуют** в исполнении. Они помогают читать диаграмму.

---

## Basic vs Extended элементы

OMG делит элементы на:

- **Basic** — минимальный набор для большинства диаграмм;
- **Extended** — transaction, compensation, complex gateway, event subprocess и др.

Для диплома и AI-генерации достаточно Basic + часть Extended (subprocess, boundary timer, data objects).

---

## Сводная таблица для промпта ИИ

При генерации BPMN XML ИИ должен знать категорию каждого элемента:

```
Flow Objects:  startEvent, userTask, serviceTask, exclusiveGateway, ...
Data:          dataObject, dataObjectReference, dataStoreReference
Connecting:    sequenceFlow, messageFlow, association
Swimlanes:     lane, laneSet (внутри process) или participant (pool)
Artifacts:     textAnnotation, group
```

Плюс **графика** (отдельная категория в XML): BPMNShape, BPMNEdge, Bounds, waypoint.

---

## Частая ошибка

Смешивать **process flow** (sequence) и **communication** (message):

- ❌ sequence flow между двумя pools;
- ✅ message flow между pools, sequence flow внутри pool.

System Prompt в проекте требует корректных связей именно по этим правилам OMG.
