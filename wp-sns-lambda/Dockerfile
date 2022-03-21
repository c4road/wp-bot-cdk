FROM public.ecr.aws/lambda/python:3.6

COPY ["*.py", "requirements.txt", "/var/task/"]
COPY ["utils", "/var/task/utils"]

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "app.handler" ]
