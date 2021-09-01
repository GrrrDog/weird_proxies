FROM python:3
ADD myapp.py /
RUN pip install gunicorn
CMD [ "gunicorn", "-w 1", "--bind=0.0.0.0", "myapp:app" ]