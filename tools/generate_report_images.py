"""Create the two BPMN illustrations used in Отчёт.docx."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(name, size)


def center_text(draw: ImageDraw.ImageDraw, box, text: str, text_font) -> None:
    left, top, right, bottom = box
    bbox = draw.multiline_textbbox((0, 0), text, font=text_font, align="center")
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(
        (left + (right - left - width) / 2, top + (bottom - top - height) / 2),
        text,
        fill="#1f2933",
        font=text_font,
        align="center",
        spacing=4,
    )


def rounded_box(draw: ImageDraw.ImageDraw, box, text: str, fill="#e9f1fb") -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill, outline="#46769b", width=3)
    center_text(draw, box, text, font(29))


def arrow(draw: ImageDraw.ImageDraw, start, end) -> None:
    draw.line([start, end], fill="#374151", width=5)
    x, y = end
    draw.polygon([(x, y), (x - 20, y - 11), (x - 20, y + 11)], fill="#374151")


def create_bill_diagram() -> None:
    image = Image.new("RGB", (2300, 950), "white")
    draw = ImageDraw.Draw(image)

    draw.text(
        (70, 45),
        "BPMN-модель: создание счёта с использованием бизнес-правила",
        fill="#111827",
        font=font(42, bold=True),
    )
    draw.text(
        (70, 115),
        "Входные критерии правила: сумма заказа и тип клиента",
        fill="#4b5563",
        font=font(28),
    )

    pool = (55, 195, 2245, 800)
    draw.rounded_rectangle(pool, radius=10, outline="#4b5563", width=3)
    draw.text((78, 415), "Создание\nсчёта", fill="#374151", font=font(27, bold=True))
    draw.line([(230, 195), (230, 800)], fill="#4b5563", width=3)

    event_start = (300, 445, 370, 515)
    event_end = (1910, 445, 1980, 515)
    draw.ellipse(event_start, fill="#f1fff4", outline="#31833c", width=4)
    draw.ellipse(event_end, fill="#fff7f7", outline="#b91c1c", width=7)
    center_text(draw, event_start, "", font(10))

    rounded_box(draw, (465, 390, 760, 570), "Рассчитать\nскидку")
    rounded_box(draw, (970, 390, 1265, 570), "Применить\nбизнес-правило", fill="#fff4da")
    rounded_box(draw, (1475, 390, 1770, 570), "Создать\nсчёт")

    arrow(draw, (370, 480), (465, 480))
    arrow(draw, (760, 480), (970, 480))
    arrow(draw, (1265, 480), (1475, 480))
    arrow(draw, (1770, 480), (1910, 480))

    draw.text((276, 535), "Запрос счёта", fill="#374151", font=font(23))
    draw.text((1865, 535), "Счёт создан", fill="#374151", font=font(23))

    rule_box = (935, 655, 1300, 755)
    draw.rounded_rectangle(rule_box, radius=14, fill="#f7e7bc", outline="#9a6c09", width=3)
    center_text(draw, rule_box, "Механизм правил:\nсумма заказа + тип клиента", font(23))
    draw.line([(1117, 570), (1117, 655)], fill="#9a6c09", width=3)
    draw.polygon([(1117, 655), (1107, 635), (1127, 635)], fill="#9a6c09")

    draw.text(
        (290, 845),
        "Примечание: проценты и диапазоны скидки относятся к учебному примеру; "
        "в реальном процессе правило оформляется отдельной таблицей решений.",
        fill="#4b5563",
        font=font(24),
    )

    image.save(ASSETS / "create_bill_business_rules.png")


def diamond(draw: ImageDraw.ImageDraw, center, text: str) -> None:
    x, y = center
    points = [(x, y - 45), (x + 45, y), (x, y + 45), (x - 45, y)]
    draw.polygon(points, fill="#fff4da", outline="#9a6c09", width=3)
    center_text(draw, (x - 42, y - 32, x + 42, y + 32), text, font(18))


def diploma_diagram() -> None:
    image = Image.new("RGB", (2400, 1400), "white")
    draw = ImageDraw.Draw(image)

    draw.text(
        (70, 35),
        "BPMN-модель: формирование и выдача диплома",
        fill="#111827",
        font=font(42, bold=True),
    )

    lanes = [
        (70, 140, 2320, 440, "Студенческий офис"),
        (70, 440, 2320, 870, "Учебное подразделение"),
        (70, 870, 2320, 1290, "Регистратура и архив"),
    ]
    for left, top, right, bottom, name in lanes:
        draw.rectangle((left, top, right, bottom), outline="#6b7280", width=2)
        draw.line((245, top, 245, bottom), fill="#6b7280", width=2)
        center_text(draw, (80, top + 20, 225, bottom - 20), name, font(24, bold=True))

    start = (300, 250, 365, 315)
    draw.ellipse(start, fill="#f1fff4", outline="#31833c", width=4)
    draw.text((275, 330), "Заявление\nподано", fill="#374151", font=font(18))
    rounded_box(draw, (445, 215, 660, 350), "Принять\nзаявление")
    arrow(draw, (365, 282), (445, 282))

    diamond(draw, (760, 555), "+")
    rounded_box(draw, (850, 475, 1085, 600), "Проверить\nзадолженности\nв ERP")
    rounded_box(draw, (850, 660, 1085, 785), "Получить оценки\nиз LMS")
    diamond(draw, (1180, 630), "+")
    arrow(draw, (760, 555), (850, 537))
    arrow(draw, (760, 555), (850, 722))
    arrow(draw, (1085, 537), (1180, 630))
    arrow(draw, (1085, 722), (1180, 630))

    rounded_box(draw, (1270, 555, 1500, 690), "Проверить\nтребования\nк выпуску", fill="#fff4da")
    arrow(draw, (1225, 630), (1270, 630))
    diamond(draw, (1595, 630), "Требования\nвыполнены?")
    arrow(draw, (1500, 630), (1550, 630))
    rounded_box(draw, (1670, 500, 1900, 625), "Подписать\nвыписку")
    arrow(draw, (1640, 630), (1670, 562))
    rounded_box(draw, (1670, 700, 1900, 825), "Уведомить\nо недостатках", fill="#fce7e7")
    arrow(draw, (1640, 630), (1670, 762))
    end_reject = (1980, 730, 2045, 795)
    draw.ellipse(end_reject, fill="#fff7f7", outline="#b91c1c", width=6)
    arrow(draw, (1900, 762), (1980, 762))

    rounded_box(draw, (600, 980, 875, 1120), "Оформление диплома:\nPDF, ЭП, архив")
    rounded_box(draw, (1000, 980, 1205, 1120), "Отправить\nуведомления")
    rounded_box(draw, (1000, 1160, 1205, 1270), "Записать\nаудит")
    diamond(draw, (1340, 1125), "+")
    end_success = (1450, 1090, 1515, 1155)
    draw.ellipse(end_success, fill="#f1fff4", outline="#31833c", width=6)
    arrow(draw, (1785, 625), (740, 980))
    arrow(draw, (875, 1050), (1000, 1050))
    arrow(draw, (875, 1050), (1000, 1215))
    arrow(draw, (1205, 1050), (1340, 1125))
    arrow(draw, (1205, 1215), (1340, 1125))
    arrow(draw, (1385, 1125), (1450, 1125))

    draw.text(
        (1600, 1080),
        "Контроль срока:\nпри задержке подписи\nслучай передаётся декану.",
        fill="#4b5563",
        font=font(24),
        spacing=4,
    )
    draw.text(
        (70, 1330),
        "Схема составлена по структуре файла Output/test3.bpmn. "
        "Показаны основные элементы процесса; полный вариант содержит дополнительные связи и подписи.",
        fill="#4b5563",
        font=font(22),
    )
    image.save(ASSETS / "graduate_diploma_issuance.png")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    create_bill_diagram()
    diploma_diagram()
    print("Report images created.")
