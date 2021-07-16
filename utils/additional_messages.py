import nltk

from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nltk.download("stopwords")

russian_stemmer = SnowballStemmer("russian")
russian_stopwords = stopwords.words("russian")

QUESTIONS_AND_ANSWERS = OrderedDict([
    (
        "Дата собеседования с деканом, Когда будет собеседование с деканом", 
        
        "Дата собеседования с деканом абитуриентов поступивших на бюджет 1-2 "
        "августа, на платное 17 августа."
    ),
    (
        "Личный кабинет, зачем заводить личный кабинет",
        
        "Мы рекомендуем Вам зарегистрировать личный кабинет, так как после "
        "этого вы сможете увидеть свой рейтинг в списке с точностью до одно "
        "человека. В общедоступном виде на сайте БГУ точность отображения "
        "находится в диапазоне 10-ти баллов"
    ),
    (
        "Время обновления о поданных документах, время обновления информации "
        "о поданных документах",
        
        "В дни приемной кампании (как на платное, так и на бюджет) на сайте "
        "БГУ обновление информации о поданных документах происходит в 15:00, "
        "18:00. Но может и чаще. В последний день подачи документов (на "
        "бюджет и на платное), сайт БГУ в последний раз обновляется в 15:00. "
        "После этого с 15:00 до 17:00 необходимо следить за подачей "
        "непосредственно возле приемной комиссии"
    ),
    (
        "Время приёма документов на факультет",
        
        "Время работы приемной комиссии с 9:00 до 18:00, обед с 13:00 до 14:00"
    ),
    (
        "Адрес общежития",
        
        "г. Минск, ул. Курчатова 8"
    ),
    (
        "Льготы на общежитие",
        
        "Подробности о льготах на общежитие можно узнать по ссылке на нашем "
        "сайте: https://rfe.bsu.by/novosti-abiturientam/~showNews/internat-"
        "lgota-zayavlenie"
    ),
    (
        "Нужно ли родителям присутствовать на собеседовании",
        
        "На собеседовании абитуриент с паспортом должен присутствовать "
        "обязательно, либо лицо, нотариально удостоверенное представлять "
        "абитуриента. Если ребенку нет 18-ти лет, должен присутствовать один "
        "из родителей ребенка. На платное обучение должен присутствовать "
        "абитуриент и тот кто будет оплачивать его обучение, так как тот "
        "кто платит, имеет льготы по налогооблажению"
    ),
    (
        "Могут ли российские/казахские/киргизские/украинские/узбекские "
        "абитуриенты поступить на факультет",
        
        "Да, могут при наличии сертификатов белорусского ЦТ"
    ),
    (
        "Где можно узнать о специальностях, какие есть специалоьности",
        
        "Подробней о специальностях вы можете узнать у нас на сайте : "
        "https://rfe.bsu.by/info/spec"
    ),
    (
        "Результаты приёмной кампании, когда можно будет узнать результаты",
        
        "Узнать прошли вы или нет можно будет на собеседовании с деканом"
    ),
    (
        "Как определяется проходной балл на факультет",
        
        "Проходной балл определяется исходя из цифр приема за исключением "
        "количества абитуриентов поступающих без экзамена и вне конкурса, "
        "т.е. пример: план набора на РФиКТ 205 человек, на факультет подало "
        "7 абитуриентов без экзаменов и 1 вне конкурса. Таким образом 205 - "
        "7 - 1 = 197, т. е. ваш общий рейтинг должен быть не ниже 197 места"
    ),
    (
        "Как сильно меняется проходной балл, сколько абитуриентов подают "
        "заявки",
        
        "В последний день после 15:00 проходной балл может подняться на 10-20 "
        "баллов, но в некоторые года было такое, что может и опуститься на "
        "10 баллов. Год на год не приходится, необходимо следить на месте."
    ),
    (
        "Перечень дисциплин, изучаемые предметы",
        
        "Перечень курсов, читаемых для всех специальностей можно посмотреть "
        "на нашем сайте: https://rfe.bsu.by/stud/discipliny"
    ),
    (
        "Кафедры факультета",
        
        "Подробней ознакомится с кафедрами для всех специальностей можно на "
        "сайте : https://rfe.bsu.by/info/kafedry/rad-f"
    ),
])

NO_ANSWER_MESSAGE = "К сожалению, ответа на Ваш вопрос нет. Обратитесь на " \
                    "сайт: https://rfe.bsu.by/."
QUESTIONS_MESSAGE = "Возможно, Вы сможете получить ответ здесь:"


def _multi_split(s, *keys):
    l = s.split()
    for k in keys:
        l = [i for j in l for i in j.split(k)]
    return l


def _get_stemmed_string(string):
    return [
            russian_stemmer.stem(word)
            for word in _multi_split(string, '/')
            if word.lower() not in russian_stopwords
        ]


def _get_template_with_processed_questions():
    stemmed_questions = {}

    for question in QUESTIONS_AND_ANSWERS.keys():
        stemmed_question = _get_stemmed_string(question)

        stemmed_questions[question] = stemmed_question

    return stemmed_questions


def find_matching_themes(user_question):
    matching_count = {question: 0 for question in QUESTIONS_AND_ANSWERS.keys()}
    stemmed_user_question = _get_stemmed_string(user_question)

    stemmed_questions = _get_template_with_processed_questions()

    for stemmed_user_word in stemmed_user_question:
        for question, stemmed_question in stemmed_questions.items():
            if stemmed_user_word in stemmed_question:
                matching_count[question] += 1

    sorted_values = sorted(matching_count.values(), reverse=True)
    matching_questions = []

    for value in sorted_values:
        if value == 0:
            continue

        for key in matching_count.keys():
            if len(matching_questions) == 5:
                break
            if key not in matching_questions and matching_count[key] == value:
                matching_questions.append(key)

    return matching_questions
