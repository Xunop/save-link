FROM python:3.11

WORKDIR /bot

COPY . /bot

RUN mv /bot/config-example.py /bot/config.py
RUN cd /bot && pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
