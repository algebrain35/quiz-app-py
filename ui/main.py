from tkinter import ttk
import tkinter as tk
from .frames.HomePage import FinalScorePage, HomePage, RevealAnswerPage, StartPage, QuestionPage
import data_controller as dc
import queue

MAX_QUIZ_LEN = 35

class MainUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.buffer = queue.LifoQueue(MAX_QUIZ_LEN)
        self.category = 0
        self.score = 0
        self.curr_question = None, None, None
        self.num_questions = 0
        self.quiz_state = (self.score, self.num_questions)
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.data_controller = dc.DataController("qa.db", "questions", "answers") 
        self.title("Quiz App")
        self.geometry("800x400")
        
        self.callbacks = {}
        self.frame_list = {}
        self.question_frames = []

        home_frame = HomePage(self.container, self)
        home_frame.grid(row=0, column=0, sticky="nsew")
        self.frame_list["home"] = home_frame

        start_frame = StartPage(self.container, self)
        start_frame.grid(row=0, column=0, sticky="nsew")
        self.frame_list["start"] = start_frame

    def show_frame(self, frame_name):
        if not frame_name in self.frame_list.keys():
            return
        frame = self.frame_list[frame_name]
        frame.tkraise()
    def load_question(self, question):
        if self.num_questions >= MAX_QUIZ_LEN:
            return
        self.buffer.put(question)
        self.num_questions += 1
    def cleanup(self):
        return
    def destroy(self):
        return
    def set_category(self, category):
        self.category = category
    def load_questions(self, questions):
        for qa in questions:
            self.load_question(qa)
    def fetch_questions(self):
        if not self.category:
            return
        else:
            qas = self.data_controller.fetch_questions(self.category)
            self.load_questions(qas)

    def next_question_frame(self):
        if(self.buffer.empty()):
            self.frame_list["question"] = FinalScorePage(self.container, self)
            self.frame_list["question"].grid(row=0, column=0, sticky="nsew")
            return
        else:
            qa = self.buffer.get()
            self.curr_question = qa
            question_page = self.question_page(qa)
            question_page.grid(row=0, column=0, sticky="nsew")

            self.frame_list["question"] = question_page
    def reveal_answer_frame(self):
        if self.curr_question == (None, None, None):
            return
        answer_page = self.answer_page(self.curr_question)
        answer_page.grid(row=0, column=0, sticky="nsew")

        self.frame_list["answer"] = answer_page


    def update_score(self, val: int):
        correct = self.valid_answer(val)
        self.score += correct * 1 / self.num_questions

        return self.valid_index()
    def question_page(self, qa):
        return QuestionPage(self.container, self, qa)
    def answer_page(self, qa):
        return RevealAnswerPage(self.container, self, qa)
    def valid_answer(self, val: int):
        return 1 if val == self.valid_index() else 0
    def valid_index(self):
        return self.curr_question[2]
    def get_curr_question(self):
        return self.curr_question        
    def print_valid_answer(self):
        q_text, ans, idx = self.curr_question
        if q_text != None and ans != None and idx != None:
            print(f"{q_text}")
            print(f"Correct: {idx} \t\t Answer:{ans[idx]}")

if __name__ == "__main__":
    main = MainUI()
    main.show_frame("home")
    main.mainloop()
