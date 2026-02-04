from tkinter import ttk
import tkinter as tk
import sys
import time
class HomePage(ttk.Frame):
    def __init__(self, parent, ui_controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.ui_controller = ui_controller # ui_controller means main app window
        #self.ui_controller.config(bg='skyblue')
        self.welcome_label = ttk.Label(self,
                              text="Welcome to Quiz App!",
                              font=('ariel', 20, 'bold'))
        self.welcome_label.grid(row=0, column=1);
        start = ttk.Button(self,
                       text="Start",
                       command=self.next)
        start.grid(row=4, column=3, padx=5, pady=5)
        
        btn_exit = ttk.Button(self, text="Exit", command=self.exit)

        btn_exit.grid(row=4, column=4)
    def next(self):
        self.ui_controller.show_frame("start")
        self.ui_controller.title("Start Quiz!")
    def exit(self):
        sys.exit(0)
class StartPage(ttk.Frame):
    def __init__(self, parent, ui_controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.ui_controller = ui_controller  
        self.categories = [2947, 2006, 2406, 1001]  
        self.radio_buttons = []
        self.button_selected = tk.IntVar()

        
        self.start_label = ttk.Label(
            self,
            text="Select category",
            font=('ariel', 20)
        )

        
        self.start_label.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        
        for i, cat in enumerate(self.categories, start=1):
            r = ttk.Radiobutton(self, text=str(cat), variable=self.button_selected, value=cat)
            self.radio_buttons.append(r)
            r.grid(row=i, column=0, padx=5, pady=5, sticky="w")

        
        start_button = ttk.Button(self, text="Submit", command=self.start_quiz)
        start_button.grid(row=len(self.categories) + 1, column=0, pady=10, sticky="ew")

        btn_exit = ttk.Button(self, text="Exit", command=self.exit)

        btn_exit.grid(row=4, column=4)
        self.grid_columnconfigure(0, weight=1)
    def start_quiz(self):
        category = self.button_selected.get()
        self.ui_controller.set_category(category)
        self.ui_controller.fetch_questions()
        self.ui_controller.next_question_frame()
        self.ui_controller.show_frame("question")
    def exit(self):
        sys.exit(0)

class QuestionPage(ttk.Frame):
    def __init__(self, parent, ui_controller, qa):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.ui_controller = ui_controller
        self.radio_buttons = []
        self.button_selected = tk.IntVar()
        self.question = qa[0]
        self.answers = qa[1]

        self.question_label = ttk.Label(
            self,
            text=self.question,
            font=('ariel', 20)
        )
        self.question_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        for i, ans in enumerate(self.answers, start=1):
            r = ttk.Radiobutton(self, text=ans, variable=self.button_selected, value=i - 1)
            self.radio_buttons.append(r)

            r.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        btn_next = ttk.Button(self, text="Next", command=self.next)
        btn_next.grid(row=4, column=6)
        btn_exit = ttk.Button(self, text="Exit", command=self.exit)

        btn_exit.grid(row=4, column=4)
    def highlight_correct(self):
        corr_style = ttk.Style()
        valid = self.ui_controller.valid_index()
        corr_style.configure("Correct.TRadiobutton", background="green", foreground="white")
        self.radio_buttons[valid].configure(style="Correct.TRadiobutton")
    def next(self):
        button_val = self.button_selected.get()
        self.ui_controller.update_score(button_val)
        self.ui_controller.reveal_answer_frame()
        self.ui_controller.show_frame("answer")
        
        #idx = self.ui_controller.update_score(button_val)
        #self.ui_controller.print_valid_answer() 
        #self.ui_controller.next_question_frame()
        #self.ui_controller.show_frame("question")
    def exit(self):
        sys.exit(0)

class RevealAnswerPage(ttk.Frame):
    def __init__(self, parent, ui_controller, qa):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.ui_controller = ui_controller
        self.radio_buttons = []
        self.button_selected = tk.IntVar()
        self.question = qa[0]
        self.answers = qa[1]
        self.style = ttk.Style()
        self.configure_styles()
        self.question_label = ttk.Label(
            self,
            text=self.question,
            font=('ariel', 20)
        )
        self.question_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.display_buttons()
        btn_next = ttk.Button(self, text="Next!", command=self.next)
        btn_next.grid(row=4, column=6)
        btn_exit = ttk.Button(self, text="Exit", command=self.exit)
        btn_exit.grid(row=4, column=4)
        self.grid_columnconfigure(0, weight=1)
    def configure_styles(self):
        self.style.configure(
            'Correct.TRadiobutton', 
            foreground='green', 
            font=('Arial', 10, 'bold')
        )
    def display_buttons(self):
        correct_idx = self.ui_controller.valid_index()
        for i, ans in enumerate(self.answers, start=1):
            button_style = 'Correct.TRadiobutton' if i - 1 == correct_idx else 'TRadiobutton'
            r = ttk.Radiobutton(self, text=ans, variable=self.button_selected, value=i, style=button_style)
            r.grid(row=i, column=0, padx=5, pady=5, sticky='w')
    def next(self):
        self.ui_controller.next_question_frame()
        self.ui_controller.show_frame("question")

    def exit(self):
        sys.exit(0)
            





class FinalScorePage(ttk.Frame):
    def __init__(self, parent, ui_controller):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.ui_controller = ui_controller

        score = self.ui_controller.score
        score_label = ttk.Label(self,
                                text=f"Score: \t{score * 100:.2f}",
                                font=("ariel",20))

        score_label.grid(row=1, column=0)
        btn_next = ttk.Button(self, text="Home Page", command=self.next)
        btn_next.grid(row=4, column=6)
        btn_exit = ttk.Button(self, text="Exit", command=self.exit)
        btn_exit.grid(row=4, column=4)
    def exit(self):
        sys.exit(0)
    def next(self):
        self.ui_controller.show_frame("home")

        

        
        



        
        
        
