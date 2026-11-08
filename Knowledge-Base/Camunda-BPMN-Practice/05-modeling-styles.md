# Стиль моделирования BPMN (Camunda)

Источник: `BPMN/02-bpmn-modeling-styles/`

---

## Зачем стиль важен

Две диаграммы могут быть **семантически одинаковы**, но одна — trusted business analyst'ом, другая — ignored.

Camunda с 2007 учит BPMN: **layout и naming** — часть качества модели.

---

## 1. Avoid Crossing Flows

**Файлы:** `01-avoid-crossing-flows.md`, image20–21

| Good | Counter |
|------|---------|
| Минимум пересечений линий | Линии пересекают друг друга |

**Практика:** reorder tasks или использовать промежуточные gateways.

**Для AI:** System Prompt требует «avoid overlapping shapes» — та же идея.

**Проблема LLM:** auto-layout часто даёт crossings — нужна ручная правка в Modeler.

---

## 2. Naming Conventions

**Файл:** `02-naming-conventions.md`, image22–24

| Element | Convention |
|---------|--------------|
| **Start Event** | Trigger (что запустило) |
| **End Event** | Object + past participle (результат) |
| **Task** | Object + verb (действие) |
| **XOR Gateway** | Question |
| **Outgoing flows** | Answers / conditions |
| **Pool** | Process name + role |

**Counter examples:** «Start», «End», «Checking», generic labels.

**Применение:** labels в `test3.bpmn` на английском enterprise style; табельный учёт — русские labels из предметной области.

---

## 3. Symmetric Modeling

**Файл:** `03-symmetric-modeling.md`, image25–28

Ветви после gateway должны быть **симметричны** по структуре и размеру.

- XOR «desired dish?» → salad branch и pasta branch **одинаковой глубины**.
- Order value gateway → branches balanced.

**Урок:** asymmetry = harder to read and maintain.

---

## 4. Use Equal Task Sizes

**Файл:** `04-use-equal-task-sizes.md`, image29–30

| Good | Counter |
|------|---------|
| «evaluate document» + «submit decision» | Одна giant task «evaluate and submit» |

**Урок:** granularity = один task = один logical step.

Слишком мелко — шум. Слишком крупно — скрытая логика.

---

## Checklist перед сдачей диаграммы

- [ ] У каждого symbol есть label
- [ ] Tasks: verb + object
- [ ] Gateways: question + named branches
- [ ] Минимум crossing flows
- [ ] Symmetric branches где возможно
- [ ] Equal task granularity

---

## Для промпта ИИ

Добавить в user message:

```
Follow Camunda modeling style: named gateways as questions,
tasks as object+verb, symmetric branches, minimize line crossings.
```

Или расширить System Prompt (optional, см. Ayad `07-how-we-use-this-for-ai.md`).

---

## Связь с оптимизацией

Читаемая модель **легче оптимизируется**: analyst видит лишние handoffs, asymmetry, missing reject paths.

Плохой layout ≠ wrong process, но мешает review — а review обязателен при AI generation.
