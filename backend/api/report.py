import os
from io import BytesIO

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.tables import Table, TableStyle

load_dotenv()

SITE_URL = os.getenv('SITE_URL', 'https://foodgram.com')

registerFont(TTFont('Times', 'times.ttf', 'UTF-8'))
registerFont(TTFont('Times-Bold', 'timesbd.ttf', 'UTF-8'))
registerFont(TTFont('Times-Italic', 'timesi.ttf', 'UTF-8'))
registerFont(TTFont('Times-BoldItalic', 'timesbi.ttf', 'UTF-8'))
addMapping('Times', 0, 0, 'Times')
addMapping('Times', 0, 1, 'Times-Italic')
addMapping('Times', 1, 0, 'Times-Bold')
addMapping('Times', 1, 1, 'Times-BoldItalic')


class PDFPrint:
    """Класс формирует pdf документ."""
    def __init__(self, pagesize='A4'):
        """Инициализация отчета."""
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.styles = getSampleStyleSheet()
        self.styles.add(
            ParagraphStyle(
                name='Justify',
                alignment=TA_JUSTIFY,
                fontName='Times',
                fontSize=11
            )
        )
        self.styles.add(
            ParagraphStyle(
                name='Header-footer',
                alignment=TA_JUSTIFY,
                fontName='Times-Bold',
                fontSize=8
            )
        )
        self.styles.add(
            ParagraphStyle(
                name='Justify-Bold',
                alignment=TA_JUSTIFY,
                fontName='Times-Bold',
                fontSize=11
            )
        )
        self.styles.add(
            ParagraphStyle(
                name='MainHeading1',
                alignment=TA_CENTER,
                fontName='Times-Bold',
                fontSize=18
            )
        )
        self.normal_table_style = TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Times', 10),
            ('ALIGN', (0, 0), (0, -1), 'CENTRE'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        )
        self.green_table_style = TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Times', 10),
            ('ALIGN', (0, 0), (0, -1), 'CENTRE'),
            ('GRID', (0, 0), (9, -1), 1, colors.springgreen),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
            ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
        ]
        )

    def _header_footer(self, canvas, doc):
        """Формирует заголовок и подвал отчета."""
        canvas.saveState()
        header = Paragraph(
            _(
                'Foodgram is an online service '
                'on which users can publish recipes.'
            ),
            self.styles['Header-footer']
        )
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        footer = Paragraph(
            SITE_URL,
            self.styles['Header-footer']
        )
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def create_pdf(self, shoping_data):
        """Формирует pdf документ."""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shoping.pdf"'
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer,
                                rightMargin=15,
                                leftMargin=15,
                                topMargin=15,
                                bottomMargin=15,
                                pagesize=self.pagesize)
        elements = []
        elements.append(Spacer(1, 15))
        elements.append(
            Paragraph(
                _('Shopping list'), self.styles['MainHeading1']
            )
        )
        elements.append(Spacer(1, 15))
        table_header = (
            '№',
            _('name').capitalize(),
            _('unit').capitalize(),
            _('amount').capitalize()
        )
        table = [table_header]
        for number, ingredient in enumerate(shoping_data, start=1):
            row = (
                f'{number}',
                f'{ingredient["ingredients__name"]}',
                f'{ingredient["ingredients__measurement_unit"]}',
                f'{ingredient["total"]}'
            )
            table.append(row)
        table = Table(table, rowHeights=15, style=self.green_table_style)
        elements.append(table)
        elements.append(Spacer(1, 10))
        doc.build(
            elements,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer,
            canvasmaker=NumberedCanvas
        )
        response.write(buffer.getvalue())
        buffer.close()
        return response


class NumberedCanvas(canvas.Canvas):
    """Класс номерации строк в отчете."""
    def __init__(self, *args, **kwargs):
        """Инициализация канвы."""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):  # noqa: N802
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Добавляет на каждую нумерацию страницу."""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        """Прорисовка нумерации."""
        self.drawRightString(200 * mm, 5 * mm + (0.2 * inch),
                             f'{self._pageNumber}')
