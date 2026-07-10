import customtkinter as ctk
from gui.theme import COLORS


def create_textbox(parent):

    textbox = ctk.CTkTextbox(
        parent,
        fg_color=COLORS["textbox"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=28,
        font=("Segoe UI Variable",16),
        text_color=COLORS["text"],
        wrap="word"
    )

    return textbox


def create_button(parent,text,command):

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=48,
        corner_radius=20,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        font=("Segoe UI Variable",15,"bold")
    )