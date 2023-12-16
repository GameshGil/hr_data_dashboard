"""Flask app commands."""
import os

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import db


def add_csv_to_db(path_to_csv):
    """Pandas CSV file loading and adding to db."""
    df = pd.read_csv(path_to_csv)
    df.to_sql('human_data', con=db.engine, if_exists='append', index=False)


def load_csv_from_folder():
    """CSV file loading from folder."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    path_to_csv = os.path.join(basedir, 'human_data/result.csv')

    if (os.path.exists(path_to_csv) and
            os.path.isfile(path_to_csv) and
            os.access(path_to_csv, os.R_OK)):
        add_csv_to_db(path_to_csv)
    else:
        print('Путь не существует, объект не является файлом'
              'или к нему нет доступа.')


def normalize_table(table):
    """Sorting records and wrapping cell text in table."""
    main_row = [
        'ID',
        'ФИО работника',
        'Падение эффективности\nза последний месяц',
        'Падение эффективности\nза последние полгода',
        'Вероятность увольнения\nв ближайшее время'
    ]
    table.sort(key=lambda x: int(x[-1][:-1]), reverse=True)
    result_table = [main_row] + table
    for row in result_table[1:]:
        for i in range(len(row)):
            if len(row[i]) > 27:
                row[i] = '\n'.join(row[i].split())
    return result_table


def generate_report(departments):
    """Generating a report on employee burnout divided by department."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    pdf_filename = os.path.join(basedir, 'reports/report_table.pdf')
    pdf = SimpleDocTemplate(
        pdf_filename, pagesize=A4, title='Отчет', topMargin=20)
    elements = []

    font_path = 'backend/my_dash/static/fonts/NotoSerif-Regular.ttf'
    pdfmetrics.registerFont(TTFont('CyrillicFont', font_path))
    styles = getSampleStyleSheet()
    styles['Heading1'].fontName = 'CyrillicFont'
    styles['Heading1'].fontSize = 24
    styles['Heading2'].fontName = 'CyrillicFont'
    styles['Heading2'].fontSize = 18
    styles['Normal'].fontName = 'CyrillicFont'

    report_heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        alignment=1,
        spaceAfter=50
    )

    table_heading_style = ParagraphStyle(
        'Heading2', parent=styles['Heading2'], alignment=1)

    column_widths = [
        0.5 * inch, 2.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch]
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'CyrillicFont'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.beige, colors.aquamarine]),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]

    link_style = ParagraphStyle(
        'Link',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.blue,
        spaceBefore=7,
        spaceAfter=50)

    def generate_report_table(department_title, department_data):
        """Generating a table with data for a separate department."""
        table_header = Paragraph(department_title, table_heading_style)
        elements.append(table_header)

        report_table = Table(
            normalize_table(department_data),
            colWidths=column_widths,
            style=table_style
        )
        elements.append(report_table)

        link_url = "https://google.com"
        link = Paragraph(
            f'<a href="{link_url}">Дашборды по данным</a>',
            link_style
        )
        elements.append(link)

    report_header_text = "Актуальный отчет по вопросу выгорания сотрудников"
    report_header = Paragraph(report_header_text, report_heading_style)
    elements.append(report_header)

    for department in departments:
        generate_report_table(
            department['department_title'],
            department['department_data']
        )

    pdf.build(elements)

    print(f"PDF report generated: {pdf_filename}")


# Testing data
# generate_report(
#     [
#         {
#             'department_title': 'Наименование отдела компании 1',
#             'department_data': [
#                 ['1', 'Иванов Иван Иванович', '11%', '63%', '54%'],
#                 ['2',
#                  'Александров Александр Александрович',
#                  '23%',
#                  '47%',
#                  '73%'
#                  ],
#                 ['3', 'Николаев Николай Николаевич', '5%', '27%', '14%'],
#             ]
#         },
#         {
#             'department_title': 'Наименование отдела компании 2',
#             'department_data': [
#                 ['1', 'Иванов Иван Иванович', '11%', '63%', '54%'],
#                 ['2', 'Александров Александр Александрович',
#                  '23%',
#                  '47%',
#                  '73%'
#                  ],
#                 ['3', 'Николаев Николай Николаевич', '5%', '27%', '14%'],
#             ]
#         }
#     ]
# )
