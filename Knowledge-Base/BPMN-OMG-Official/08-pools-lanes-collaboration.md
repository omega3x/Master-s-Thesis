# Пулы, дорожки и коллаборация (OMG)

Источник: OMG BPMN 2.0, глава 9 Collaboration.

---

## Pool (бассейн / участник)

**Pool** представляет **участника** в collaboration:

- организацию;
- отдел;
- внешнего партнёра;
- систему (иногда).

Pool может содержать:

- **Process** (детализированный поток);
- **пустой** pool (black box — только сообщения снаружи);
- **Choreography** между pools.

---

## Lane (дорожка)

**Lane** — подразделение **внутри одного pool** для показа ответственности.

| Свойство | Значение |
|----------|----------|
| Организационный смысл | Кто выполняет задачи в lane |
| Семантика исполнения | **Не меняет** token semantics |
| Вложенность | Lane может содержать child lanes |

**Пример `test3.bpmn`:**

- Lane_Student — Student Office
- Lane_Academic — Academic Department  
- Lane_Registry — Registry and Archive

**Пример `табельныйучёт2.bpmn`:**

- подразделение
- кадровая служба

---

## Participant

В XML collaboration **participant** связывает pool с processRef.

При private process в одном pool lanes достаточно для ролей.

---

## Message Flow между pools

```
Pool A (Customer)  ----message---->  Pool B (Supplier)
         |                                  |
    [process inside]                  [process inside]
```

- Sequence flow **не пересекает** границу pool.
- Message flow **пересекает** границу.

Four Eyes (Camunda): отдельные pools для Process Engine, 1st Approver, 2nd Approver.

---

## Black Box Pool

Pool **без** раскрытого process — только message flows на границе.

Используется когда **внутренность** партнёра неизвестна или не важна.

---

## Collaboration vs Private Process

| Аспект | Private Process | Collaboration |
|--------|-----------------|---------------|
| Фокус | Внутренний поток | Взаимодействие участников |
| Pools | Один (обычно) | Два и более |
| Основной поток | Sequence flow | Message flow + processes |

---

## Оптимизация через swimlanes

1. **Ясность ответственности** — сразу видно, кто должен автоматизировать шаг.
2. **Выявление лишних handoffs** — частые переходы между lanes = кандидаты на объединение или automation.
3. **Parallel work** — задачи в разных lanes часто можно parallelize.

---

## Для AI и XML

System Prompt требует «realistic swimlanes». OMG: каждый flowNodeRef в lane должен ссылаться на реальный id элемента. BPMN DI: отдельные BPMNShape для lanes с bounds.

Конвертер `bpmn_to_xpdl.py` переносит lanes в XPDL Pools/Lanes для Bizagi.
