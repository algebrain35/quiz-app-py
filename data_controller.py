from dao.question_dao import QuestionAnswerDao
import random

class DataController:
    def __init__(self, db_str, answer_table, question_table):
        self.question_dao = QuestionAnswerDao(db_str, answer_table, question_table)
        self.delim = '|'
        self.answer_idx_delim = '~'
    def fetch_questions(self, category_id):
        qas = self.question_dao.fetch_qas(category_id)
        parsed = self.parse_qas(qas)

        return sorted(parsed, key = lambda k: random.random())
    def parse_qas(self, qas) -> list[tuple[str, list[str], int]]:
        parsed = []
        
        for qa in qas:
            question = qa[0]
            if question == "": continue
            print(qa[1])
            answer_pairs = qa[1].split(self.delim)
            answers = []
            idx = None
            for i in range(len(answer_pairs)):
                split = answer_pairs[i].split(self.answer_idx_delim)
                if(len(split) < 2):
                    continue
                if split[0] == '' or split[1] == '': continue
                try:
                    ans, corr = split[0], int(split[1])
                except:
                    continue
                idx = i if corr == 1 else idx
                answers.append(ans)

                                
            parsed.append((question, answers, idx))
        return parsed

if __name__ == "__main__":
    dc = DataController("qa.db", "questions", "answers")

