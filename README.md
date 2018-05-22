# Lancer
for running this project on your computer follow these instructions:

first download the project and open terminal in the project folder then run the commands below in terminal

$ virtualenv venv --python=python3

$ source venv/bin/activate

$ pip3 install -r requirements.txt

$ python3 manage.py migrate

$ python3 manage.py createsuperuser

$ python3 manage.py runserver

then go to this url :
http://localhost:8000/blog/

Note: Only the super user can go to http://localhost:8000/admin

Note: after creating post in site, super user should confirm that post in http://localhost:8000/admin otherwise the post will not show in the site
