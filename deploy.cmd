call heroku login -i
if errorlevel 1 exit /B
call heroku create cv-web-app-tu --buildpack=heroku/python
if errorlevel 1 exit /B
call heroku git:remote -a cv-web-app-tu
if errorlevel 1 exit /B
call git add .
if errorlevel 1 exit /B
call git commit -m "[MESSAGE]"
if errorlevel 1 exit /B
call git push heroku master
if errorlevel 1 exit /B
