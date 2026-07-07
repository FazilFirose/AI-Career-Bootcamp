from fpdf import FPDF

def clean_text(value):
    """Convert to string, remove unsupported characters, break long words."""
    text = str(value)  # force to string in case it's a number or something odd
    text = text.encode("latin-1", "ignore").decode("latin-1")

    safe_words = []
    for word in text.split(" "):
        if len(word) > 40:
            chunks = [word[i:i+40] for i in range(0, len(word), 40)]
            safe_words.append(" ".join(chunks))
        else:
            safe_words.append(word)
    return " ".join(safe_words) if safe_words else " "


def safe_multicell(pdf, text, label=""):
    """Write text to the PDF, printing debug info if it fails."""
    try:
        pdf.set_x(pdf.l_margin)  # force cursor back to left margin
        pdf.multi_cell(0, 6, clean_text(text))
    except Exception as e:
        print(f"--- PDF ERROR on field [{label}] ---")
        print(f"Raw value: {repr(text)}")
        print(f"Error: {e}")
        pdf.multi_cell(0, 6, "[Content could not be displayed]")


def generate_pdf(study_data, subject_code, days_left):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    safe_multicell(pdf, f"PrepPilot AI - Quick Revision: {subject_code}", "title")
    pdf.set_font("Helvetica", "", 11)
    safe_multicell(pdf, f"{days_left} day(s) left until exam", "days_left")
    pdf.ln(5)

    for module in study_data["modules"]:
        pdf.set_font("Helvetica", "B", 13)
        safe_multicell(pdf, module["name"], "module_name")
        pdf.ln(2)

        pdf.set_font("Helvetica", "", 10)
        for point_data in module["key_points"]:
            pdf.set_font("Helvetica", "B", 10)
            safe_multicell(pdf, f"- {point_data['point']}", "key_point_title")
            pdf.set_font("Helvetica", "", 9)
            safe_multicell(pdf, point_data["content"], "key_point_content")
            pdf.ln(1)

        pdf.ln(5)

    return bytes(pdf.output())