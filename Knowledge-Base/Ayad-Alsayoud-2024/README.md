# База знаний: Ayad & Alsayoud (2024)

> **Дополнительный источник (~10% базы знаний).** Основа — OMG BPMN (`../BPMN-OMG-Official/`) и Camunda (`../Camunda-BPMN-Practice/`). Эта папка — про prompt engineering и semantic enhancement, не про определение элементов BPMN.

Это **не статья** и **не её копия**. Это структурированные **конспектные заметки** по опубликованной работе — для диплома, презентации преподавателю и улучшения промптов ИИ в нашем проекте.

## Источник

**Ayad, S., & Alsayoud, F. (2024).** Prompt engineering techniques for semantic enhancement in business process models. *Business Process Management Journal*, 30(7), 2611–2641.  
DOI: https://doi.org/10.1108/BPMJ-02-2024-0108

**Официальные доп. материалы авторов:** https://github.com/fgs-fgs/BusinessModelPrompt  
(склонировано в `Literature/Ayad2024-BusinessModelPrompt/`)

## Файлы в этой папке

| Файл | Содержание |
|------|------------|
| `01-citation-and-disclaimer.md` | Что это за папка, что мы НЕ делаем |
| `02-what-the-article-is-about.md` | Цель, проблема, основная идея |
| `03-methodology.md` | Как авторы работают: XPDL → промпты → предложения |
| `04-prompt-engineering-techniques.md` | Zero-shot, few-shot, chain-of-thought |
| `05-findings-limitations.md` | Результаты, ограничения, практика |
| `06-hospitalization-example.md` | Пример Hospitalization из GitHub авторов |
| `07-how-we-use-this-for-ai.md` | Как применяем в нашем репозитории |
| `08-prompt-templates.md` | Готовые шаблоны промптов для LLM |

## Для преподавателя (одно предложение)

> Мы изучили статью Ayad & Alsayoud (2024), выделили ключевые идеи в эту базу знаний и используем их для улучшения prompt engineering при работе с BPMN и XPDL — без подделки оригинальной публикации.

## Как использовать с ИИ

1. Прочитайте файлы `02`–`05` — контекст статьи.
2. Используйте `08-prompt-templates.md` в Cursor / ChatGPT при доработке моделей.
3. Сверяйте выводы ИИ с `System Prompt/SystemPrompt.md` и `Output/testx.bpmn`.
