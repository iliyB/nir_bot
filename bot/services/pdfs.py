import io

from our_types import ObservedStrObject
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def generate_pdf_from_card(card: ObservedStrObject) -> bytes:
    font_config = FontConfiguration()

    html_template = card.get_all_card.replace("\n", "<br>")

    html = HTML(string=html_template)

    pdf = html.write_pdf(font_config=font_config, presentational_hints=True)
    pdf_in_memory = io.BytesIO(pdf)
    pdf_in_memory.seek(0)

    return pdf_in_memory.read()
