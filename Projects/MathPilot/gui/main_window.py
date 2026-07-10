from ai.interpreter import interpret
from solver.sympy_solver import solve_expression
from voice.speech import SpeechRecognizer
from voice.tts import Speaker
from voice.voice_controller import VoiceController
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
        self.speaker = Speaker()

        self.voice_mode = False
        self.voice_controller = VoiceController(
         self.on_voice_question,
         self.update_status
        )
        self.voice_controller.start()


        self.build_ui()

    def build_ui(self):

     # ================= HEADER =================

     header = ctk.CTkFrame(
        self,
        fg_color="transparent"
     )
 
     header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
     )

     title = ctk.CTkLabel(
        header,
        text="🧠 MathPilot AI",
        font=("Segoe UI Variable", 42, "bold"),
        text_color=COLORS["text"]
     )

     title.pack(anchor="w")

     subtitle = ctk.CTkLabel(
        header,
        text="Your AI Mathematics Assistant",
        font=("Segoe UI Variable", 16),
        text_color=COLORS["secondary_text"]
     )

     subtitle.pack(anchor="w", pady=(5, 0))

     #================== TOOLBAR=================

     toolbar = ctk.CTkFrame(
      self,
      fg_color="transparent"
     )

     toolbar.pack(
      fill="x",
      padx=30,
      pady=(5,15)
     )

     version = ctk.CTkLabel(
      toolbar,
      text="Version 1.0",
      font=("Segoe UI Variable",13),
      text_color=COLORS["secondary_text"]
     )

     version.pack(side="left")

     mode = ctk.CTkLabel(
      toolbar,
      text="AI • Voice • SymPy",
      font=("Segoe UI Variable",13),
      text_color=COLORS["secondary_text"]
     )

     mode.pack(side="right")

     # ================= STATUS =================

     status_frame = ctk.CTkFrame(
        self,
        fg_color="transparent"
     )

     status_frame.pack(
        fill="x",
        padx=30,
        pady=(10, 20)
     )

     self.mic_indicator = ctk.CTkLabel(
        status_frame,
        text="🎤",
        font=("Segoe UI Emoji", 36),
        text_color=COLORS["secondary_text"]
     )

     self.mic_indicator.pack(
        side="left",
        padx=(0, 10)
     )

     self.status = ctk.CTkLabel(
        status_frame,
        text='🟢 Waiting for "Math"...',
        font=("Segoe UI Variable", 15, "bold"),
        text_color=COLORS["success"]
     )

     self.status.pack(side="left")

     # ================= MAIN CONTENT =================

     main_frame = ctk.CTkFrame(
        self,
        fg_color="transparent"
     )

     main_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
     )

     main_frame.grid_columnconfigure(0, weight=1)
     main_frame.grid_columnconfigure(1, weight=1)
     main_frame.grid_rowconfigure(0, weight=1)

     # ================= QUESTION =================

     question_card = ctk.CTkFrame(
       main_frame,
       fg_color=COLORS["card"],
       corner_radius=28,
       border_width=1,
       border_color=COLORS["border"]
     )

     question_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 10)
     )

     question_label = ctk.CTkLabel(
        question_card,
        text="Ask your question",
        font=("Segoe UI Variable", 16, "bold"),
        text_color=COLORS["text"]
     )

     question_label.pack(
        anchor="w",
        padx=20,
        pady=(18, 8)
     )

     self.question_box = create_textbox(question_card)

     self.question_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
     )

     self.question_box.configure(
        height=420
     )

     self.question_box.bind(
        "<Return>",
        self.enter_pressed
     )

     # ================= ANSWER =================

     answer_card = ctk.CTkFrame(
      main_frame,
      fg_color=COLORS["card"],
      corner_radius=28,
      border_width=1,
      border_color=COLORS["border"]
    )

     answer_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(10, 0)
     )

     answer_label = ctk.CTkLabel(
        answer_card,
        text="Answer",
        font=("Segoe UI Variable", 18, "bold"),
        text_color=COLORS["text"]
     )

     answer_label.pack(
        anchor="w",
        padx=20,
        pady=(18, 8)
     )

     self.answer_box = create_textbox(answer_card)

     self.answer_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
     )

     self.answer_box.insert(
        "1.0",
        "Answer..."
     )

     self.answer_box.configure(
        state="disabled"
     )

     # ================= BUTTON =================

     self.solve_button = create_button(
      self,
        "✨ Solve",
        self.solve
     )

     self.solve_button.pack(
        pady=(0, 25)
     )

    def enter_pressed(self, event):
        
        self.solve()

        return "break"
    def solve(self):

     question = self.question_box.get("1.0", "end").strip()

     if not question:

        
        return

     self.update_status("🟣 Thinking")
     self.animate_thinking()
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

        if self.voice_mode:

            try:

                if "≈" in output:

                    try:

                     spoken = str(round(float(sp.N(answer)), 2))

                    except Exception:

                     spoken = str(round(float(sp.N(answer)), 2))

                else:

                    spoken = str(round(float(sp.N(answer)), 2))

                threading.Thread(
                  target=self.speaker.speak,
                  args=(spoken,),
                  daemon=True
                ).start()

            except Exception:

                pass

            self.voice_mode = False

        self.question_box.delete("1.0", "end")

        self.question_box.focus_set()

        self.status.configure(text='Waiting for "Math"...')

     except Exception as e:

        self.answer_box.configure(state="normal")
        self.answer_box.delete("1.0", "end")
        self.answer_box.insert("1.0", f"Error:\n{e}")
        self.answer_box.configure(state="disabled")

        self.status.configure(text="Error")
        self.status.configure(
          text='🟢 Waiting for "Math"...'
         )

    def on_voice_question(self, question):

     self.after(
        0,
        lambda: self.process_voice_question(question))
      


    def process_voice_question(self, question):

     self.voice_mode = True

     self.question_box.delete("1.0", "end")

     self.question_box.insert("1.0", question)

     self.solve()
    def update_status(self, text):

      def update():

        self.status.configure(text=text)

        if "Waiting" in text:

            self.status.configure(
                text_color=COLORS["success"]
            )

            self.mic_indicator.configure(
                text_color=COLORS["secondary_text"]
            )

        elif "Listening" in text:

            self.status.configure(
                text_color="#38BDF8"
            )
            self.pulse_microphone()
        elif "Thinking" in text:

            self.status.configure(
                text_color="#A855F7"
            )
            self.pulse_microphone()

        elif "Speaking" in text:

            self.status.configure(
                text_color="#F59E0B"
            )
            self.pulse_microphone()

        else:

            self.status.configure(
                text_color=COLORS["secondary_text"]
            )

            self.mic_indicator.configure(
                text_color=COLORS["secondary_text"]
            )

      self.after(0, update)
    def animate_thinking(self):

     dots = ["", ".", "..", "..."]

     index = 0

     def animate():

        nonlocal index

        if "Thinking" not in self.status.cget("text"):

            return

        self.status.configure(
            text=f"🟣 Thinking{dots[index]}"
        )

        index = (index + 1) % len(dots)

        self.after(350, animate)

     animate()
    def pulse_microphone(self):

     colors = [
        COLORS["secondary_text"],
        "#60A5FA",
        "#A855F7",
        "#60A5FA"
       ]

     index = 0

     def animate():

        nonlocal index

        status = self.status.cget("text")

        if ("Listening" not in status and
            "Thinking" not in status and
            "Speaking" not in status):
            return

        self.mic_indicator.configure(
            text_color=colors[index]
        )

        index = (index + 1) % len(colors)

        self.after(250, animate)

     animate()



def run_app():

    app = MathPilot()

    app.mainloop()