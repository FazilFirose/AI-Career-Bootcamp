import customtkinter as ctk

from gui.theme import COLORS


def build_section(parent, title: str, placeholder: str, *, readonly: bool = False):
    frame = ctk.CTkFrame(
        parent,
        fg_color=COLORS["surface"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=8,
    )
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    label = ctk.CTkLabel(
        frame,
        text=title,
        text_color=COLORS["text"],
        font=ctk.CTkFont(size=16, weight="bold"),
        anchor="w",
    )
    label.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 8))

    textbox = ctk.CTkTextbox(
        frame,
        fg_color=COLORS["surface_alt"],
        border_width=1,
        border_color=COLORS["border"],
        corner_radius=8,
        text_color=COLORS["text"],
        font=ctk.CTkFont(size=15),
        wrap="word",
    )
    textbox.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
    textbox.insert("1.0", placeholder)

    if readonly:
        textbox.configure(state="disabled")

    return frame, textbox


def build_action_button(parent, text: str, command, *, secondary: bool = False):
    color = COLORS["secondary"] if secondary else COLORS["accent"]
    hover = COLORS["secondary_hover"] if secondary else COLORS["accent_hover"]

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=44,
        corner_radius=8,
        fg_color=color,
        hover_color=hover,
        text_color="#FFFFFF",
        font=ctk.CTkFont(size=15, weight="bold"),
    )
