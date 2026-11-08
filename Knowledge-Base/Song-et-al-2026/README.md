# База знаний: Song et al. (2026) — pMeta-BPMN

> **Дополнительный источник (~10% базы знаний).** Основа — OMG BPMN и Camunda. Эта папка — про uncertainty и pMeta-BPMN (теория), не про базовое моделирование BPMN.

Это **не статья** и **не её копия**. Это структурированные **конспектные заметки** по опубликованной работе — для диплома, презентации преподавателю и улучшения понимания неопределённости в BPM.

## Источник

**Song, R., Luo, X., Li, M., & Liu, C. (2026).** Modelling and analysing the uncertainty in business processes: pMeta-BPMN based on probability theory. *Business Process Management Journal*, 32(4), 1510–1542.  
DOI: https://doi.org/10.1108/BPMJ-09-2025-1429

**Связанная более ранняя публикация (китайский журнал, открытый abstract):**  
Luo, X., Song, R., Li, M., & Liu, C. (2025). Service process analysis method integrating probabilistic BPMN and Meta graph with information probability. *Computer Integrated Manufacturing Systems*, 31(9), 3437–3454.

## Файлы в этой папке

| Файл | Содержание |
|------|------------|
| `01-citation-and-disclaimer.md` | Цитирование, что это конспект |
| `02-what-the-article-is-about.md` | Проблема, цель, VUCA, неопределённость |
| `03-methodology-pmeta-bpmn.md` | Метод pMeta-BPMN: workflow + information flow |
| `04-probabilistic-bpmn-and-meta-graph.md` | Два слоя: pBPMN и information probability Meta graph |
| `05-findings-and-originality.md` | Результаты, новизна, ограничения |
| `06-logistics-case.md` | Пилотный кейс (логистика) |
| `07-how-we-use-this-for-ai.md` | Связь с нашим BPMN/XPDL проектом |
| `08-key-terms-glossary.md` | Словарь терминов для ИИ |

## Для преподавателя (одно предложение)

> Мы изучили Song et al. (2026): метод pMeta-BPMN объединяет BPMN (качественное моделирование workflow) и Meta graph с теорией вероятностей (количественный анализ неопределённости workflow и information flow). Конспект — в этой папке, без подделки оригинала.

## Как использовать с ИИ

1. Прочитайте `02`–`05` — понять, чем pMeta-BPMN отличается от обычного BPMN.
2. Используйте `08-key-terms-glossary.md` как контекст при обсуждении uncertainty с LLM.
3. Сверяйте с нашими моделями: обычный BPMN в `Output/` описывает **логику**, но **не квантифицирует** вероятности (это нормально для нашего текущего scope).
