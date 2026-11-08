# Conformance и семантика (OMG)

Источник: OMG BPMN 2.0, глава 2 Conformance.

---

## Четыре типа conformance

| Тип | Назначение |
|-----|------------|
| **Process Modeling** | Рисование и семантика диаграмм |
| **Process Execution** | Исполнение по BPMN execution semantics |
| **BPEL Process Execution** | Mapping и исполнение через BPEL |
| **Choreography Modeling** | Моделирование choreography |

Tool может заявлять **один или несколько** типов. Полный — **BPMN Complete Conformance** (все четыре).

---

## Process Modeling Conformance

Tool **должен** поддерживать packages:

- Infrastructure, Foundation, Common, Service (Chapter 8);
- Process, Activities, Data, Human Interaction (Chapter 10);
- Collaboration: pools, message flow (Chapter 9);
- Conversation diagrams (Chapter 9).

**Не обязан** поддерживать choreography modeling для claim Process Modeling.

---

## Подклассы Process Modeling

| Подкласс | Для кого | Охват |
|----------|----------|-------|
| **Descriptive** | High-level аналитики, flowchart tools | Минимальный видимый набор |
| **Analytic** | Анализ процессов | ~половина full class |
| **Common Executable** | Исполняемые модели | Нужное для execution |

### Descriptive включает (примеры)

participant (pool), lane, sequenceFlow, messageFlow, exclusiveGateway, parallelGateway, userTask, serviceTask, subProcess, callActivity, dataObject, start/end events, message/timer start events.

**Наши AI-модели** близки к **Common Executable** + Descriptive visual set.

---

## Process Semantics

Implementation, интерпретирующая diagram как process, **должна** быть consistent с Chapter 10.

**Process Modeling conformance НЕ требует** execution semantics (Chapter 13).

Camunda Modeler = modeling; Camunda Engine = execution (отдельный conformance).

---

## Token semantics (учебная модель)

- Start → создаёт token;
- Activity → token входит, ждёт completion, token выходит;
- XOR split → один token на одну ветвь;
- AND split → token копируется на каждую ветвь;
- AND join → ждёт все tokens;
- End → уничтожает token.

Помогает **проверять логику** AI-сгенерированных gateway.

---

## Structural Conformance

- Каждый sequence flow имеет valid source/target;
- Flow objects связаны корректно;
- Нет orphan elements;
- Gateway split/join согласованы.

**Типичные ошибки AI:**

- gateway без второй ветви;
- task без incoming или outgoing;
- broken reference id.

---

## Visual Interchange Conformance

Diagram layout переносится через BPMN DI. Tool claiming visual interchange должен сохранять bounds/edges.

---

## ISO/IEC 19510

BPMN 2.0 от OMG опубликован как **ISO/IEC 19510:2013**.

Camunda на сайте указывает: BPMN is ISO-ratified open standard.

Для диплома: можно ссылаться и на OMG, и на ISO как на **международное** признание нотации.

---

## Что это значит для проекта

| Компонент | Conformance |
|-----------|-------------|
| Output/*.bpmn | Стремление к Process Modeling + DI |
| Camunda import | De-facto validation |
| bpmn_to_xpdl.py | Partial mapping, не full OMG |
| LLM generation | Human review обязателен |

Мы **не заявляем** полную OMG Complete Conformance — учебный/research prototype.
