# Core BPMN elements — практическое руководство (Camunda)

Источник: camunda.com/bpmn + согласование с OMG.

---

## Task (задача)

**Единица работы.**

| Подтип | Практика |
|--------|----------|
| User Task | Человек в task list (approval, review) |
| Service Task | API, microservice, integration |
| Business Rule Task | DMN / rule engine |
| Manual Task | Вне BPMS |
| Script Task | Inline automation |

**Camunda tip:** не смешивать «человеческую» работу вне системы (manual) с user task в portal.

---

## Gateway (шлюз)

**Точка решения или синхронизации.**

| Тип | Когда |
|-----|-------|
| Exclusive XOR | «Или-или»: approved / rejected |
| Parallel AND | Независимые ветки одновременно |
| Inclusive OR | Несколько optional paths |
| Event-based | Ждём первое из событий |

**Практика:** у XOR **всегда** label-вопрос и named outgoing flows.

---

## Event (событие)

| Тип | Практика |
|-----|----------|
| Start | Trigger процесса |
| End | Итог (success / fail) |
| Intermediate | Wait, signal, timer mid-flow |
| Boundary | SLA, timeout на task |

---

## Sequence flow

Порядок **внутри** process. Условие на стрелке после XOR.

---

## Pools & Lanes

- **Pool** — участник (организация, система).
- **Lane** — роль внутри pool.

Four Eyes: отдельные pools для approvers + message flows.

---

## Data

Data objects на diagram показывают **какие документы** участвуют. Не заменяют data modeling.

---

## Минимальный набор для 80% процессов

Camunda: productive за **один день** обучения с:

- start / end
- userTask, serviceTask
- exclusiveGateway, parallelGateway
- sequenceFlow
- lanes (optional)

Наш `test4.bpmn` — почти этот минимум.  
`test3.bpmn` — расширенный enterprise set.

---

## Mapping на файлы проекта

| Element | testx | test4 | test3 |
|---------|-------|-------|-------|
| userTask | ✓ | ✓ | ✓ |
| serviceTask | | ✓ | ✓ |
| businessRuleTask | | ✓ | ✓ |
| scriptTask | | | ✓ |
| exclusiveGW | | ✓ | ✓ |
| parallelGW | | | ✓ |
| subprocess | | | ✓ |
| boundary timer | | | ✓ |
| lanes | | | ✓ |
| dataObject | | | ✓ |

---

## Import checklist (Camunda Modeler / bpmn.io)

1. File opens without parse error?
2. All shapes visible (DI present)?
3. Gateways have 2+ meaningful outgoing where needed?
4. Every task has incoming and outgoing?
5. Labels readable (naming conventions)?

System Prompt нацелен на прохождение пунктов 1–4 автоматически; 5 — partial.
