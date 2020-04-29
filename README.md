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

