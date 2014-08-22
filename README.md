### Dependencies
```
sudo pip install django-celery
sudo pip install django-jquery
sudo pip install django-bootstrap3
sudo apt-get install rabbitmq-server
```

### Config
```
# add a virtual environment in Rabbit
sudo rabbitmqctl add_vhost dev

# grant guest permission to this env
sudo rabbitmqctl set_permissions -p dev guest '.*' '.*' '.*'
```

### Run
```
# start test server
python manage.py runserver 0.0.0.0:8000

# start django-celery
python manage.py celery worker
```

