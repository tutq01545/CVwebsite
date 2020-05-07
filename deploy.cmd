@echo off
set /p Input=Enter your Heroku app name for deployment:
call heroku create %Input% --buildpack=heroku/python
if errorlevel 1 deploy 
call git checkout master
call heroku git:remote -a %Input%

:commit
set /p Input=Do you need to commit changes to Git(y/n)?
if /I "%Input%"=="y" goto y 
if /I "%Input%"=="n" goto n
echo Invalid input
goto commit

:y 
call git add . 
set /p Input=Enter your commit message:
call git commit -m "%Input%"

:n
call git push heroku master
if errorlevel 1 (
	pause
	goto n
) else (
	echo Deployment successful!
	pause
)

