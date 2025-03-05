from enum import Enum


class QuizSubject(str, Enum):
    MAT_GRAMOTNOST = "Мат Грамотность"
    HISTORY_KZ = "История Казахстана"
    READING_LITERACY = "Грамотность Чтения"
    PHYSICS = "Физика"
    MATHEMATICS = "Математика"
    CHEMISTRY = "Химия"
    BIOLOGY = "Биология"
    GEOGRAPHY = "География" 
    WORD_HISTORY = 'ДЖТ'
    KAZAKH_LITERATURE='Каз Лит'
    RUSSIAN_LITERATURE='Рус Лит'
    ENGLISH='Английскии'


class QuizType(str, Enum):
    PHYSICS_MATH = "ФизМат"  # Физика + Математика
    GEO_MATH = "ГеоМат"      # География + Математика
    PHYSICS_CHEMISTRY = "ФизХим"  # Физика + Химия
    LANGUAGE_HISTORY = "ЯзыкИстория"  # Иностранный язык + История
    BIOLOGY_CHEMISTRY = "БиоХим"  # Биология + Химия
    MATH_INFORMATICS = "МатИнф"  # Математика + Информатика


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"