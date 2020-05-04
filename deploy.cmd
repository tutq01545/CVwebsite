call heroku login -i
if errorlevel 1 exit /B
call heroku create [HEROKU_APP_NAME] --buildpack=heroku/python
if errorlevel 1 exit /B
call heroku git:remote -a [HEROKU_APP_NAME]
if errorlevel 1 exit /B
call git add .
if errorlevel 1 exit /B
call git commit -m "[MESSAGE]"
if errorlevel 1 exit /B
call git push heroku master
if errorlevel 1 exit /B
