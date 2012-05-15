# -*- coding: utf-8 -*-
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm, inch
import PIL


W, H = defaultPageSize
styles = getSampleStyleSheet()

title = "Flowables example title"
pageinfo = "platypus example"
im = PIL.Image.open("eggs.jpg")
im_width, im_height = im.size[0] // 3, im.size[1] // 3


def my_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.drawCentredString(W // 2, H - 108, title)
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "First Page / {0}".format(pageinfo))
    canvas.restoreState()


def my_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "Page {0} {1}".format(doc.page, pageinfo))


def go():
    doc = SimpleDocTemplate("flowables.pdf")
    story = [Spacer(1, 2 * cm)]
    style = styles["Normal"]
    for i in xrange(20):
        bogustext = ("This is paragraph number {0}.".format(i)) * 20
        p = Paragraph(bogustext, style)
        story.append(p)
        story.append(Spacer(1, 0.2 * cm))
        story.append(Image("eggs.jpg", im_width, im_height))
    doc.build(story, onFirstPage=my_first_page, onLaterPages=my_later_pages)


go()
