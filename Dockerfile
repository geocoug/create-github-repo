FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV PYTHON_VENV=/opt/pyenv

RUN python -m venv $PYTHON_VENV 

ENV PATH="$PYTHON_VENV/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY create_repo.py .

CMD [ "python", "create_repo.py" ]