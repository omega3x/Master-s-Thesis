# Паттерны оптимизации (Camunda + проект)

Синтез Camunda examples и моделей `Output/`, `XML код/`.

---

## Принцип

**Оптимизация** = изменение структуры process model для:

- меньшего времени (latency);
- меньше manual work;
- меньше errors;
- лучше compliance / audit;
- лучше maintainability.

Camunda не sells «optimizer tool» — patterns **встроены в BPMN**.

---

## Pattern A: Parallelize independent work

**Источник:** parallel gateway + batch thinking

| Before | After |
|--------|-------|
| Check A → Check B | Parallel split → A, B → join |

**Cases:** test3 (ERP+LMS), табельныйучёт1 (3 analyses).

**Metric (simulation):** cycle time ↓.

---

## Pattern B: Automate integration steps

**Источник:** service task vs user task

Replace «human logs into LMS» with «service pulls from LMS API».

**Cases:** Pull grades, Verify debts, Generate PDF.

---

## Pattern C: Externalize business rules

**Источник:** Business Rules pattern (image1 vs image2)

DMN / rule engine вмест of XOR tree in diagram.

**Cases:** GPA check, graduation requirements.

---

## Pattern D: SLA with escalation

**Источник:** Two Step Escalation (image17–19)

Boundary timer + escalation user task.

**Cases:** 5-day chair sign → dean.

---

## Pattern E: Explicit rejection path

**Источник:** Additional Info + good XOR naming

Not eligible → notify → end rejected.

**Gap:** test4 needs reject branch on GPA gateway.

---

## Pattern F: Subprocess decomposition

**Источник:** Monthly invoicing pools + HR tabely

Main process stays readable; detail in call/embedded subprocess.

**Cases:** Registry subprocess, табельныйучёт1 via callActivity.

---

## Pattern G: Post-completion parallel actions

**Источник:** enterprise orchestration practice

After main deliverable: notify || audit log → join → end.

**Case:** test3 post-issuance gateway pair.

---

## Pattern H: Document / data visibility

**Источник:** data objects on diagram

Shows **information flow** for completeness (links to Ayad artifacts, Song info flow).

**Cases:** transcript, diploma, табели, ведомости.

---

## As-Is vs To-Be narrative (диплом)

### Scholarship (test4) — baseline

Linear, minimal automation depth, incomplete gateway.

### Diploma (test3) — optimized target

Parallel validation, rules, SLA, subprocess, audit, data objects, lanes.

### Tabely — administrative ground truth

Real domain, parallel HR, cross-department lanes.

---

## Quantitative optimization (future)

| Tool | What it measures |
|------|------------------|
| Bizagi Simulation | Time, cost per path |
| Camunda Optimize | Runtime duration |
| pMeta-BPMN (Song) | Uncertainty (not implemented) |

Current repo: **structural** optimization documented; numbers need simulation run.

---

## AI role in optimization

| AI can | AI cannot (alone) |
|--------|-------------------|
| Draft to-be model with patterns | Know real SLA without analyst |
| Suggest missing steps (Ayad) | Replace simulation |
| Apply patterns from this catalog | Guarantee correct gateway branches |

**Workflow:** As-Is description → LLM + this KB + System Prompt → To-Be BPMN → human review → Modeler → optional simulation.
