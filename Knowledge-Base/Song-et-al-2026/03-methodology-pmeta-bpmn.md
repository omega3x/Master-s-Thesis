# Методология pMeta-BPMN

## Общая схема (по abstract + CIMS 2025)

```
Классический BPMN (логика процесса + информационные связи)
        ↓
┌───────────────────────────────────────────────────────┐
│  Слой 1: Probabilistic BPMN (pBPMN)                   │
│  — вероятности на workflow                            │
│  — activity dependency (зависимость активностей)    │
│  — activity dependency table (таблица зависимостей) │
└───────────────────────────────────────────────────────┘
        ↓
┌───────────────────────────────────────────────────────┐
│  Слой 2: Information probability Meta graph         │
│  — явное выражение information flow из BPMN         │
│  — преобразование в Meta graph с вероятностями        │
│  — information dependency table                       │
└───────────────────────────────────────────────────────┘
        ↓
Количественный анализ неопределённости
(зависимости, ресурсы, «ликвидность»/circulation процесса)
        ↓
Пилот: logistic case
```

## Принцип интеграции

| Компонент | Роль | Тип анализа |
|-----------|------|-------------|
| **BPMN** | Символьная нотация, activity logic | Качественный (qualitative) |
| **Meta graph** | Алгебраическая структура информационных элементов | Количественный (quantitative) |
| **Probability theory** | Математическая основа неопределённости | Количественный |

**Ключевая формула идеи (словами):**

> Qualitative modelling (BPMN) + Quantitative analytics (Meta graph) + Probability = pMeta-BPMN

## Шаг 1. Probabilistic BPMN (pBPMN)

По связанной публикации CIMS 2025:

1. Расширить BPMN с помощью **теории вероятностей**.
2. Определить **activity dependency** (зависимость между активностями).
3. Выполнить **reasoning** (логический вывод) → получить **activity dependency table**.

**Смысл:** не просто «A идёт перед B», а «с какой вероятностной/зависимой силой A влияет на B» в условиях неопределённости.

## Шаг 2. Information probability Meta graph

1. **Явно выразить information flow** сервисного/BPMN-процесса.
2. **Преобразовать** в information probability Meta graph.
3. **Вычислить** **information dependency table**.

**Смысл:** данные и документы в процессе тоже несут неопределённость — кто от кого зависит, насколько надёжен информационный поток.

## Шаг 3. Совместный анализ

pMeta-BPMN объединяет преимущества:

| BPMN | Meta graph |
|------|------------|
| Моделирование логики активностей | Аналитика информационных элементов |
| Понятен аналитикам | Алгебраическая строгость |
| Стандарт OMG | Подходит для dependency analysis |

Результат: анализ **dependency of activities and information** → улучшение process analysis towards uncertainty.

## Шаг 4. Практическая валидация

- **Logistic case** — пилот.
- Оценка usability и advantage метода.
- Поддержка анализа: resource allocation, activity dependence, circulation/liquidity в процессе (по CIMS abstract).

## Отличие от обычного BPMN в нашем проекте

Наши файлы (`Output/testx.bpmn`, `XPDL/Output/testx.xpdl`):

- описывают **детерминированную** логику (sequence flows, gateways);
- **не содержат** probability annotations;
- **не строят** dependency tables.

pMeta-BPMN — **следующий уровень анализа**, если преподаватель спросит про uncertainty quantification.
