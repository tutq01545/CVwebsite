import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cv_website.settings import STATICFILES_DIRS
from cv_website_app.helper.read_yaml import read_yaml_from_file
from cv_website_app.static.language_code import LANGUAGES
from django.utils import translation
from .models import Question, Answer
from operator import itemgetter
from django.contrib.auth import authenticate, login, logout
from cv_website_app.helper.update_url import add_parameter_to_url


STATIC_ROOT = STATICFILES_DIRS[0]
PAGE_NOT_FOUND = translation.ugettext("'<h1>Page not found</h1>'")
DEFAULT_LANGUAGE = "en"
YAML_FOLDER = "yaml-data"


# Create your views here.
def home_redirect(request):
    return redirect('home')


def home(request):
    global DEFAULT_LANGUAGE
    template_file = "home.html"
    context = {"language": DEFAULT_LANGUAGE}

    if request.method == 'GET':
        language = request.GET.get("language")
        if language:
            language_iso_code = [code for code in LANGUAGES if code[1] == language][0][0]
            DEFAULT_LANGUAGE = language_iso_code
        file_name = "cv-{}.yaml".format(DEFAULT_LANGUAGE)
        context.update({"language": DEFAULT_LANGUAGE})
        translation.activate(DEFAULT_LANGUAGE)
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
    elif request.method == 'POST':
        has_username = request.POST.get('username', False)
        if not has_username:
            current_url = request.get_full_path()
            return HttpResponseRedirect(current_url)
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                params = {"loginState": 1}
            else:
                params = {"loginState": 0}

            current_url = request.get_full_path()
            new_url = add_parameter_to_url(url=current_url, params=params)
            return HttpResponseRedirect(new_url)


def contact(request):
    global DEFAULT_LANGUAGE
    template_file = "qanda-main.html"
    context = {"language": DEFAULT_LANGUAGE}
    init = True

    if request.method == 'GET':
        language = request.GET.get("language")
        if language:
            language_iso_code = [code for code in LANGUAGES if code[1] == language][0][0]
            DEFAULT_LANGUAGE = language_iso_code
        file_name = "cv-{}.yaml".format(DEFAULT_LANGUAGE)
        context.update({"language": DEFAULT_LANGUAGE})
        translation.activate(DEFAULT_LANGUAGE)
        file_with_path = os.path.join(os.path.join(STATIC_ROOT, YAML_FOLDER), file_name)
        data = read_yaml_from_file(file_with_path)
        if data:
            context.update({'developer': data['developer']})

        questioner_email_address = request.GET.get('questioner-email')
        is_get_all_question = request.GET.get("get_all_questions")
        is_get_statistics = request.GET.get("get_statistics")
        if questioner_email_address:
            from cv_website_app.helper.view_helper import get_question_answer_list
            init = False
            question_answer_list = get_question_answer_list(email_address=questioner_email_address)

            context.update({"questioner_email_address": questioner_email_address, "init": init,
                            "question_answer_list": question_answer_list,
                            "numberOfQuestions": len(question_answer_list),
                            "message": ""})
        elif is_get_all_question:
            from cv_website_app.helper.view_helper import get_all_questions_list

            all_questions_list = get_all_questions_list()

            context.update({"allQuestions": all_questions_list,
                            "numberOfQuestions": len(all_questions_list),
                            })
            #TODO

        elif is_get_statistics:
            from cv_website_app.helper.view_helper import get_statistics

            statistics = get_statistics() ##TODO
        else:
            context.update({"init": init})

    elif request.method == 'POST':
        has_username = request.POST.get('username', False)
        has_questioner_email = request.POST.get('questioner-email', False)
        has_new_question = request.POST.get('new-question', False)
        if has_new_question and has_questioner_email:
            new_question_questioner_email = request.POST['questioner-email']
            new_question_content = request.POST['new-question']
            new_question = Question(content=new_question_content, questioner_email=new_question_questioner_email)
            new_question.save()
            # Redirect to current page after submit
            current_url = request.get_full_path()
            return HttpResponseRedirect(current_url)
        else:
            if not has_username:
                current_url = request.get_full_path()
                return HttpResponseRedirect(current_url)
            else:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    params = {"loginState": 1}
                else:
                    params = {"loginState": 0}

                current_url = request.get_full_path()
                new_url = add_parameter_to_url(url=current_url, params=params)
                return HttpResponseRedirect(new_url)

    return render(request, template_name=template_file, context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
