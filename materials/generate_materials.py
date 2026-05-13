"""根据 Markdown 源稿生成教师 Word 指导手册和课堂 PPT。"""

from pathlib import Path


def generate_word():
    from docx import Document

    source = Path('materials/teacher_lab_guide.md')
    document = Document()
    document.add_heading('无线通信技术实验指导手册', level=0)
    for line in source.read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):
            document.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            document.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            document.add_heading(line[4:], level=3)
        elif line.startswith('- '):
            document.add_paragraph(line[2:], style='List Bullet')
        elif line.strip().startswith('|') or line.startswith('```'):
            document.add_paragraph(line)
        elif line.strip():
            document.add_paragraph(line)
    document.save('materials/teacher_lab_guide.docx')


def generate_ppt():
    from pptx import Presentation
    from pptx.util import Inches, Pt

    slides = []
    current = None
    for line in Path('materials/lecture_slides_outline.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('## Slide'):
            if current:
                slides.append(current)
            title = line.split('：', 1)[-1] if '：' in line else line[3:]
            current = {'title': title, 'bullets': []}
        elif current and line.startswith('- '):
            current['bullets'].append(line[2:])
    if current:
        slides.append(current)

    presentation = Presentation()
    for index, item in enumerate(slides):
        layout = presentation.slide_layouts[0] if index == 0 else presentation.slide_layouts[1]
        slide = presentation.slides.add_slide(layout)
        slide.shapes.title.text = item['title']
        if index == 0:
            slide.placeholders[1].text = '无线通信技术 · 信道编码与信道均衡'
            continue
        body = slide.placeholders[1].text_frame
        body.clear()
        for bullet in item['bullets'][:6]:
            paragraph = body.add_paragraph()
            paragraph.text = bullet
            paragraph.level = 0
            paragraph.font.size = Pt(22)
    presentation.save('materials/lecture_slides.pptx')


def main():
    Path('materials').mkdir(exist_ok=True)
    generate_word()
    generate_ppt()
    print('已生成 materials/teacher_lab_guide.docx 和 materials/lecture_slides.pptx')


if __name__ == '__main__':
    main()
