import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from cv_website.settings import STATICFILES_DIRS
from cv_website_app.helper.read_yaml import read_yaml_from_file
from .models import Question, Answer

PAGE_NOT_FOUND = "'<h1>Page not found</h1>'"


# Create your views here.
def home_redirect(request):
    return redirect('home')


def home(request):
    yaml_folder = "yaml-data"
    file_name = "cv.yaml"
    template_file = "home.html"
    context = {}

    if request.method == 'GET':
        file_with_path = os.path.join(os.path.join(STATICFILES_DIRS[0], yaml_folder), file_name)
        data = read_yaml_from_file(file_with_path)
        if data:
            for item, document in data.items():
                context.update({item: document})
            return render(request, template_name=template_file, context=context)
        else:
            return HttpResponseNotFound(PAGE_NOT_FOUND)


def contact(request):
    template_file = "qanda-main.html"
    context = {}
    init = True

    if request.method == 'GET':
        questioner_email_address = request.GET.get('questioner-email')
        question_list = Question.objects.filter(questioner_email=questioner_email_address).order_by('-question_date')
        question_answer_list = []

        for question in question_list:
            try:
                answer = Answer.objects.get(related_question=question.id).answer
                question_answer_pair = {"question": question.content, "answer": answer}
            except:
                question_answer_pair = {"question": question.content, "answer": ""}

            question_answer_list.append(question_answer_pair)

        if questioner_email_address:
            init = False
        else:
            questioner_email_address = ""
        context = {"questioner_email_address": questioner_email_address, "init": init,
                   "question_answer_list": question_answer_list}

    elif request.method == 'POST':
        new_question_questioner_email = request.POST['questioner-email']
        new_question_content = request.POST['new-question']
        new_question = Question(content=new_question_content, questioner_email=new_question_questioner_email)
        new_question.save()
        # Redirect to current page after submit
        current_url = request.get_full_path()
        return HttpResponseRedirect(current_url)

    return render(request, template_name=template_file, context=context)