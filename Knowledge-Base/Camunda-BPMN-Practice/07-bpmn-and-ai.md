# BPMN и искусственный интеллект (Camunda + проект)

Источники: camunda.com/bpmn (AI-readable), Ayad 2024 (minority), System Prompt.

---

## Camunda: BPMN и LLM

На странице camunda.com/bpmn явно указано:

> **AI-readable and AI-writable** — LLMs can read and generate BPMN.

Это **industry validation** подхода диплома: не эксперимент «в вакууме», а следование направлению открытого стандарта.

---

## Три уровня использования ИИ

### Уровень 1. Generation (основной в проекте)

**Вход:** текстовое описание + `System Prompt/SystemPrompt.md` + контекст из OMG/Camunda KB.

**Выход:** полный BPMN 2.0 XML.

**Примеры:** test3, test4, testx.

**Ограничение:** validate in Modeler; fix gateways, layout.

---

### Уровень 2. Semantic enhancement (Ayad — minority)

**Вход:** существующая модель (lanes, activities, artifacts).

**Выход:** список недостающих элементов (не XML redraw).

**Шаблоны:** `Ayad-Alsayoud-2024/08-prompt-templates.md`.

**Пример:** testx.bpmn → предложения approve/reject/audit.

---

### Уровень 3. Uncertainty discussion (Song — minority)

**Вход:** список activities.

**Выход:** qualitative VUCA analysis (не pMeta-BPMN math).

**Шаблоны:** `Song-et-al-2026/07-how-we-use-this-for-ai.md`.

---

## Почему нужна KB (OMG + Camunda), а не только статьи

| Без KB | С KB |
|--------|------|
| LLM inventing non-standard shapes | LLM uses OMG element names |
| Missing BPMNDI | Prompt requires DI |
| Wrong gateway semantics | Patterns from Camunda catalog |
| Overfocus on prompting papers | BPMN fundamentals first |

**Соотношение контекста для LLM:** ~80% OMG+Camunda, ~20% Ayad+Song.

---

## Рекомендуемый prompt stack

```
1. System Prompt (XML rules)
2. Snippet: OMG five categories OR Camunda pattern #N
3. Optional: 08-prompt-templates (enhancement only)
4. User: domain description (university / HR / etc.)
```

---

## Agentic orchestration (Camunda 2025+ messaging)

Camunda продвигает **ad-hoc subprocess** для AI agents **inside** governed BPMN (vs agents outside).

**Для диплома:** optional future — текущие models deterministic + service tasks; agents not deployed.

---

## Quality gates для AI output

1. **XML parse** — automated (41 files OK in project).
2. **Modeler import** — visual.
3. **OMG checklist** — gateways, ends, refs (manual).
4. **Camunda style** — naming, crossings (manual).
5. **Domain expert** — university/HR rules (manual).

---

## Честное позиционирование

- ИИ **ускоряет** drafting и exploration.
- **Стандарт BPMN** (OMG/Camunda) **ограничивает** hallucinations.
- **Статьи** обосновывают research angle, не заменяют spec.

---

## Files in repo

| Role | Path |
|------|------|
| Generation contract | `System Prompt/SystemPrompt.md` |
| Enhancement templates | `Ayad.../08-prompt-templates.md` |
| OMG reference KB | `BPMN-OMG-Official/` |
| Practice KB | `Camunda-BPMN-Practice/` |
| Outputs | `Output/*.bpmn` |
