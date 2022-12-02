
FROM python:latest
COPY main.py /
RUN yarn install --production
CMD [ "python", "./main.py" ]
