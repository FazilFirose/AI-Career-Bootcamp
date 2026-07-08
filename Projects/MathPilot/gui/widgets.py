import customtkinter as ctk
from gui.theme import COLORS


def create_textbox(parent):

    textbox = ctk.CTkTextbox(
        parent,
        fg_color=COLORS["textbox"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=12,
        font=("Segoe UI",16),
        text_color="white",
        wrap="word"
    )

    return textbox


def create_button(parent,text,command):

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=45,
        corner_radius=12,
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        font=("Segoe UI",15,"bold")
    )