FROM python

WORKDIR /app

COPY . .

RUN pip3 install requests bs4 lxml

CMD ["python", "main.py"]