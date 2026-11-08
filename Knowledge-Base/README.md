# База знаний по моделированию и оптимизации бизнес-процессов

Структурированные конспекты для диплома, отчёта, презентаций и улучшения промптов ИИ.

**Это не копии официальных стандартов и не подделка научных статей.** Это учебные заметки, составленные по открытым материалам OMG, Camunda и двум статьям BPMJ.

---

## Главная идея базы знаний

Тема работы: **применение ИИ для решения задачи оптимизации бизнес-процессов**.

Чтобы ИИ мог помогать с BPMN, сначала нужен фундамент:

1. **Что такое BPMN и зачем он нужен** (официальный стандарт OMG, сайт bpmn.org).
2. **Как BPMN применяется на практике** (Camunda: паттерны, стиль, оптимизация).
3. **Как ИИ может дополнять или генерировать модели** (две статьи BPMJ, меньшая часть базы).

Примерное соотношение материалов:

| Доля | Источник | Папка |
|------|----------|-------|
| ~45% | OMG BPMN 2.0 / bpmn.org | [`BPMN-OMG-Official/`](BPMN-OMG-Official/) |
| ~35% | Camunda (практика BPMN) | [`Camunda-BPMN-Practice/`](Camunda-BPMN-Practice/) |
| ~20% | Научные статьи BPMJ | [`Ayad-Alsayoud-2024/`](Ayad-Alsayoud-2024/), [`Song-et-al-2026/`](Song-et-al-2026/) |

---

## С чего начать

1. [`00-map-for-thesis-and-ai.md`](00-map-for-thesis-and-ai.md) — карта всей базы и связь с проектом.
2. [`BPMN-OMG-Official/README.md`](BPMN-OMG-Official/README.md) — официальная нотация.
3. [`Camunda-BPMN-Practice/README.md`](Camunda-BPMN-Practice/README.md) — практика и паттерны.
4. Статьи — только после пунктов 2 и 3.

---

## Структура папок

### Основа (большинство материала)

| Папка | Источник | Содержание |
|-------|----------|------------|
| [`BPMN-OMG-Official/`](BPMN-OMG-Official/) | [bpmn.org](https://www.bpmn.org/) → OMG BPMN 2.0.2 | Цели, элементы, типы диаграмм, XML, conformance |
| [`Camunda-BPMN-Practice/`](Camunda-BPMN-Practice/) | [camunda.com/bpmn](https://camunda.com/bpmn/) + примеры в `BPMN/` | Практика, паттерны, стиль, оптимизация, ИИ |

### Дополнение (меньшинство)

| Папка | Источник |
|-------|----------|
| [`Ayad-Alsayoud-2024/`](Ayad-Alsayoud-2024/) | Prompt engineering для semantic quality BPM |
| [`Song-et-al-2026/`](Song-et-al-2026/) | pMeta-BPMN, неопределённость, вероятности |

---

## Связь с файлами проекта

| База знаний | Файлы в репозитории |
|-------------|---------------------|
| OMG: элементы BPMN | `Output/*.bpmn`, `XML код/*.bpmn` |
| Camunda: паттерны | `BPMN/01-bpmn-examples/`, `BPMN/xml/image*.bpmn` |
| Camunda: стиль | `BPMN/02-bpmn-modeling-styles/` |
| ИИ + BPMN | `System Prompt/SystemPrompt.md` |
| XPDL / Bizagi | `tools/bpmn_to_xpdl.py`, `XPDL/` |
| Статья Ayad | `Literature/Ayad2024-BusinessModelPrompt/` |

---

## Для преподавателя (кратко)

> База знаний построена прежде всего на официальном стандарте BPMN 2.0 (OMG, bpmn.org) и практическом руководстве Camunda. Научные статьи Ayad (2024) и Song (2026) используются как дополнение для обоснования применения ИИ, а не как основной источник по BPMN.

---

## Официальные ссылки

- BPMN на OMG: https://www.omg.org/spec/BPMN/
- Текущая версия: BPMN 2.0.2 (январь 2014)
- ISO: BPMN также опубликован как ISO/IEC 19510:2013
- Camunda BPMN: https://camunda.com/bpmn/
- Примеры Camunda в проекте: `BPMN/00-overview.md`
