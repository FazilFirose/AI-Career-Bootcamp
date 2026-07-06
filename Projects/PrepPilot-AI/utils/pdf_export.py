from fpdf import FPDF

def generate_pdf(study_data, subject_code, days_left):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"PrepPilot AI - Study Map for {subject_code}", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 10, f"{days_left} day(s) left until exam", ln=True)
    pdf.ln(5)

    for module in study_data["modules"]:
        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(0, 8, module["name"])
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, f"Difficulty: {module['difficulty_score']}/10")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, "Key Points:")
        pdf.set_font("Helvetica", "", 10)
        for point in module["key_points"]:
            pdf.multi_cell(0, 6, f"- {point}")

        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, "Likely Questions:")
        pdf.set_font("Helvetica", "", 10)
        for q in module["likely_questions"]:
            pdf.multi_cell(0, 6, f"Q: {q['question']} ({q['marks']} marks)")
            pdf.multi_cell(0, 6, q["model_answer"])
            pdf.ln(1)

        pdf.ln(5)

    return pdf.output(dest="S").encode("latin-1")