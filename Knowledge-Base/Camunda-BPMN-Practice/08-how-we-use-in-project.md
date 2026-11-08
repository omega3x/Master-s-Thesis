# Camunda materials в нашем репозитории

---

## Локальный архив

| Path | Content |
|------|---------|
| `BPMN/00-overview.md` | Index Camunda examples |
| `BPMN/01-bpmn-examples/` | 8 pattern articles |
| `BPMN/02-bpmn-modeling-styles/` | 4 style guides |
| `BPMN/images/` | 30 SVG diagrams |
| `BPMN/xml/` | 30 BPMN + `generate_bpmn.py` |

Imported May 2026 from camunda.com/bpmn/examples.

---

## Как KB связана с кодом

| KB file | Repo artifact |
|---------|---------------|
| `04-patterns-catalog.md` | `01-bpmn-examples/*.md` |
| `05-modeling-styles.md` | `02-bpmn-modeling-styles/*.md` |
| `06-optimization-patterns.md` | `Output/test3.bpmn` vs test4 |
| `03-core-elements` | element usage in Output/XML код |

---

## Tools

| Tool | Role |
|------|------|
| Camunda Modeler / bpmn.io | View AI BPMN |
| `generate_bpmn.py` | Regenerate reference XML |
| `bpmn_to_xpdl.py` | Bizagi path |

Camunda **Platform** (Zeebe cluster) — **not** bundled; repo is notation-focused.

---

## Demo flow for supervisor

1. Open `BPMN/01-bpmn-examples/03-four-eyes-principle.md` — pattern theory.
2. Open `Output/test3.bpmn` in bpmn.io — AI optimized process.
3. Show `Knowledge-Base/Camunda-BPMN-Practice/` — structured notes.
4. Mention OMG KB as primary standard reference.
5. Brief Ayad/Song — AI research context only.

---

## Maintenance

При обновлении Camunda examples online — re-import SVG/BPMN and refresh pattern catalog table.

При изменении Output models — update `06-optimization-patterns.md` as-is/to-be table.
