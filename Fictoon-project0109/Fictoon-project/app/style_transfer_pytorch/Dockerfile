FROM python:3.6


COPY .. /app
WORKDIR /app/style_transfer_pytorch
RUN pip3 install -r requirements.txt
RUN pip install gunicorn


RUN pip install Pillow

RUN adduser --disabled-password --gecos '' app
EXPOSE 5005

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5005", "wsgi"]