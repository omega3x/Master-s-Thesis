"""Fill the VVSU practice report template without changing the original file."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "_2026  МПИ Отчет по практике_ шаблон.docx"
REPORT_TEXT = ROOT / "Отчёт.md"
OUTPUT_PROJECT = ROOT / "Отчёт по практике Расулев Сергей Шамильевич (с приложением).docx"
OUTPUT_DESKTOP = Path(
    r"C:\Users\Godzilla\Desktop\Отчёт по практике Расулев Сергей Шамильевич (с приложением).docx"
)
CREATE_BILL_IMAGE = ROOT / "assets" / "create_bill_business_rules.png"
DIPLOMA_IMAGE = ROOT / "assets" / "graduate_diploma_issuance.png"


def remove_paragraph(paragraph) -> None:
    element = paragraph._element
    element.getparent().remove(element)
    paragraph._p = paragraph._element = None


def clear_paragraph(paragraph) -> None:
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)


def set_text(
    paragraph,
    text: str,
    *,
    font_name: str = "Times New Roman",
    size: float = 12,
    align=None,
    bold: bool = False,
    italic: bool = False,
    first_indent: float | None = None,
    line_spacing: float = 1.0,
) -> None:
    clear_paragraph(paragraph)
    run = paragraph.add_run(text)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    paragraph.alignment = align
    paragraph.paragraph_format.line_spacing = line_spacing
    paragraph.paragraph_format.first_line_indent = (
        Cm(first_indent) if first_indent is not None else None
    )


def set_outline_level(paragraph, level: int) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    outline = p_pr.find(qn("w:outlineLvl"))
    if outline is None:
        outline = OxmlElement("w:outlineLvl")
        p_pr.append(outline)
    outline.set(qn("w:val"), str(level))


def remove_outline_level(paragraph) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    outline = p_pr.find(qn("w:outlineLvl"))
    if outline is not None:
        p_pr.remove(outline)


def add_heading_before(
    anchor,
    text: str,
    *,
    level: int,
    centered: bool = False,
    page_break: bool = False,
):
    paragraph = anchor.insert_paragraph_before()
    set_text(
        paragraph,
        text,
        font_name="Arial",
        size=14,
        align=WD_ALIGN_PARAGRAPH.CENTER if centered else WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.0,
    )
    paragraph.paragraph_format.space_before = Pt(24 if level == 0 else 12)
    paragraph.paragraph_format.space_after = Pt(12 if level == 0 else 6)
    paragraph.paragraph_format.page_break_before = page_break
    set_outline_level(paragraph, level)
    return paragraph


def add_body_before(anchor, text: str, *, list_item: bool = False):
    paragraph = anchor.insert_paragraph_before()
    set_text(
        paragraph,
        text,
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        first_indent=None if list_item else 1.25,
        line_spacing=1.5,
    )
    paragraph.paragraph_format.space_after = Pt(0)
    if list_item:
        paragraph.paragraph_format.left_indent = Cm(1.25)
        paragraph.paragraph_format.first_line_indent = Cm(-0.63)
    return paragraph


def add_image_before(anchor, image_path: Path, caption_text: str):
    if not image_path.exists():
        return
    paragraph = anchor.insert_paragraph_before()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(3)
    paragraph.add_run().add_picture(str(image_path), width=Cm(15.5))

    caption = anchor.insert_paragraph_before()
    set_text(
        caption,
        caption_text,
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.0,
    )
    caption.paragraph_format.space_after = Pt(6)


def add_toc_field_before(anchor):
    paragraph = anchor.insert_paragraph_before()
    paragraph.paragraph_format.line_spacing = 1.5
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = ' TOC \\o "1-3" \\h \\z \\u '
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Содержание будет обновлено при открытии документа."
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, placeholder, end])
    return paragraph


def update_fields_on_open(document: Document) -> None:
    settings = document.settings._element
    update = settings.find(qn("w:updateFields"))
    if update is None:
        update = OxmlElement("w:updateFields")
        settings.append(update)
    update.set(qn("w:val"), "true")


def fill_cover_and_assignment(document: Document) -> None:
    p = document.paragraphs

    set_text(
        p[24],
        "гр. МПИ-25-ИИ1                         _______________________ С.Ш. Расулев",
        font_name="Times New Roman",
        size=14,
        line_spacing=1.0,
    )
    set_text(p[26], "Руководитель практики", size=14, line_spacing=1.0)
    set_text(p[27], "от кафедры", size=14, line_spacing=1.0)
    set_text(
        p[28],
        "кандидат физико-математических наук, доцент",
        size=14,
        line_spacing=1.0,
    )
    set_text(
        p[29],
        "                                                _______________________ А.Б. Кригер",
        size=14,
        line_spacing=1.0,
    )

    set_text(
        p[45],
        "на производственную научно-исследовательскую практику (2 семестр)",
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.0,
    )
    set_text(
        p[49],
        "Студенту гр. МПИ-25-ИИ1 Расулеву Сергею Шамильевичу",
        size=12,
        line_spacing=1.0,
    )
    tasks = [
        "1. Изучить нотацию BPMN 2.0 и сформировать структуру базы знаний.",
        "2. Разработать системный промпт для генерации BPMN XML.",
        "3. Подготовить и описать модели бизнес-процессов.",
        "4. Реализовать генерацию BPMN и преобразование BPMN в XPDL.",
        "5. Провести проверку моделей, выявить ошибки и оценить результат.",
    ]
    for idx, task in enumerate(tasks, start=50):
        set_text(p[idx], task, size=12, line_spacing=1.0)
    set_text(
        p[55],
        "Срок сдачи отчёта на кафедру: 17.07.2026",
        size=12,
        line_spacing=1.0,
    )
    set_text(
        p[72],
        "Руководитель практики от кафедры,",
        size=12,
        line_spacing=1.0,
    )
    set_text(
        p[73],
        "кандидат физико-математических наук, доцент       ____________________ А.Б. Кригер",
        size=12,
        line_spacing=1.0,
    )
    set_text(
        p[77],
        "Задание получил                                  ____________________ С.Ш. Расулев",
        size=12,
        line_spacing=1.0,
    )


def classify_heading(line: str):
    if line in {"ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ"}:
        return 0, True
    if re.match(r"^\d+\.\s+[А-ЯЁA-Z0-9 ,]+$", line):
        return 0, False
    numbered_heading = re.match(r"^(\d+(?:\.\d+)+)\.\s+", line)
    if numbered_heading:
        depth = numbered_heading.group(1).count(".")
        return min(depth, 2), False
    return None


def fill_report_body(document: Document) -> None:
    start = next(i for i, p in enumerate(document.paragraphs) if p.text == "Содержание")
    end = next(i for i, p in enumerate(document.paragraphs) if p.text == "Приложение А")
    to_remove = list(document.paragraphs[start:end])
    anchor = document.paragraphs[end]
    for paragraph in to_remove:
        remove_paragraph(paragraph)

    content_heading = add_heading_before(
        anchor, "Содержание", level=0, centered=True, page_break=True
    )
    remove_outline_level(content_heading)
    content_heading.paragraph_format.space_before = Pt(24)
    add_toc_field_before(anchor)

    lines = REPORT_TEXT.read_text(encoding="utf-8").splitlines()
    report_start = lines.index("ВВЕДЕНИЕ")
    lines = lines[report_start:]

    for line in lines:
        text = line.strip()
        if not text:
            continue

        heading = classify_heading(text)
        if heading is not None:
            level, centered = heading
            if text == "4.1.5. Анализ качества":
                add_image_before(
                    anchor,
                    CREATE_BILL_IMAGE,
                    "Рисунок 1. Процесс создания счёта с использованием бизнес-правила",
                )
            if text == "4.2.5. Проверка в StormBPMN":
                add_image_before(
                    anchor,
                    DIPLOMA_IMAGE,
                    "Рисунок 2. BPMN-модель процесса формирования и выдачи диплома",
                )
            add_heading_before(
                anchor,
                format_heading_text(text),
                level=level,
                centered=centered,
                page_break=level == 0,
            )
            continue

        is_list_item = bool(re.match(r"^\d+\.\s+", text)) or text.startswith("http")
        add_body_before(anchor, text, list_item=is_list_item)

    update_fields_on_open(document)


def format_heading_text(text: str) -> str:
    fixed_titles = {
        "ВВЕДЕНИЕ": "Введение",
        "ЗАКЛЮЧЕНИЕ": "Заключение",
        "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ": "Список использованных источников",
    }
    if text in fixed_titles:
        return fixed_titles[text]
    match = re.match(r"^(\d+\.\s+)(.+)$", text)
    if match and match.group(2).isupper():
        title = match.group(2).lower()
        return match.group(1) + title[0].upper() + title[1:]
    return text


def format_appendices(document: Document) -> None:
    for paragraph in document.paragraphs:
        if paragraph.text in {"Приложение А", "Приложение Б", "Приложение В"}:
            set_outline_level(paragraph, 0)


def set_cell_text(cell, text: str, *, bold: bool = False) -> None:
    cell.text = ""
    paragraph = cell.paragraphs[0]
    set_text(
        paragraph,
        text,
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        bold=bold,
        line_spacing=1.0,
    )
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def fill_appendix_a(document: Document) -> None:
    appendix_a_index = next(
        i for i, paragraph in enumerate(document.paragraphs)
        if paragraph.text == "Приложение А"
    )
    appendix_b = next(
        paragraph for paragraph in document.paragraphs
        if paragraph.text == "Приложение Б"
    )
    appendix_title = document.paragraphs[appendix_a_index + 2]
    set_text(
        appendix_title,
        "Характеристики больших языковых моделей, использованных в работе",
        font_name="Arial",
        size=14,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.0,
    )
    appendix_title.paragraph_format.space_before = Pt(12)
    appendix_title.paragraph_format.space_after = Pt(12)

    intro = appendix_b.insert_paragraph_before()
    set_text(
        intro,
        "В ходе практики применялись две большие языковые модели: GPT-5.6 Sol "
        "и Composer 2.5. Их основные характеристики и фактическая роль в проекте "
        "представлены в таблице А.1.",
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        first_indent=1.25,
        line_spacing=1.5,
    )

    caption = appendix_b.insert_paragraph_before()
    set_text(
        caption,
        "Таблица А.1. Сравнительные характеристики использованных LLM",
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.0,
    )
    caption.paragraph_format.space_before = Pt(6)
    caption.paragraph_format.space_after = Pt(3)

    rows = [
        (
            "Разработчик и способ доступа",
            "OpenAI; использовалась в рабочей среде Cursor.",
            "Cursor; использовалась как встроенная агентная модель Cursor.",
        ),
        (
            "Тип модели",
            "Универсальная большая языковая модель с возможностями рассуждения "
            "и работы с программным кодом.",
            "Агентная большая языковая модель, ориентированная на программную "
            "разработку и длительные задачи.",
        ),
        (
            "Основное назначение",
            "Анализ текста и кода, подготовка объяснений, сопоставление данных "
            "и выполнение многоэтапных заданий.",
            "Работа с проектом: поиск файлов, редактирование, выполнение команд "
            "и согласованное изменение нескольких материалов.",
        ),
        (
            "Входные данные и контекст",
            "Текстовые запросы, программный код, XML и выбранные материалы проекта, "
            "переданные через Cursor.",
            "Текстовые запросы, программный код, файлы рабочего пространства "
            "и результаты работы инструментов Cursor.",
        ),
        (
            "Использование в проекте",
            "Анализ структуры проекта, проверка BPMN XML, уточнение фактов, "
            "подготовка и редактирование русскоязычного отчёта.",
            "Первичная структуризация материалов, работа с файлами, подготовка "
            "черновых решений и выполнение программных задач.",
        ),
        (
            "Сильные стороны",
            "Следование подробным инструкциям, анализ связанных материалов, "
            "работа с русским языком, кодом и формализованными требованиями.",
            "Высокая скорость работы с репозиторием, удобное выполнение цепочки "
            "действий и ориентация на практические задачи разработки.",
        ),
        (
            "Ограничения",
            "Может формировать правдоподобные, но неточные ответы; результат "
            "зависит от запроса и контекста и требует проверки.",
            "Результаты редактирования и выводы также требуют проверки; модель "
            "не заменяет специализированный валидатор BPMN.",
        ),
        (
            "Условия доступа и оплаты",
            "Коммерческое использование. Стоимость зависит от тарифа Cursor "
            "или объёма токенов при доступе через API.",
            "Доступна в Cursor. Стоимость зависит от выбранного плана, объёма "
            "использования и режима модели.",
        ),
        (
            "Публичность технических данных",
            "Число параметров, состав обучающей выборки и часть архитектурных "
            "характеристик публично не раскрываются.",
            "Число параметров, состав обучающей выборки и подробная архитектура "
            "публично не раскрываются.",
        ),
    ]

    table = document.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{edge}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "4")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "000000")
        borders.append(border)
    table._tbl.tblPr.append(borders)
    table.columns[0].width = Cm(4.0)
    table.columns[1].width = Cm(6.0)
    table.columns[2].width = Cm(6.0)
    headers = ("Характеристика", "GPT-5.6 Sol", "Composer 2.5")
    for cell, text in zip(table.rows[0].cells, headers):
        set_cell_text(cell, text, bold=True)
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))

    for characteristic, gpt, composer in rows:
        cells = table.add_row().cells
        for cell, text in zip(cells, (characteristic, gpt, composer)):
            set_cell_text(cell, text)
    appendix_b._p.addprevious(table._tbl)

    note = appendix_b.insert_paragraph_before()
    set_text(
        note,
        "Обе модели имеют вероятностный характер генерации. Поэтому полученные "
        "ответы проверялись по исходным файлам, официальной документации и с "
        "помощью специализированных средств, включая StormBPMN. Технические "
        "характеристики, которые не раскрыты разработчиками, в таблицу не "
        "включались. Сведения об условиях доступа и стоимости зафиксированы "
        "по состоянию на 17.07.2026 [16-20].",
        font_name="Times New Roman",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        first_indent=1.25,
        line_spacing=1.5,
    )
    note.paragraph_format.space_before = Pt(6)


def main() -> None:
    document = Document(TEMPLATE)
    fill_cover_and_assignment(document)
    fill_report_body(document)
    fill_appendix_a(document)
    format_appendices(document)
    document.save(OUTPUT_PROJECT)
    document.save(OUTPUT_DESKTOP)
    print("Filled practice report created.")


if __name__ == "__main__":
    main()
