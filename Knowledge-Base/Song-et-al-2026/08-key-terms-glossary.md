# Словарь терминов (для ИИ и презентации)

Краткие определения по Song et al. (2026) и связанной литературе. Используйте как контекст при промптах.

---

## pMeta-BPMN

**Probabilistic Meta-BPMN** — интегрированный метод моделирования и анализа неопределённости в BPM через BPMN + Meta graph + теорию вероятностей.

---

## VUCA

**V**olatility, **U**ncertainty, **C**omplexity, **A**mbiguity — рамка для обоснования необходимости вероятностного анализа процессов.

---

## Workflow / Control flow

Порядок выполнения активностей: start events, tasks, gateways, sequence flows. В BPMN — основная диаграмма процесса.

---

## Information flow / Dataflow

Поток данных и документов между активностями: data objects, message flows, артефакты. В pMeta-BPMN анализируется отдельно от control flow.

---

## Probabilistic BPMN (pBPMN)

Расширение BPMN вероятностной интерпретацией workflow. Выход: **activity dependency table**.

---

## Meta graph

Формальный граф с алгебраическими операциями для анализа информационных элементов процесса. В pMeta-BPMN — с вероятностями.

---

## Information probability Meta graph

Meta graph, где информационные элементы и связи имеют вероятностные характеристики. Выход: **information dependency table**.

---

## Activity dependency

Степень/характер зависимости одной активности от другой в условиях неопределённости workflow.

---

## Information dependency

Степень/характер зависимости информационных элементов (документов, данных) друг от друга.

---

## Activity dependency table

Табличный результат reasoning по pBPMN — зависимости между активностями.

---

## Information dependency table

Табличный результат вычислений по information probability Meta graph.

---

## Qualitative vs quantitative analysis

| Qualitative | Quantitative |
|-------------|--------------|
| Правила, эвристики | Вероятности, таблицы, числа |
| «Путь может сорваться» | «P(delay) = 0.23» |
| Типично в BPMN-ревью | Цель pMeta-BPMN |

---

## Semantic quality (Ayad 2024) vs Uncertainty (Song 2026)

| | Ayad | Song |
|-|------|------|
| Фокус | Полнота концепций | Неопределённость |
| Метод | LLM prompts | Probability + Meta graph |
| Вопрос | «Чего не хватает?» | «Насколько неопределённо?» |

---

## sBPMN (смежная работа, не pMeta-BPMN)

**Stochastic BPMN** — BPMN с likelihood of occurrence на элементах. Близкая тема, другой formalism. Song et al. интегрируют Meta graph — это их отличие.
