FROM python:3.8.2
RUN mkdir /script
RUN pip install hvac
RUN pip install kubernetes
ENTRYPOINT [ "python" ]
