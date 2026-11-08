# Результаты, новизна и ограничения

## Findings (по abstract BPMJ 2026)

1. **pMeta-BPMN интегрирует** технические framework'и BPMN и Meta graph.

2. **Сочетаются сильные стороны:**
   - BPMN → activity logic modelling
   - Meta graph → information element analytics

3. Метод **доступен на практике** (availability) для:
   - моделирования uncertain business processes;
   - анализа dependency activities + information;
   - улучшения process analysis towards uncertainty.

4. **Logistic case** подтверждает usability и advantage.

## Findings (дополнительно из CIMS 2025 abstract)

- Метод **эффективен** для quantitative analysis uncertain service processes.
- Даёт поддержку анализа:
  - **resource allocation**
  - **activity dependence**
  - **circulation / liquidity** в процессе

## Originality / value

### Пробел в литературе (по авторам)

| Было | Стало с pMeta-BPMN |
|------|-------------------|
| Качественный анализ (pre-defined rules) | + Количественный (probability) |
| Workflow OR dataflow отдельно | Workflow AND information flow вместе |
| Нет specific quantitative results | Математически обоснованные таблицы зависимостей |

### Научный вклад

Заполнение gap: **holistic method** для modelling + analysis process uncertainty с **mathematical probability** по обоим потокам.

## Ограничения (честно, по доступной информации)

Из публичного abstract **нельзя** утверждать:

- точные формулы вероятностей;
- размер logistic case;
- сравнение с конкретными конкурентами (sBPMN, Petri nets, etc.).

**Вероятные ограничения** (логически следуют из метода):

1. Требует **оценки вероятностей** — откуда брать P? (эксперт, исторические данные)
2. Сложнее обычного BPMN — нужна экспертиза в Meta graph
3. Пилот на **logistics** — переносимость на university processes требует проверки
4. Не заменяет **симуляцию Bizagi** напрямую — другой класс анализа

## Для защиты: как позиционировать

| Вопрос преподавателя | Ответ |
|---------------------|-------|
| «Вы учитываете uncertainty?» | Знаем метод pMeta-BPMN (Song 2026); наш scope — генерация BPMN/XPDL; quant analysis — future work |
| «Чем отличается от Ayad 2024?» | Ayad: semantic completeness через LLM. Song: uncertainty через probability |
| «Почему обычный BPMN?» | BPMN — стандарт моделирования; pMeta-BPMN — расширение для анализа |

## Связь двух статей в Knowledge-Base

```
Ayad 2024          Song 2026
    │                  │
    ▼                  ▼
Semantic quality   Uncertainty quantification
LLM prompts        Probability + Meta graph
Дополнить смысл    Измерить зависимости
    │                  │
    └────────┬─────────┘
             ▼
      Полноценный BPM lifecycle (идеал)
```
