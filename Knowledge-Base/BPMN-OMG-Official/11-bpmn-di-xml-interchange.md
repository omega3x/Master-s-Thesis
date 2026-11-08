# BPMN DI, XML и interchange (OMG)

Источник: OMG BPMN 2.0, глава 12 BPMN Notation and Diagrams / BPMN DI.

---

## Два слоя BPMN файла

| Слой | Содержание |
|------|------------|
| **Semantic (MODEL)** | Process, tasks, flows, gateways — **что** делает процесс |
| **Diagram Interchange (DI)** | Bounds, waypoints — **как** выглядит на экране |

Инструмент без DI может **импортировать логику**, но не расположение фигур.

---

## Корневой элемент

```xml
<bpmn:definitions>
  <bpmn:process>...</bpmn:process>
  <bpmndi:BPMNDiagram>...</bpmndi:BPMNDiagram>
</bpmn:definitions>
```

Namespace (BPMN 2.0):

- `http://www.omg.org/spec/BPMN/20100524/MODEL`
- `http://www.omg.org/spec/BPMN/20100524/DI`
- `http://www.omg.org/spec/DD/20100524/DC`
- `http://www.omg.org/spec/DD/20100524/DI`

---

## BPMNShape

Для каждого видимого элемента:

- `bpmnElement` — id элемента process;
- `dc:Bounds` — x, y, width, height.

Без Bounds элемент **невидим** в modeler.

---

## BPMNEdge

Для sequence flow и message flow:

- `bpmnElement` — id потока;
- `di:waypoint` — точки ломаной линии.

Некорректные waypoints = «ломаные» или пересекающиеся линии.

---

## Interchange между инструментами

**Цель BPMN 2.0 (Scope):** пользователь создаёт process в tool A и открывает в tool B **без потери** структуры и layout.

**Практика:** 100% interchange редок из-за extensions (Camunda, Bizagi). Core elements переносятся хорошо.

**Наш pipeline:**

```
LLM → BPMN XML (Camunda/bpmn.io)
     → bpmn_to_xpdl.py → XPDL (Bizagi)
```

BPMN остаётся **source of truth** (как в System Prompt).

---

## XSD и machine-readable spec

OMG публикует:

- BPMN20.xsd
- BPMNDI.xsd
- Semantic.xsd

Путь: https://www.omg.org/spec/BPMN/20100501/

Валидация XML по XSD — stricter check чем «открылось в modeler».

---

## Extensibility

BPMN 2.0 позволяет **extensions** (например `camunda:`, `modeler:`).

| Плюс | Минус |
|------|-------|
| Vendor features | Потеря при смене engine |
| Execution hints | Не в pure OMG interchange |

System Prompt использует Camunda Cloud 8.9 extensions — осознанный trade-off.

---

## Требования System Prompt vs OMG

| Требование | OMG | Наш промпт |
|------------|-----|------------|
| Full definitions | Да | Да |
| Executable process | Optional | isExecutable="true" |
| BPMNDI | Recommended | Обязательно |
| Unique IDs | Да | Да |
| sourceRef/targetRef | Да | Да |

---

## Проверка в проекте

41 BPMN/XPDL file прошли XML parse. Это **syntax**, не полная OMG conformance.

Рекомендуется: import в Camunda Modeler + visual review.
