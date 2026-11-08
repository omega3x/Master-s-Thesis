# Как OMG BPMN используется в нашем проекте

---

## Соответствие файлов проекта элементам OMG

| OMG concept | Файл проекта |
|-------------|--------------|
| Private executable Process | `Output/test3.bpmn`, `test4.bpmn` |
| Lanes | `test3.bpmn`, `XML код/табельныйучёт2.bpmn` |
| Parallel gateway | `test3.bpmn`, `табельныйучёт1.bpmn` |
| Exclusive gateway + conditions | `test3.bpmn` |
| Inclusive gateway | `табельныйучёт2.bpmn` |
| Embedded subprocess | `Subprocess_Registry` in test3 |
| Call activity | `табельныйучёт2.bpmn` |
| Boundary timer | `test3.bpmn` |
| Data objects | test3, табельный учёт |
| Business rule task | test3, test4 |
| Service / user / script tasks | test3 |
| BPMN DI (shapes, edges) | все Output/*.bpmn |

---

## System Prompt как «контракт OMG-lite»

`System Prompt/SystemPrompt.md` переводит требования OMG в инструкции для LLM:

- full `bpmn:definitions`;
- executable process;
- BPMNDiagram + shapes + edges;
- valid refs;
- enterprise patterns (parallel, approval, timer, subprocess, lanes).

**Не покрывает:** full choreography, full ISO conformance testing.

---

## Reference library (30 Camunda diagrams)

`BPMN/xml/image1.bpmn` … `image30.bpmn` — упрощённые **Descriptive** models по мотивам OMG/Camunda examples.

`generate_bpmn.py` — linear subset, не full multi-pool OMG examples.

---

## XPDL bridge

Преподаватель / Bizagi: XPDL 2.2.

OMG primary interchange — BPMN XML. Мы конвертируем:

```
BPMN (OMG semantic + DI) → XPDL (Bizagi)
```

См. `tools/bpmn_to_xpdl.py`, ограничения в `XPDL/README.md`.

---

## Gaps (честно)

| OMG / best practice | Статус в проекте |
|---------------------|------------------|
| Reject path на все XOR | test4 — gap |
| Message flows / multi-pool | упрощено в image*.bpmn |
| Choreography | не моделируется |
| Full data associations in XPDL | converter skip |
| Execution conformance | не deployed engine |

---

## Рекомендуемый narrative для защиты

1. **Стандарт:** BPMN 2.0 OMG / ISO 19510 — основа.
2. **Практика:** Camunda patterns — как оптимизировать.
3. **Инструмент:** LLM + System Prompt — ускорение drafting.
4. **Статьи:** Ayad (semantic), Song (uncertainty) — **дополнение**, ~20% обоснования.

---

## Что читать перед правкой моделей

1. OMG `04`–`07` (elements, events, tasks, gateways)
2. OMG `13` (optimization)
3. Camunda `04-patterns`, `06`
4. System Prompt
5. Ayad templates — только для enhancement, не для замены OMG rules
