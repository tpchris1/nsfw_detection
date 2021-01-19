FROM python:3.6-stretch

ARG CONTAINER_WORKDIR
# ENV ENV_CONTAINER_WORKDIR=$CONTAINER_WORKDIR
WORKDIR $CONTAINER_WORKDIR
RUN echo $CONTAINER_WORKDIR

ARG CONTAINER_INDEX
RUN echo $CONTAINER_INDEX > container_index.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Check current installed python packages
RUN pip list

COPY . .

# show all file in the current folder
RUN ls -al

RUN python manage.py collectstatic --noinput
# CMD [ "python", "manage.py", "collectstatic", "--noinput"]

# CMD [ "python", "manage.py", "shell", "-c", "\"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('batalk', 'batalk@batalk.fun', 'batalk')\""]
# CMD python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'batalk\', \'batalk@batalk.fun\', \'batalk\')"

RUN python manage.py makemigrations
RUN python manage.py migrate
# CMD [ "python", "manage.py", "makemigrations"]
# CMD [ "python", "manage.py", "migrate"]

RUN python create_admin.py
# CMD [ "python", "create_admin.py"]

CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
# CMD [ "uwsgi", "--http", ":8000", "--module", "NSFW_detect.wsgi", "--enable-threads"]
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]