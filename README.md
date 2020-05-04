# CVwebsite
Code base to create simple website(s) for Developer, with CV section and QA section. <br>
We use Django 2.2, Bootstrap 4.4.1, Gettext 0.17.1 and Heroku
# Install package
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>

# Setup for Multiple language development
## 1. Install gettext 
- Download and install gettext-tools and gettext-runtime (version 0.17.1 windows-34 bit, version 0.18 has bug)
  Both of them should be saved under C:\<Your Path>\gettext-utils
- Set C:\<Your Path>\gettext-utils\bin to Path in environment variable (Windows)
- Link of documentation: https://www.gnu.org/software/gettext/manual/gettext.html
## 2. Set up settings.py
- define LANGUAGES
- define LANGUAGE_CODE
- set USE_I18N to True to support localization
- set USE_L10N to True to support format dates, numbers and calendars
- set USE_TZ to True
- set LOCALE_PATHS to (os.path.join(BASE_DIR, 'locale'))
- Link of documentation: https://docs.djangoproject.com/en/2.2/topics/i18n/
## 3. Add {% trans "[TEXT_THAT_YOU_WANT_TO_TRANSLATE]"%} in template
## 4. Generate .po file for selected language
- Command: django-admin.py makemessages -l [LANGUAGE_ISO_CODE]
- A .po file will be generated and saved into your defined LOCAL_PATH above
- For each text you added {% trans %} in template above, one msgstr will be generated. At this point, value of msgstr is ""
## 5. Add translated text into .po
- Now you will need to fill the msgstr values in .po, manually.
## 6. Compile .po file to .mo file
- Command: django-admin.py compilemessages
- A .mo file will be generated and saved into the same place as .po's one.
## 7. Don't forget to activate the language when you switch the language in form
- translation.activate([LANGUAGE_ISO_CODE]) where translation is imported from django.utils
## Note
- If you want to update the translation, don't forget to re-generate .po file (step 4), add translated text (step 5) and generate .mo file (step 6)

# Deploy server on Heroku
## 1. Install Heroku CLI
- Download and install the Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
- Add absolute path to Heroku CLI to environment variable Path
## 2. Required data for Heroku deployment
- Procfile
- requirements.txt
- runtime.txt
These files should be located in the project root folder
## 3. Setup Procfile
- For this Django project, Profile is already setup
- The Profile should contain for this app the following: web: gunicorn cv_website.wsgi
- For other Django projects, it should contain: web: gunicorn [DJANGO_PROJECT_NAME].wsgi
## 4. Setup requirements.txt
- For this Django project, requirements.txt is already setup
- requirements.txt should contain all required dependencies which need to be installed for the app to run
- Result from pip freeze in the virtualenv can be used as requirements.txt
## 5. Setup runtime.txt
- For this Django project, runtime.txt is already setup
- It should specify the version of python used at runtime
## 6. Create Heroku app from project root folder
- From command line, navigate to the project root folder (in this app it is [PATH]\CVWebsite\Project\cv_website\, where <PATH> is the path where the git local repository is stored
- Login to heroku with command: heroku login -i
- Create app with command: heroku create [HEROKU_APP_NAME] --buildpack=heroku/python
- After finisih creating the Heroku app, you can type git remote. heroku should show up as 1 of your git remotes
## 7. Add and push git repository to heroku remote
- Command: git add .
- Command: git commit -m "[MESSAGE]"
- Command: git push heroku master
## 8. Open app from Heroku's website
- Go to app on Heroku and choose Open app 