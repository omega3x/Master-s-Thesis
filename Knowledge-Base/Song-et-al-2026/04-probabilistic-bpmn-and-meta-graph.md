# Probabilistic BPMN и Meta graph — два слоя метода

## Зачем два слоя

Неопределённость в процессе бывает **двух типов**:

| Тип | Пример | Слой pMeta-BPMN |
|-----|--------|-----------------|
| **Workflow uncertainty** | Задача B может не выполниться / выполнится с задержкой | pBPMN |
| **Information uncertainty** | Документ X приходит неполным / с ошибкой | Info probability Meta graph |

Классический BPMN хорошо показывает **структуру**, но слабо **квантифицирует** оба типа.

---

## Слой 1: Probabilistic BPMN (pBPMN)

### Что добавляется к BPMN

- **Probability theory** — вероятностная интерпретация элементов workflow.
- **Activity dependency** — формальное понятие зависимости между активностями.
- **Activity dependency table** — табличный результат анализа (reasoning).

### Что можно анализировать (по CIMS abstract)

- Какие активности **критически зависят** друг от друга
- Где неопределённость workflow **наиболее высока**
- Основа для **resource allocation** (распределение ресурсов)

### Связь с обычным BPMN

```
Обычный BPMN:     Start → Task A → Gateway → Task B → End
pBPMN:            те же элементы + вероятности/зависимости на переходах и активностях
```

В литературе по stochastic BPMN (sBPMN) похожие идеи: аннотация likelihood of occurrence на элементах. pMeta-BPMN — **своя интеграция** с Meta graph, не просто sBPMN.

---

## Слой 2: Information probability Meta graph

### Meta graph (общая идея)

**Meta graph** — формальный граф для моделирования и анализа **информационных элементов** процесса с алгебраическими операциями.

В pMeta-BPMN к Meta graph добавляются **вероятности** → **information probability Meta graph**.

### Pipeline (по CIMS abstract)

1. Из BPMN **явно извлечь information flow** (data objects, message flows, документы между задачами).
2. **Преобразовать** в Meta graph representation.
3. **Вычислить information dependency** → **information dependency table**.

### Что можно анализировать

- Зависимости между **информационными элементами**
- Узкие места в **потоке данных**
- «Circulation» / ликвидность информации в процессе

---

## Две таблицы — два выхода метода

| Таблица | Источник | Содержание |
|---------|----------|------------|
| **Activity dependency table** | pBPMN | Зависимости активностей (workflow) |
| **Information dependency table** | Info probability Meta graph | Зависимости информационных элементов |

Вместе они дают **holistic** картину — то, чего не хватает качественным методам.

---

## Сравнение с нашим репозиторием

| Элемент | Наш проект | pMeta-BPMN |
|---------|------------|------------|
| BPMN XML | ✓ `Output/*.bpmn` | Вход для pBPMN |
| Data objects | Иногда (табельный учёт) | Вход для Meta graph |
| Вероятности | ✗ | ✓ Core |
| Dependency tables | ✗ | ✓ Output |
| XPDL для Bizagi | ✓ | Не фокус статьи |

**Вывод:** наш проект = **моделирование**. Song et al. = **количественный анализ неопределённости** поверх модели.
