import os
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from cv_website.settings import STATIC_ROOT
from cv_website_app.helper.read_yaml import read_yaml_from_file

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
        file_with_path = os.path.join(os.path.join(STATIC_ROOT, yaml_folder), file_name)
        data = read_yaml_from_file(file_with_path)
        if data:
            for item, document in data.items():
                context.update({item: document})
            return render(request, template_name=template_file, context=context)
        else:
            return HttpResponseNotFound(PAGE_NOT_FOUND)

