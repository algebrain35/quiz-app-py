import sqlite3
from typing import List, Optional
from utils import quiz_utils
def TABLE_EXISTS_QUERY(table_name: str):
    return f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"

CREATE_QUESTIONS = f''' 
CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    category_id INTEGER
    )
'''

CREATE_ANSWERS= f'''
CREATE TABLE IF NOT EXISTS answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
)
'''

def CREATE_TABLE_QUERY(table: str) -> str:
    if table == "questions":
        return CREATE_QUESTIONS
    elif table == "answers":
        return CREATE_ANSWERS
    else:
        return ""
def INSERT_QUESTION_QUERY(table_name: str, question: tuple[str, int]):
    return f"INSERT INTO {table_name} (question_text, category_id) VALUES (?, ?)", (question[0], question[1])
def INSERT_ANSWER_QUERY(table_name: str, question_id: int, answer: tuple[str, bool]):
    return f"INSERT INTO {table_name} (question_id, answer_text, is_correct) VALUES (?, ?, ?)", (question_id, answer[0], answer[1])

def GET_QAS_QUERY(question_table: str,
                  answer_table: str,
                  col_names: tuple[str, str, str, str] = ("question_id", "question_text", "answer_text", "is_correct"),
                  category_id: int | None = None):
    category_str = "" if category_id == None else f"WHERE q.category_id = {category_id}"
    formatted_query = f'''
    SELECT q.{col_names[1]}, GROUP_CONCAT(CONCAT(a.{col_names[2]}, "~", a.{col_names[3]}),"|")
    FROM {question_table} as q
    LEFT JOIN {answer_table} as a ON q.{col_names[0]}=a.{col_names[0]}
    {category_str}
    GROUP BY q.{col_names[0]}
    '''
    return formatted_query
def convert_to_insert_format(qa: tuple[tuple[str, int, int], List[str]]) -> tuple[tuple[str, int], list[tuple[str, bool]]]:
    question_str, idx, category = qa[0]
    answers = qa[1]
    
    new_answers = [(answers[i], idx == i) for i in range(len(answers))]
    new_question = (question_str, category)

    return (new_question, new_answers)




class QuestionAnswerDao:
    def __init__(self, db_str, question_table, answer_table):
        self.db_str = db_str
        self.answer_table = answer_table
        self.question_table = question_table
        
    def _get_conn(self):
        conn = sqlite3.connect(self.db_str)
        return conn
    def _init_schema(self):
        self._create_table(self.question_table)
        self._create_table(self.answer_table)
        

    def _create_table(self, table_name):
        query = CREATE_TABLE_QUERY(table_name)
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
        except Exception as e:
            print(e)
    def execute_query(self, query, args, fetch_method="fetchone"):
        results = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            if not args == None:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            fn = getattr(cursor, fetch_method)
            if fn is None or not callable(fn):
                raise AttributeError(f"Method {fetch_method} is not found/callable.")

            

            results = fn()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        return results
    def add_question(self, question: tuple[str, int]) -> int | None:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            query, args = INSERT_QUESTION_QUERY(self.question_table, question)
            cursor.execute(query, args)
            return cursor.lastrowid

    def add_questions(self, questions: List[tuple[str, int]]):
        row_ids = []
        for question in questions:
            row_id = self.add_question(question)
            row_ids.append(row_id)
        return row_ids
    def add_answer(self, answer: tuple[str, bool], question_id: int):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            query, args = INSERT_ANSWER_QUERY(self.answer_table, question_id, answer)
            cursor.execute(query, args)
            return cursor.lastrowid
    def add_answers(self, answers: list[tuple[str, bool]], question_id: int):
        for answer in answers:
            self.add_answer(answer, question_id)
        return
    def add_questions_answers(self, qa: list[tuple[tuple[str, int, int], list[str]]]):
        try:
            for entry in qa:
                question, answers = convert_to_insert_format(entry)
                rowid = self.add_question(question)
                if rowid != None:
                    self.add_answers(answers, rowid)

        except Exception as e:
            print(e)
    def fetch_qas(self, category_id):
        query = GET_QAS_QUERY(self.question_table, self.answer_table, category_id=category_id)
        results = self.execute_query(query, None, "fetchall")
        return results


if __name__ == "__main__":
    qa_dao = QuestionAnswerDao("qa.db", "questions", "answers")
    #qa_dao._init_schema()
    qas = quiz_utils.parse_txt_file("COSC2406-Final.txt" , '@')
    qa_dao.add_questions_answers(qas)
    results = qa_dao.execute_query(GET_QAS_QUERY("questions", "answers"), None, "fetchall")
    print(results)
    




                      
