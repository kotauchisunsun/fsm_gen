FROM python:3.6.9
COPY ./ /work/
WORKDIR work
RUN pip install pipenv
RUN pip install -r requirements.txt
CMD ["streamlit","run","web.py","--server.enableCORS","--server.port","8502"]