# Как мы используем эту базу для ИИ и диплома

## Зачем Song et al. в нашем проекте

Ayad (2024) отвечает на вопрос: **«Чего не хватает в модели по смыслу?»**

Song (2026) отвечает на вопрос: **«Где неопределённость и насколько сильны зависимости?»**

Обе статьи усиливают аргументацию диплома про **AI-assisted BPM**, но на разных уровнях.

---

## Текущий scope нашего репозитория

| Делаем сейчас | Не делаем сейчас (Song et al.) |
|---------------|-------------------------------|
| Генерация BPMN (LLM) | Probability annotations |
| Конвертация XPDL | Activity dependency table |
| Semantic enhancement (Ayad) | Information dependency table |
| Визуальная проверка в modeler | Meta graph algebra |

Это **нормально** для MVP диплома — важно уметь **объяснить границу**.

---

## Как подключить идеи Song к LLM (без pMeta-BPMN tool)

### Промпт: qualitative uncertainty check

```
Analyze this BPMN process for sources of uncertainty (VUCA).
Do NOT generate XML.

For each activity and gateway list:
- workflow uncertainty (timing, failure, optional path)
- information uncertainty (missing data, incorrect document)
- suggested probability estimate range (low/medium/high) if domain knowledge allows

Process: [paste activity list from testx or diploma model]
```

### Промпт: dependency brainstorming

```
Based on the activity list below, propose an activity dependency table
(qualitative, not numerical). Format: Activity A → Activity B | dependency type | reason.

Then propose an information dependency table for data objects mentioned.

This is inspired by pMeta-BPMN (Song et al. 2026) but qualitative only.
```

**Важно:** это **не замена** pMeta-BPMN — это использование **идей статьи** для улучшения обсуждения с ИИ.

---

## Карта: статья → файлы репозитория

| Концепция Song | Где у нас |
|----------------|-----------|
| BPMN modelling | `Output/*.bpmn`, `System Prompt/` |
| Information flow | `XML код/табельныйучёт2.bpmn` (data objects) |
| Workflow logic | gateways в `test3.bpmn`, `graduate_diploma` |
| Quantitative uncertainty | `Knowledge-Base/Song-et-al-2026/` (теория) |
| XPDL / Bizagi | `XPDL/Output/` (не pMeta, но практика преподавателя) |

---

## Roadmap (если спросят «что дальше?»)

1. Добавить **data objects** во все university models (information flow).
2. Экспертно задать **probability ranges** на gateway branches.
3. Построить **qualitative dependency tables** вручную или через LLM.
4. (Future) Реализовать pBPMN / Meta graph по полному PDF.

---

## Что сказать на защите (30 секунд)

> «Song et al. (2026) предлагают pMeta-BPMN: BPMN для логики workflow плюс Meta graph с вероятностями для information flow. Метод даёт количественные таблицы зависимостей активностей и данных — в отличие от чисто качественного анализа. Мы используем BPMN как основу моделирования; идеи uncertainty учитываем в knowledge base и при доработке моделей с LLM. Количественный pMeta-BPMN — направление развития после получения полного текста статьи.»
