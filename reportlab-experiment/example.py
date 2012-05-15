# -*- coding: utf-8 -*-
from functools import wraps

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table
from reportlab.graphics.barcode import eanbc, code39, code93
from PIL import Image


M = cm  # margin
W, H = A4[0] - 2 * M, A4[1] - 2 * M  # width & height


def trans(x=0, y=0):
    """
    Be wary this expects a global Canvas object named ``c`` to be existing.

    """
    def deco(func):
        @wraps(func)
        def wrapper(*a, **kwa):
            c.translate(x, y)
            result = func(*a, **kwa)
            return result
        return wrapper
    return deco


@trans(M, M)
def draw_margin_box(c, offset=5):
    for i, color in enumerate(
                (colors.black, colors.greenyellow, colors.red, colors.aqua)):
        c.setStrokeColor(color)
        c.rect(offset * i, offset * i, W - 2 * offset * i, H - 2 * offset * i)


@trans(M, M)
def draw_centered_img(c, img_file, ratio=1.0):
    img = Image.open(img_file)
    w, h = img.size
    if ratio != 1:
        w, h = w * ratio, h * ratio
    x, y = (W - w) // 2, (H - h) // 2
    c.drawImage(img_file, x, y, w, h)


@trans(M, M)
def draw_paragraph_text(c, text):
    style = getSampleStyleSheet()['Normal']
    style = ParagraphStyle(
                name='pingu_style',
                borderWidth=1,
                borderColor='#000000',
                backColor='#eeffee',
                borderPadding=12)
    p = Paragraph(text, style)
    aw, ah = W, H
    w, h = p.wrap(aw * 0.8, ah)
    p.drawOn(c, (W - w) // 2, ah - h - 60)


@trans(M, M)
def draw_centered_circle(c, colors):
    for i, color in enumerate(colors):
        c.setStrokeColor(color)
        c.setLineWidth(i * 2 + 1)
        c.circle(W // 2, H // 2, 100 + 16 * i, stroke=1, fill=0)


@trans(M, M)
def draw_table(c):
    cw, rh = 40, 32
    data = [
            ['00', '01', '02', '03', '04'],
            ['10', '11', '12', '13', '14'],
            ['20', '21', '', '23', '24'],
            ['30', '31', '32', '33', '34'],
            ['40', '41', '42', '43', '44']
           ]
    t = Table(
            data,
            style=[
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('GRID', (1, 1), (-2, -2), 1, colors.green),
                ('BOX', (0, 0), (1, -1), 2, colors.red),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                ('ALIGN', (0, 0), (4, 4), 'CENTER'),
                ('VALIGN', (0, 0), (4, 4), 'MIDDLE'),
                ],
            colWidths=[cw] * len(data[0]),
            rowHeights=[rh] * len(data),)
    w, h = t.wrapOn(c, W, H)
    t.drawOn(c, (W - w) // 2, (H - h) // 2)


@trans(M, M)
def draw_fonts(c, fonts=["Times-Roman", "Helvetica", "Courier"],
               dims=[10, 16, 22]):
    h = 40
    for font in fonts:
        for dim in dims:
            c.setFont(font, dim)
            c.drawCentredString(W // 2, H - h,
                    "Sixth Requirement: Fonts ({0} {1}).".format(font, dim))
            h += 20 * (dim * 0.1)


@trans(M, M)
def draw_ttfonts(c, fonts=["Argos-Regular", "kberry", "BluePlateSpecialNF"],
                 dims=[12, 18, 24]):
    h = 40
    for font in fonts:
        pdfmetrics.registerFont(TTFont(font, 'fonts/{0}.ttf'.format(font)))
        for dim in dims:
            c.setFont(font, dim)
            c.drawCentredString(W // 2, H - h,
                    "Sixth Requirement (b): T.T. Fonts ({0} {1})."
                    .format(font, dim))
            h += 20 * (dim * 0.1)


@trans(M, M)
def draw_bc(c, codes=['21557308', 'PINGU', "123456789"]):
    c.setStrokeColor(colors.black)
    w, h = 0.5 * mm, 15 * mm
    hoffset, hoffset_add = 4 * cm, 2 * cm

    for code in codes:
        barcode = code39.Standard39(
                        code,
                        barWidth=w,
                        barHeight=h,
                        checksum=0)
        barcode.drawOn(c, (W - barcode.width) // 2, H - hoffset)
        c.drawCentredString(W // 2, H - hoffset - 16,
                "standard code39: {0}".format(code))
        hoffset += barcode.height + hoffset_add


@trans(M, M)
def all_in_one(c):
    # margin
    c.setStrokeColor(colors.black)
    c.rect(0, 0, W, H)

    # img
    img_file = 'eggs.jpg'
    img = Image.open(img_file)
    w, h = img.size
    ratio = 0.3
    w, h = w * ratio, h * ratio
    c.drawImage(img_file, 12, H - 12 - h, w, h)

    # paragraph text
    style = getSampleStyleSheet()['Normal']
    style = ParagraphStyle(
                name='pingu_style',
                borderWidth=1,
                borderColor='#000000',
                backColor='#eeffee',
                borderPadding=12)
    p = Paragraph(
            "Hi, I am a very simple paragraph<br />This is the "
            "'all together' demo!", style)
    aw, ah = W, H
    w, h = p.wrap(aw * 0.4, ah)
    p.drawOn(c, W - w - 24, ah - h - 60)

    # circles
    c.setLineWidth(1)
    c.circle(W // 2, H // 2, 30, stroke=1, fill=0)

    # table
    cw, rh = 20, 16
    data = [range(3), range(3, 6), range(6, 9)]
    t = Table(
            data,
            style=[
                ('GRID', (0, 0), (2, 2), 0.5, colors.grey),
                ('ALIGN', (0, 0), (2, 2), 'CENTER'),
                ('VALIGN', (0, 0), (2, 2), 'MIDDLE'),
                ],
            colWidths=[cw] * len(data[0]),
            rowHeights=[rh] * len(data),)
    w, h = t.wrapOn(c, W, H)
    t.drawOn(c, 60, 120)

    # fonts
    c.setFont("Helvetica", 16)
    c.drawCentredString(W // 2, H - 200,
            "Standard Font: ({0} {1}).".format("Helvetica", 16))

    # pdfmetrics.registerFont(TTFont('kberry', 'fonts/kberry.ttf'))
    c.setFont('kberry', 24)

    c.drawCentredString(W // 2, H - 260,
            "True Type Font: ({0} {1}).".format("kberry.ttf", 24))

    # barcode
    code = '1234567890'
    w, h = 0.5 * mm, 12 * mm
    barcode = code39.Standard39(
                        code,
                        barWidth=w,
                        barHeight=h,
                        checksum=0)
    barcode.drawOn(c, (W - barcode.width) // 2, H // 2 - 100)
    c.setFont("Helvetica", 14)
    c.drawCentredString(W // 2, H // 2 - 130, "standard39: {0}".format(code))


if __name__ == "__main__":

    c = canvas.Canvas(
            "example.pdf",
            pagesize=A4)
    c.setAuthor("Fabrizio Romano <fabrizio.romano@glassesdirect.co.uk>")
    c.setTitle("My first reportlab example")

    # first requirement: margin box around the page
    draw_margin_box(c)
    c.drawCentredString(
        W // 2, H // 2, "First Requirement: margin box around the whole page")
    c.showPage()

    # second requirement: image
    draw_centered_img(c, "eggs.jpg", ratio=0.6)
    c.drawCentredString(
        W // 2, H // 2 + 160, "Second Requirement: image drawn in the page")
    c.drawCentredString(
        W // 2, H // 2 + 140, "with a little bit of drama.")
    c.showPage()

    # third requirement: paragraph text
    with open('example_text.txt') as f:
        text = [line.strip() for line in f.readlines()]
        text = '<br />'.join(text)

    draw_paragraph_text(c, text)
    c.drawCentredString(
            W // 2, H - 10, "Third Requirement: paragraph in the page.")
    c.showPage()

    # fourth requirement: circles
    draw_centered_circle(c,
            (colors.black, colors.greenyellow, colors.red, colors.aqua))
    c.drawCentredString(W // 2, H - 160, "Fourth Requirement: circles.")
    c.showPage()

    # fifth requirement: table
    draw_table(c)
    c.drawCentredString(W // 2, H - 160, "Fifth Requirement: a table.")
    c.showPage()

    # sixth requirement: fonts
    draw_fonts(c)
    c.showPage()

    # sixth requirement (b): fonts
    draw_ttfonts(c)
    c.showPage()

    # seventh: barcode in the ideal world
    draw_bc(c)
    c.drawCentredString(W // 2, H - 30, "Seventh Requirement: the ideal world")
    c.showPage()

    all_in_one(c)
    c.showPage()

    c.save()
