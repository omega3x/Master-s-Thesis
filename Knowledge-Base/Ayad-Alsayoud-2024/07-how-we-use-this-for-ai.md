# Как мы используем эту базу для улучшения ИИ

## Цель

Не «подделать статью», а **встроить проверенные идеи** в наш pipeline генерации и доработки BPM.

---

## Два режима работы с LLM (по Ayad et al. + наш проект)

### Режим A — Semantic enhancement (как в статье)

**Когда:** есть черновик модели (`Output/testx.bpmn` или XPDL).

**Что делает ИИ:** предлагает недостающие activities и artifacts.

**Промпты:** `08-prompt-templates.md` (zero-shot / few-shot / CoT).

**Человек:** выбирает предложения → обновляет BPMN → перегенерирует XPDL.

### Режим B — Generation (наше расширение)

**Когда:** нужна новая модель с нуля.

**Что делает ИИ:** генерирует полный BPMN XML по `System Prompt/SystemPrompt.md`.

**Человек:** проверяет в Camunda/bpmn.io → конвертирует в XPDL → Bizagi.

---

## Карта: статья → файлы репозитория

| Идея из статьи | Наша реализация |
|----------------|-----------------|
| Domain knowledge через LLM | `System Prompt/SystemPrompt.md` |
| XPDL для Bizagi | `tools/bpmn_to_xpdl.py` → `XPDL/` |
| Извлечение lanes/activities | Можно использовать `Parsing_xml.py` авторов |
| Zero-shot / few-shot / CoT | `08-prompt-templates.md` |
| Hospitalization benchmark | `Literature/.../Medical2.xpdl` |
| Простой тестовый процесс | `Output/testx.bpmn` |
| Полуавтомат | ИИ предлагает/генерирует → человек проверяет |

---

## Рекомендуемый workflow перед показом преподавателю

```
1. Показать testx.bpmn (простая модель)
2. Запустить zero-shot промпт из 08-prompt-templates.md
3. Показать список предложений LLM (semantic enhancement)
4. Показать testx.xpdl в Bizagi (XPDL pipeline)
5. Показать эту папку Knowledge-Base — «мы изучили Ayad 2024, вот конспект»
```

---

## Что добавить в System Prompt (опционально)

На основе статьи, в промпт генерации BPMN можно включить:

1. «Перед финальным XML проверь semantic completeness: все ли роли покрыты?»
2. «Для каждой userTask укажи связанный dataObject где уместно»
3. «Не упрощай процесс до линейной цепочки, если домен требует approvals/exceptions»

Это переносит **semantic quality** из статьи в наш генератор.

---

## Что сказать, если спросят «вы прочитали статью?»

> «Мы изучили публикацию Ayad & Alsayoud (2024): метод semantic enhancement через prompt engineering и XPDL. Полный PDF — через библиотеку; ключевые идеи и материалы авторов с GitHub собраны в `Knowledge-Base/Ayad-Alsayoud-2024/`. Мы применили их техники промптинга и реализовали XPDL-экспорт для Bizagi. Наш подход расширяет статью: мы также генерируем BPMN, а не только дополняем существующую модель.»
