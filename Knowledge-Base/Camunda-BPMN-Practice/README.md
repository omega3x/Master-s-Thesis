# База знаний: Camunda BPMN (практика)

Конспекты по **практическому применению BPMN** на основе материалов Camunda и локального архива примеров в `BPMN/`.

## Источники

- Официальная страница: https://camunda.com/bpmn/
- Примеры: https://camunda.com/bpmn/examples/ (архив в `BPMN/`)
- Camunda — **участник разработки BPMN 2.0** в OMG (с 2009)
- BPMN как **ISO/IEC 19510:2013** (указано на camunda.com/bpmn)

## Важно

Camunda — **вендор** BPM-платформы, но их материалы по BPMN описывают **открытый стандарт**, а не проприетарную нотацию. Это второй опорный источник после OMG, с акцентом на **практику и паттерны**.

## Файлы

| Файл | Содержание |
|------|------------|
| `01-citation-and-disclaimer.md` | Цитирование |
| `02-why-bpmn-matters.md` | Зачем BPMN бизнесу и IT |
| `03-core-elements-practical.md` | Элементы на практике |
| `04-patterns-catalog.md` | Каталог паттернов из примеров |
| `05-modeling-styles.md` | Стиль и читаемость |
| `06-optimization-patterns.md` | Оптимизация процессов |
| `07-bpmn-and-ai.md` | BPMN и LLM |
| `08-how-we-use-in-project.md` | Связь с репозиторием |

## Связь с OMG

| OMG (теория) | Camunda (практика) |
|--------------|-------------------|
| Определение элементов | Когда какой паттерн применять |
| Conformance | Import в Modeler |
| Scope | Enterprise use cases |
| Token semantics | Engine behavior (Zeebe/Camunda 8) |

Читать **после** `BPMN-OMG-Official/04`–`07`, **до** статей Ayad/Song.
