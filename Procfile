release: python manage.py makemigrations && python manage.py migrate
web: daphne taskmanagement.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker channel_layer -v2