# Пилотный кейс: Logistic case

## Что известно из abstract

Авторы применяют pMeta-BPMN к **логистическому бизнес-процессу** (logistic case), чтобы:

1. Показать **usability** (применимость метода).
2. Оценить **advantage** (преимущество перед качественными методами).

Детали кейса (названия задач, числа, диаграммы) — **в полном PDF**, недоступном в открытом доступе.

## Зачем логистика как пример

Логистика — классический домен с высокой **VUCA**-неопределённостью:

| Источник uncertainty | Пример |
|---------------------|--------|
| Workflow | Задержка доставки, срыв маршрута |
| Information | Неверный трекинг-номер, неполная накладная |
| Resources | Нехватка транспорта/склада |
| Dependencies | Задача B невозможна без данных от A |

pMeta-BPMN здесь уместен: и workflow, и information flow критичны.

## Что демонстрирует кейс (логика метода)

```
Logistic BPMN (качественная модель)
        ↓
pBPMN → activity dependency table
        ↓
Info probability Meta graph → information dependency table
        ↓
Выводы: где uncertainty максимальна, что оптимизировать
```

## Параллель с нашим проекту

| Song et al. — logistics | Наш репозиторий — university |
|-------------------------|------------------------------|
| Logistic case | Scholarship, diploma, timesheet |
| pMeta-BPMN analysis | BPMN + XPDL generation |
| Количественные таблицы | Качественные модели |

**Для презодавателя:** «Мы взяли домен university/administrative processes; Song et al. показывают метод на logistics — перенос идеи аналогичен, реализация pMeta-BPMN у нас пока не внедрена.»

## Если попросят «покажите похожий анализ»

Честный ответ:

1. Показать **BPMN** с data objects (`XML код/табельныйучёт2.bpmn` — есть артефакты).
2. Объяснить: «здесь виден information flow на уровне BPMN; pMeta-BPMN добавил бы probability и dependency tables».
3. Сослаться на `04-probabilistic-bpmn-and-meta-graph.md` для структуры метода.

## CIMS 2025 — тот же авторский трек

Китайская версия (Luo et al., 2025) подтверждает: case application проверяет effectiveness для **uncertain service process** quantitative analysis. Logistics в BPMJ — англоязычная публикация той же линии исследований (Hangzhou Dianzi University).
