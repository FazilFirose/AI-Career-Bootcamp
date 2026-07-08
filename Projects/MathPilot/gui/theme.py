import customtkinter as ctk

APP_TITLE = "MathPilot AI"

COLORS = {
    "background": "#0B1120",
    "surface": "#141B2D",
    "textbox": "#1B2438",
    "border": "#2C3A55",
    "accent": "#00D4FF",
    "accent_hover": "#00B8E0",
    "text": "#FFFFFF",
    "secondary_text": "#9DA8C3",
}


def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")