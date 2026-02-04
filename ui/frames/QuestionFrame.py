import tkinter as tk
from tkinter import ttk
import time

class QuestionFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.question_title = None
        self.answers = None
        self.radio_buttons = []
    def _init_qa(self, question, answers):
        self.question_title = question
        self.answers = answers
    def _setup_qa(self):
        assert(self.question_title is not None)
        assert(self.answers is not None)
        selected = tk.IntVar()
        q_button = ttk.Label(self,
                         text=self.question_title,
                         font=('ariel', 30))
        q_button.pack()
        for i in range(len(self.answers)):
            r = ttk.Radiobutton(self, text=self.answers[i], value=i, variable=selected)
            self.answers.append(r)
            r.pack(fill='x', padx=5, pady=5)
        submit_button = ttk.Button(self,
                               text="Submit",
                                   command= lambda : self.pack_forget())
        submit_button.pack()
        self.pack() # packs frame onto parent
if __name__ == "__main__":
    root = tk.Tk()
    frame = QuestionFrame(root)
    frame._init_qa("Sky color?", ["blue", "green", "red", "white"])
    frame._setup_qa()

    
    
    frame1 = QuestionFrame(root)
    frame1._init_qa("What color is sky?", ["blue", "green", "red", "white"])
    frame1._setup_qa()
    root.mainloop()

            
            
        
        



        
    
