# -- Import for running main()
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_website.settings')
application = get_wsgi_application()

# -- Write code --
import yaml
from cv_website_app.helper.read_yaml import read_yaml_from_file
from cv_website_app.helper.translator import translate
from cv_website.settings import STATIC_ROOT

yaml_folder = os.path.join(STATIC_ROOT, 'yaml-data')
yaml_en_file = os.path.join(yaml_folder, 'cv-en.yaml')


def translate_yaml(language_code:str):
    data = read_yaml_from_file(yaml_en_file)
    for item, document in data.items():
        if item == "education" or item == "work_experience":
            for doc in document:
                for key, value in doc.items():
                    if isinstance(value, str):
                        translated_text = ""
                        if "\n" in value:
                            phrases = value.split("\n")
                            for index, phrase in enumerate(phrases):
                                if index != len(phrases) - 1:
                                    postfix = "\n"
                                else:
                                    postfix = ""
                                translated_text += translate(language_code, phrase) + postfix
                        else:
                            translated_text = translate(language_code, value)
                        doc[key] = translated_text
            pass
        elif item == "summary" or item == "hobby":
            if isinstance(document, str):
                data[item] = translate(language_code, document)

    yaml_new_file = os.path.join(yaml_folder, 'cv-{}.yaml'.format(language_code))
    with open(yaml_new_file, 'w') as file:
        yaml.dump(data, file)


if __name__ == '__main__':
    translate_yaml("de")
