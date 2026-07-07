import customtkinter as ctk


APP_TITLE = "MathPilot AI"

COLORS = {
    "background": "#080B12",
    "surface": "#101624",
    "surface_alt": "#151D2E",
    "border": "#26324A",
    "text": "#F4F7FB",
    "muted": "#9CA8BA",
    "accent": "#00D1FF",
    "accent_hover": "#00A8CC",
    "secondary": "#7C4DFF",
    "secondary_hover": "#6438D1",
}


def apply_theme() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
