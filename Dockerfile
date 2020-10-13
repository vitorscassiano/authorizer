# FROM python:3.7-buster
FROM python:3.8-alpine

WORKDIR /app

COPY authorizer /app/authorizer

CMD ["python3", "-m", "authorizer.app"]
