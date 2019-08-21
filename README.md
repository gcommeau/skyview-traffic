To run locally:
```
# Loading setting for local development
cp settings.py.local settings.py
# Building the database
python manage.py migrate
# Loading play data
python manage.py loaddata traffic
# Starting the Django server
python manage.py runserver
```

To deploy in AWS:
```
# Loading setting for production deployment
# Note that of course settings.py.remote is not checked in git
cp settings.py.remote settings.py
# Handling static Files
python manage.py collectstatic
# Elastic Beanstalk deploy (this may take a while)
eb deploy
```
