% Prepare
release: sh -c 'cd NeedGo && python3 manage.py makemigrations && python3 manage.py migrate'

% Deploy
web: sh -c 'cd NeedGo && gunicorn NeedGo.wsgi --log-file -'

% Scheduler.
clock: python3 NeedGo/clock.py
