import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from cv_website.settings import STATIC_ROOT
from cv_website_app.helper.read_yaml import read_yaml_from_file
from cv_website_app.static.language_code import LANGUAGES
from django.utils import translation


PAGE_NOT_FOUND = translation.ugettext("'<h1>Page not found</h1>'")
DEFAULT_LANGUAGE = "en"


# Create your views here.
def home_redirect(request):
    return redirect('home')


def home(request):
    yaml_folder = "yaml-data"
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
        file_with_path = os.path.join(os.path.join(STATIC_ROOT, yaml_folder), file_name)
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
    template_file = "contact.html"
    context = {}

    return render(request, template_name=template_file, context=context)
