from tkinter  import *
#class QuizUI(Tk):
 #   Tk.__init__(self)
 #   self.resizable(width=True, height=True)
    
    
if __name__ == "__main__":
    main = Tk()
    main.title('Quiz App')
    main.geometry('800x400')
    main.config(bg='skyblue')

    welcome_label = Label(main, text="Welcome to Python Quiz App!", font=('ariel', 20, 'bold'))
    start_quiz = Button(main, text="Start", command=lambda : print("Nothing"))
    start_quiz.pack(side='bottom')
    welcome_label.pack()
    main.mainloop()
