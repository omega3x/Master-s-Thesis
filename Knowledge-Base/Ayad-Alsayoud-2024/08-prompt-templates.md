# Шаблоны промптов (на основе Ayad & Alsayoud, 2024)

Использовать для **semantic enhancement** — когда модель уже есть.  
Не заменяют `System Prompt/SystemPrompt.md` для генерации XML.

---

## Подготовка контекста

Перед любым промптом соберите:

```
Process name: [имя]
Lanes: [роль1, роль2, ...]
Activities: [список]
Artifacts: [data objects, документы]
```

Источники в репозитории:

- ручной просмотр `.bpmn` / `.xpdl`
- CSV после `Parsing_xml.py` (для XPDL)

---

## Template 1: Zero-shot

```
You are a senior business process analyst.

Task: Improve SEMANTIC QUALITY of an existing process model.
Do NOT generate BPMN XML or XPDL. Do NOT draw a diagram.
Only suggest MISSING activities and artifacts.

Process name: {{PROCESS_NAME}}

Current lanes:
{{LANES}}

Current activities:
{{ACTIVITIES}}

Current artifacts:
{{ARTIFACTS}}

Return:
1. Missing activities (name, lane, reason)
2. Missing artifacts (name, linked activity, reason)
3. Top 3 highest-impact additions
```

---

## Template 2: Few-shot

```
You are a business process analyst improving semantic completeness.

EXAMPLE (hospitalization domain):
- Missing activity: "Verify insurance coverage" → Lane: Secretary
- Missing artifact: "Insurance card copy" → linked to registration
- Reason: registration cannot proceed without insurance validation

Now analyze MY process in the SAME output format.

Process name: {{PROCESS_NAME}}
Lanes: {{LANES}}
Activities: {{ACTIVITIES}}
Artifacts: {{ARTIFACTS}}

Suggest 5 missing activities and 3 missing artifacts.
```

---

## Template 3: Chain-of-Thought

```
Improve the semantic quality of a business process model.
Think step by step before giving final recommendations.
Do NOT output BPMN or XPDL code.

Step 1 — Domain: identify the industry and typical regulations.
Step 2 — Roles: list standard lanes for this domain.
Step 3 — Gap analysis: compare standard roles vs current lanes.
Step 4 — Activities: per role, list typical activities missing from the model.
Step 5 — Artifacts: documents/data each activity should produce or consume.
Step 6 — Prioritize: rank suggestions by impact on completeness.

Current model:
Process: {{PROCESS_NAME}}
Lanes: {{LANES}}
Activities: {{ACTIVITIES}}
Artifacts: {{ARTIFACTS}}

Output Steps 4–6 only, in clear bullet lists.
```

---

## Template 4: Feedback loop (из статьи)

После первого ответа LLM:

```
I accept suggestions #1 and #3. I reject #2 because [reason].
Refine the remaining suggestions for my process context: {{DOMAIN}}.
Do not repeat rejected items.
```

---

## Пример заполнения для testx

```
Process name: testx
Lanes: none
Activities: Start, Review request, Done
Artifacts: none
```

Ожидаемые типы предложений LLM:

- Approve request (manager)
- Reject request (exception path)
- Request form (artifact)
- Audit log entry (artifact)

---

## Связь с генерацией BPMN

| Задача | Файл промпта |
|--------|--------------|
| Дополнить смысл модели | Этот файл (08) |
| Сгенерировать BPMN XML | `System Prompt/SystemPrompt.md` |
| Получить XPDL | `python tools/bpmn_to_xpdl.py` |

Сначала enhancement (08) → потом обновление модели → потом generation/conversion.
