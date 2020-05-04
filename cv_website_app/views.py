import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from cv_website.settings import STATICFILES_DIRS
from cv_website_app.helper.read_yaml import read_yaml_from_file
from cv_website_app.static.language_code import LANGUAGES
from django.utils import translation
from .models import Question, Answer

STATIC_ROOT = STATICFILES_DIRS[0]
PAGE_NOT_FOUND = translation.ugettext("'<h1>Page not found</h1>'")
DEFAULT_LANGUAGE = "en"
YAML_FOLDER = "yaml-data"


# Create your views here.
def home_redirect(request):
    return redirect('home')


def home(request):
    file_name = "cv-en.yaml"
    template_file = "home.html"
    context = {"language": DEFAULT_LANGUAGE}

    if request.method == 'GET':
        language = request.GET.get("language")
        if language:
            language_iso_code = [code for code in LANGUAGES if code[1] == language][0][0]
            file_name = "cv-{}.yaml".format(language_iso_code)
            context.update({"language": language_iso_code})
            translation.activate(language_iso_code)
        file_with_path = os.path.join(os.path.join(STATIC_ROOT, YAML_FOLDER), file_name)
        data = read_yaml_from_file(file_with_path)
        if data:
            for item, document in data.items():
                if item == "work_experience" or item == "education":
                    temp_document = sorted(document, key= lambda i: i["id"], reverse=True)
                    context.update({item: temp_document})
                else:
                    context.update({item: document})
            return render(request, template_name=template_file, context=context)
        else:
            return HttpResponseNotFound(PAGE_NOT_FOUND)


def contact(request):
    file_name = "cv-en.yaml"
    template_file = "qanda-main.html"
    context = {"language": DEFAULT_LANGUAGE}
    init = True

    if request.method == 'GET':
        language = request.GET.get("language")
        if language:
            language_iso_code = [code for code in LANGUAGES if code[1] == language][0][0]
            file_name = "cv-{}.yaml".format(language_iso_code)
            context.update({"language": language_iso_code})
            translation.activate(language_iso_code)
        file_with_path = os.path.join(os.path.join(STATIC_ROOT, YAML_FOLDER), file_name)
        data = read_yaml_from_file(file_with_path)
        if data:
            context.update({'developer': data['developer']})
        questioner_email_address = request.GET.get('questioner-email')
        question_list = Question.objects.filter(questioner_email=questioner_email_address).order_by('-question_date')
        question_answer_list = []

        if question_answer_list:
            for question in question_list:
                try:
                    answer = Answer.objects.get(related_question=question.id).answer
                    print(answer)
                    question_answer_pair = {"question": question.content, "answer": answer}
                except Exception as e:
                    print("Exception: ", e)
                    question_answer_pair = {"question": question.content, "answer": ""}

                question_answer_list.append(question_answer_pair)

        if questioner_email_address:
            init = False
        else:
            questioner_email_address = ""

        context.update({"questioner_email_address": questioner_email_address, "init": init,
                        "question_answer_list": question_answer_list})

    elif request.method == 'POST':
        new_question_questioner_email = request.POST['questioner-email']
        new_question_content = request.POST['new-question']
        new_question = Question(content=new_question_content, questioner_email=new_question_questioner_email)
        new_question.save()
        # Redirect to current page after submit
        current_url = request.get_full_path()
        return HttpResponseRedirect(current_url)

    return render(request, template_name=template_file, context=context)
