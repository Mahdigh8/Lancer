# Lancer
for running this project on your computer follow these instructions:
first download the project and open terminal in the project folder then run the commands below in terminal
\n
$ virtualenv venv --python=python3\n
$ source venv/bin/activate\n
$ pip3 install -r requirements.txt\n
$ python3 manage.py migrate\n
$ python3 manage.py createsuperuser\n
$ python3 manage.py runserver\n
\n
then go to this url :
http://localhost:8000/blog/
\n
Note: Only the super user can go to http://localhost:8000/admin\n
Note: after creating post in site, super user should confirm that post otherwise the post will not show in the site
