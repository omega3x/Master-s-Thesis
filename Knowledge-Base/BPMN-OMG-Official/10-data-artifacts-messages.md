# Данные, артефакты и сообщения (OMG)

Источник: OMG BPMN 2.0, Data, Messages, Artifacts.

---

## Data Object

**Data Object** — информация, которая **используется** или **производится** в процессе.

- Не полная модель данных (не ER-диаграмма).
- Показывает **какой документ** связан с задачей.

**Связь:** association или dataInputAssociation / dataOutputAssociation.

**Примеры в проекте:**

| Файл | Data Object |
|------|-------------|
| test3.bpmn | Official transcript, Diploma record |
| табельныйучёт1.bpmn | ведомости |
| табельныйучёт2.bpmn | табели, больничные |

---

## Data Input / Data Output

На границе **process** или **activity**:

- **Data Input** — что process получает на вход;
- **Data Output** — что process отдаёт на выход.

Используются в executable models с формальными IO.

---

## Data Store

**Постоянное хранилище** (БД, архив, registry).

Переживает завершение process instance. Отличается от data object, который «проходит» через процесс.

**Пример (концептуально):** archive system в subprocess registry `test3.bpmn`.

---

## Message

**Message** — содержимое, передаваемое через **message flow** между participants.

В XML: `message`, `messageEventDefinition`, `messageRef`.

Hospitalization (Ayad): messages между Patient, Secretary, Doctor, Nurse.

---

## Artifacts

| Артефакт | Исполнение | Назначение |
|----------|------------|------------|
| **Text Annotation** | Нет | Пояснение для читателя |
| **Group** | Нет | Визуальная рамка вокруг элементов |

Не влияют на token. Полезны в отчётах и для преподавателя.

---

## Item Definition

OMG связывает data elements с **типом данных** (часто через XML Schema).

На практике в Camunda/Bizagi часто достаточно name на data object.

---

## Semantic enhancement (связь с Ayad)

Статья Ayad & Alsayoud отдельно выделяет **artifacts** как показатель semantic richness модели.

По OMG: data objects и messages — часть полной картины процесса, не только tasks.

**Для промпта:** «для каждой userTask укажи dataObject где уместно» (из `07-how-we-use-this-for-ai.md` Ayad).

---

## Ограничение конвертера XPDL

`tools/bpmn_to_xpdl.py` **пропускает** dataObject, dataObjectReference, association при конвертации.

Диаграмма в Bizagi может **потерять** документы на краях. Проверять вручную после import.

---

## Information flow vs Workflow

Song et al. (pMeta-BPMN) разделяют:

- **workflow** — sequence of activities (BPMN core);
- **information flow** — movement of data/documents (data objects, messages).

BPMN покрывает оба **качественно**. pMeta-BPMN добавляет **вероятности** (не в scope проекта).
