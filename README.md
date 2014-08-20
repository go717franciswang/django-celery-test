### Dependencies
```
sudo pip install django-celery
sudo pip install django-jquery
sudo pip install django-jquery-ui
sudo apt-get install rabbitmq-server
```

### Run
```
# start test server
python manage.py runserver 0.0.0.0:8000

# start django-celery
python manage.py celery worker
