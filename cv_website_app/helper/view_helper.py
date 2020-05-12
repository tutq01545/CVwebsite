from cv_website_app.models import Question, Answer
from operator import itemgetter


def get_question_answer_list(email_address: str) -> list:
    question_list = Question.objects.filter(questioner_email=email_address).order_by('-question_date')
    question_answer_list = []

    for question in question_list:
        try:
            answers = Answer.objects.filter(related_question=question.id)
            question_answer_pair = {"id": question.id,
                                    "question": question.content,
                                    "questionDate": question.question_date,
                                    "numberOfAnswers": len(answers),
                                    "answers": answers}
        except Exception as e:
            print("Exception while querying answers: ", e)
            question_answer_pair = {"id": question.id, "question": question.content, "answer": ""}

        question_answer_list.append(question_answer_pair)

    question_answer_list = sorted(question_answer_list, key=itemgetter('id'))
    return question_answer_list


def get_all_questions_list() -> list:
    questions_set = Question.objects.all().order_by('-question_date')
    questions_list = []

    for question in questions_set:
        relevant_answers = Answer.objects.filter(related_question=question).order_by('answer_date')
        questions_list.append({
            "id": question.id,
            "question": question.content,
            "questionDate": question.question_date,
            "questioner": question.questioner_email,
            "answers": [{"answerID": answer.id,
                         "answerContent": answer.answer, "answerDate": answer.answer_date}
                        for answer in relevant_answers]
        })
    return questions_list


def get_statistics() -> dict:
    total_number_of_questions = Question.objects.count()
    total_number_of_questioner = Question.objects.values('questioner_email').distinct().count()
    number_of_questions_with_answer = 0
    number_of_questions_without_answer = 0
    all_questions = Question.objects.all()

    for question in all_questions:
        try:
            relevant_answer = Answer.objects.get(related_question=question.id)
        except Answer.DoesNotExist:
            relevant_answer = None
        except Answer.MultipleObjectsReturned:
            relevant_answer = 1
        if relevant_answer is not None:
            number_of_questions_with_answer += 1
        else:
            number_of_questions_without_answer += 1

    return {
        'numberOfQuestion': total_number_of_questions,
        'numberOfQuestioner': total_number_of_questioner,
        'numberOfQuestionWithAnswer': number_of_questions_with_answer,
        'numberOfQuestionWithoutAnswer': number_of_questions_without_answer
    }
