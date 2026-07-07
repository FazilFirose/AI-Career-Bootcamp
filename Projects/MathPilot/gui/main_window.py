import threading

import customtkinter as ctk

from gui.theme import APP_TITLE, COLORS, apply_theme
from gui.widget import build_action_button, build_section
from voice import listen


class MathPilotApp(ctk.CTk):
    def __init__(self):
        apply_theme()
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("980x720")
        self.minsize(760, 560)
        self.configure(fg_color=COLORS["background"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_workspace()
        self._build_status_bar()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 12))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text=APP_TITLE,
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=30, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Phase 2 interface",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=14),
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

    def _build_workspace(self) -> None:
        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=1, column=0, sticky="nsew", padx=28, pady=12)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(0, weight=1)

        question_frame, self.question_textbox = build_section(
            workspace,
            "Question",
            "Type your math question here...",
        )
        question_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        answer_frame, self.answer_textbox = build_section(
            workspace,
            "Answer",
            "Answer will appear here in a future phase.",
            readonly=True,
        )
        answer_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    def _build_status_bar(self) -> None:
        footer = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=8,
        )
        footer.grid(row=2, column=0, sticky="ew", padx=28, pady=(12, 24))
        footer.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            footer,
            text="Waiting...",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=14),
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=18, pady=16)

        upload_button = build_action_button(
            footer,
            "Upload Image",
            self._on_upload_image,
            secondary=True,
        )
        upload_button.grid(row=0, column=1, sticky="e", padx=(8, 10), pady=12)

        voice_button = build_action_button(
            footer,
            "\U0001F3A4 Voice",
            self._on_voice,
            secondary=True,
        )
        voice_button.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=12)

        solve_button = build_action_button(footer, "Solve", self._on_solve)
        solve_button.grid(row=0, column=3, sticky="e", padx=(0, 12), pady=12)

    def _on_solve(self) -> None:
        self.status_label.configure(text="Solving will be added in a future phase.")

    def _on_upload_image(self) -> None:
        self.status_label.configure(text="Image upload will be added in a future phase.")

    def _on_voice(self) -> None:
        self.status_label.configure(text="Listening...")
        self.update_idletasks()

        thread = threading.Thread(target=self._listen_for_voice, daemon=True)
        thread.start()

    def _listen_for_voice(self) -> None:
        try:
            recognized_text = listen()
        except RuntimeError as exc:
            self.after(0, self._show_voice_error, str(exc))
            return

        self.after(0, self._apply_voice_text, recognized_text)

    def _apply_voice_text(self, recognized_text: str) -> None:
        self.question_textbox.delete("1.0", "end")
        self.question_textbox.insert("1.0", recognized_text)
        self.status_label.configure(text="Ready")

    def _show_voice_error(self, message: str) -> None:
        self.status_label.configure(text=f"Voice error: {message}")


def run_app() -> None:
    app = MathPilotApp()
    app.mainloop()
