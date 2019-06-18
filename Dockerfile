# start from an official image
FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app/

RUN pip config --global set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org"
RUN pip install pip --upgrade
RUN pip install -r requirements.txt

# define the default command to run when starting the container
EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
