# Lancer
For running this project on your computer follow these instructions:

1.First download the project and open terminal in the project folder.

2.Run the commands below in terminal:

   $ virtualenv venv --python=python3

   $ source venv/bin/activate

   $ pip3 install -r requirements.txt

   $ python3 manage.py migrate

   $ python3 manage.py createsuperuser

   $ python3 manage.py runserver

3.Go to this url :
http://localhost:8000/blog/

Note: Admin page url is  http://localhost:8000/admin and only super user can login to this page.

Note: After creating post by employers, super user should confirm that post in admin page otherwise the post will not show in the site.
