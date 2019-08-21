# phonebook


install requirements
--------------------

> pip install -r requirement.txt


createsuperuser
-----------------

> python manage.py createsuperuser


Authentication
---------
> You have to add your own client id and secret in settings.py for google and linked in authentication.



Migrations
----------
You need to migrate code after create or modify existing or new models
> python manage.py makemigrations

> python manage.py migrate

runserver
---------
> python manage.py runserver

> after login goto localhost:8000 for default admin interface
