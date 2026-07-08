from ai.interpreter import interpret
from solver.sympy_solver import solve_expression
from voice.speech import SpeechRecognizer

import threading
import sympy as sp
import customtkinter as ctk

from gui.theme import apply_theme
from gui.theme import COLORS
from gui.theme import APP_TITLE

from gui.widgets import create_textbox
from gui.widgets import create_button


class MathPilot(ctk.CTk):

    def __init__(self):

        apply_theme()

        super().__init__()

        self.title(APP_TITLE)

        self.geometry("1000x700")

        self.configure(
            fg_color=COLORS["background"]
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.speech = SpeechRecognizer()

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="MathPilot AI",
            font=("Segoe UI", 32, "bold")
        )

        title.pack(pady=(20, 10))

        self.question_box = create_textbox(self)

        self.question_box.pack(
            fill="both",
            expand=False,
            padx=30,
            pady=10
        )

        self.question_box.configure(height=180)

        self.answer_box = create_textbox(self)

        self.answer_box.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.answer_box.insert(
            "1.0",
            "Answer will appear here..."
        )

        self.answer_box.configure(state="disabled")

        self.solve_button = create_button(
            self,
            "Solve",
            self.solve
        )

        self.solve_button.pack(
            pady=(15, 5)
        )

        self.voice_button = create_button(
            self,
            "🎤 Voice",
            self.start_voice
        )

        self.voice_button.pack(
            pady=(0, 15)
        )

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Segoe UI", 14)
        )

        self.status.pack(
            pady=10
        )

        self.question_box.bind(
            "<Return>",
            self.enter_pressed
        )

    def enter_pressed(self, event):
        self.voice_button.configure(state="normal")
        self.solve()

        return "break"

    def start_voice(self):

        self.voice_button.configure(state="disabled")

        self.status.configure(
            text="Listening..."
        )

        thread = threading.Thread(
            target=self.voice_worker,
            daemon=True
        )

        thread.start()

    def voice_worker(self):

        try:

            text = self.speech.listen()

            self.after(
                0,
                lambda: self.voice_finished(text)
            )

        except Exception as e:

            self.after(
                0,
                lambda: self.voice_failed(str(e))
            )

    def voice_finished(self, text):

        self.question_box.delete(
            "1.0",
            "end"
        )

        self.question_box.insert(
            "1.0",
            text
        )

        self.solve()

    def voice_failed(self, message):

        self.voice_button.configure(
            state="normal"
        )

        self.status.configure(
            text=message
        )
    def solve(self):

        question = self.question_box.get("1.0", "end").strip()

        if not question:

            self.voice_button.configure(state="normal")

            return

        self.status.configure(text="Thinking...")

        self.update()

        try:

            expression = interpret(question)

            answer = solve_expression(expression)

            try:

                numeric = sp.N(answer)

                if numeric != answer:

                    output = f"{answer}\n\n≈ {numeric}"

                else:

                    output = str(answer)

            except Exception:

                output = str(answer)

            self.answer_box.configure(state="normal")

            self.answer_box.delete("1.0", "end")

            self.answer_box.insert("1.0", output)

            self.answer_box.configure(state="disabled")

            self.question_box.delete("1.0", "end")

            self.question_box.focus_set()

            self.status.configure(text="Ready")

        except Exception as e:

            self.answer_box.configure(state="normal")

            self.answer_box.delete("1.0", "end")

            self.answer_box.insert("1.0", f"Error:\n{e}")

            self.answer_box.configure(state="disabled")

            self.status.configure(text="Error")

        finally:

            self.voice_button.configure(state="normal")


def run_app():

    app = MathPilot()

    app.mainloop()