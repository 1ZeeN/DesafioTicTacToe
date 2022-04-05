FROM python:3.10.3-buster
COPY . .
RUN pip install -r requisitos.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
EXPOSE 80