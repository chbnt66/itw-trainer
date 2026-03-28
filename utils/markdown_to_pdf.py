from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue, orange, darkorange, orangered, salmon, lightsalmon, darksalmon

from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import os



class MarkdownPDF : 

    def __init__(self, report) : 

        self.report = report

    def _add_logos_first_page(self, canvas, doc):
        width, height = A4

        big_logo = ImageReader("logo/logo_text_v2_no_background.png")
        small_logo = ImageReader("logo/logo_no_background.png")

        # Big logo (top-right)
        canvas.drawImage(
            big_logo,
            width - 8*cm,      # X position
            height - 3.5*cm,     # Y position
            width=7.5*cm,
            height=3.5*cm,
            preserveAspectRatio=True,
            mask='auto'
        )

        # Small logo (bottom-right)
        canvas.drawImage(
            small_logo,
            width - 3*cm,
            1*cm,
            width=2*cm,
            height=2*cm,
            preserveAspectRatio=True,
            mask='auto'
        )


    def _add_logo_other_pages(self, canvas, doc):
        width, height = A4

        small_logo = ImageReader("logo/logo_no_background.png")

        canvas.drawImage(
            small_logo,
            width - 3*cm,
            1*cm,
            width=2*cm,
            height=2*cm,
            preserveAspectRatio=True,
            mask='auto'
        )

    def build_pdf(self ): 

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle', 
            parent=styles["Title"], 
            spaceAfter = 10, 
            fontName="Times-Bold",
            fontSize = 22
        )

        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Heading2'],
            spaceAfter=10, 
            spaceBefore = 10,
            fontName="Times-Bold",
            fontSize = 14
        )

        feedback_style_global = ParagraphStyle(
            'FeedbackStyle',
            parent=styles['BodyText'],
            italic=True,
            spaceAfter=10, 
            fontName="Times",
            fontSize = 12, 
            
            )


        story = []

        # Title
        title = f"{self.report['report_title']}."
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 10))

        # Questions loop
        for nb, q in enumerate(self.report["questions"]):
            story.append(Paragraph(f"Q{nb+1}: {q['question']}", question_style))

            story.append(Paragraph(
                f"<font name='Times' size='12' color='orangered'><b>Candidate answer:</b></font> "
                f"<font name='Times' size='12'> {q['candidate_answer']}</font>",
                styles["BodyText"]
                )
                )
            
            story.append(Spacer(1, 10))
            
            story.append(Paragraph(
                f"<font name='Times' size='12' color='darksalmon'><b>Coach feedback:</b></font> "
                f"<font name='Times' size='12'> {q['feedback']}</font>",
                styles["BodyText"]
                )
                )
            
            story.append(Spacer(1, 20))

            

        story.append(Spacer(1, 20))
        story.append(Paragraph("Global Feedback.", question_style))
        story.append(Paragraph(self.report["global_feedback"], feedback_style_global))

        doc.build(story, onFirstPage= self._add_logos_first_page, onLaterPages = self._add_logo_other_pages)
        buffer.seek(0)
        return buffer