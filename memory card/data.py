from PyQt5.QtCore import*
from random import*

new_quest_templ = 'Нове запитання'
new_answer_templ = 'Нова відповідь'

text_wrong = 'Невірно'
text_correct = 'Вірно'

class Question():
    ''' зберігає інформацію про одне питання'''
    def __init__(self, question=new_quest_templ, answer=new_answer_templ,
                       wrong_answer1='', wrong_answer2='', wrong_answer3=''):
        self.question = question # питання
        self.answer = answer # правильна відповідь
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3
        self.is_active = True
        self.attempts = 0
        self.correct = 0
        
    def got_right(self):
        ''' змінює статистику, отримавши правильну відповідь'''
        self.attempts += 1
        self.correct += 1

    def got_wrong(self):
        ''' змінює статистику, отримавши неправильну відповідь'''
        self.attempts += 1

class QuestionView():
    ''' зіставляє дані та віджети для відображення запитання'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.frm_model = frm_model 
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3

    def change(self, frm_model):
        ''' оновлення даних, уже пов'язаних з інтерфейсом '''
        self.frm_model = frm_model

    def show(self):
        ''' виводить на екран усі дані з об'єкта '''
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_answer1)
        self.wrong_answer2.setText(self.frm_model.wrong_answer2)
        self.wrong_answer3.setText(self.frm_model.wrong_answer3)

class QuestionEdit(QuestionView):
    ''' використовується, якщо потрібно редагувати форму: встановлює обробники подій, які зберігають текст'''
    def save_question(self):
        ''' зберігає текст запитання '''
        self.frm_model.question = self.question.text() # копіюємо дані з віджета в об'єкт
    
    def save_answer(self):
        ''' зберігає текст правильної відповіді '''
        self.frm_model.answer = self.answer.text() # копіюємо дані з віджета в об'єкт
    
    def save_wrong(self):
        ''' зберігає всі неправильні відповіді'''
        self.frm_model.wrong_answer1 = self.wrong_answer1.text()
        self.frm_model.wrong_answer2 = self.wrong_answer2.text()
        self.frm_model.wrong_answer3 = self.wrong_answer3.text()
    def set_connects(self):
        ''' встановлює обробки подій у віджетах так, щоб зберігати дані '''
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong) 
        self.wrong_answer2.editingFinished.connect(self.save_wrong)
        self.wrong_answer3.editingFinished.connect(self.save_wrong)
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.set_connects()

class AnswerCheck(QuestionView):
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3, showed_answer, result):
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.showed_answer = showed_answer
        self.result = result
        
    def check(self):
        if self.answer.isChecked():
            # відповідь правильна, запишемо і відобразимо в статистиці
            self.result.setText(text_correct) # напис "вірно" або "невірно"
            self.showed_answer.setText(self.frm_model.answer) # пишемо сам текст відповіді у відповідному віджеті
            self.frm_model.got_right() # оновити статистику, додавши одну правильну відповідь
        else:
            # відповідь невірна, запишемо і відобразимо в статистиці
            self.result.setText(text_wrong) # напис "вірно" або "невірно"
            self.showed_answer.setText(self.frm_model.answer) # пишемо сам текст відповіді у відповідному віджеті
            self.frm_model.got_wrong() # оновити статистику, додавши невірну відповідь
            
class QuestionListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []
        
    def rowCount(self, index):
        return len(self.form_list)
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            # інтерфейс хоче намалювати цей рядок, дамо йому текст запитання для відображення
            form = self.form_list[index.row()]
            return form.question
        
    def insertRows(self, parent=QModelIndex()):
        position = len(self.form_list) 
        self.beginInsertRows(parent, position, position) 
        self.form_list.append(Question()) 
        self.endInsertRows() 
        QModelIndex()
        return True
    
    def removeRows(self, position, parent=QModelIndex()):
        ''' стандартний метод для видалення рядків - після видалення з моделі рядок автоматично видаляється з екрана '''
        self.beginRemoveRows(parent, position, position) 
        self.form_list.pop(position)
        self.endRemoveRows()
        return True
        
    def random_question(self):
        ''' Видає випадкове запитання '''
        total = len(self.form_list)
        current = randint(0, total - 1)
        return self.form_list[current]

def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card