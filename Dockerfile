FROM python:3

WORKDIR /kt_bot

COPY requirements.txt /kt_bot

EXPOSE 80

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "bot.py" ]