import docx
from docx.shared import Pt, RGBColor, Inches

def create_doc():
    doc = docx.Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    title = doc.add_heading(level=1)
    run_t = title.add_run("Resposta Técnica ao Parecer nº 10: Consolidação CLG-R (Versão 2.0)")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(16, 44, 87)
    
    with open(r"C:\MathDoCarvalho\P_NP\Publicacoes\RespostaAoProfessor_Analise10.md", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        text = line.strip()
        if not text or text.startswith("# Resposta Técnica"):
            continue
        if text.startswith("---"):
            continue
        if text.startswith("## "):
            h = doc.add_heading(level=2)
            r = h.add_run(text[3:])
            r.font.name = "Calibri"
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = RGBColor(27, 72, 140)
        elif text.startswith("### "):
            h = doc.add_heading(level=3)
            r = h.add_run(text[4:])
            r.font.name = "Calibri"
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(40, 40, 40)
        elif text.startswith("#### "):
            h = doc.add_heading(level=4)
            r = h.add_run(text[5:])
            r.font.name = "Calibri"
            r.font.size = Pt(11)
            r.font.bold = True
        else:
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(11)
            
    doc.save(r"C:\MathDoCarvalho\P_NP\Publicacoes\RespostaAoProfessor_Analise10.docx")
    doc.save(r"C:\MathDoCarvalho\RespostaAoProfessor_Analise10.docx")
    print("DOCX gerado com sucesso!")

if __name__ == "__main__":
    create_doc()
