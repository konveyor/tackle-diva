FROM diva:latest

RUN apt-get update \
    && apt-get install -y \
    python3.7 python3-pip curl \
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# RUN git clone https://github.com/pyenv/pyenv.git .pyenv
# ENV HOME /root
# ENV PYENV_ROOT /app/.pyenv
# ENV PATH ${PYENV_ROOT}/bin:${PATH}
# RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# RUN eval "$(pyenv init -)"
# RUN pyenv install 3.9.6 && pyenv local 3.9.6

COPY requirements.txt .
COPY src src
COPY spec spec
COPY dist dist
COPY .env.docker .env

RUN python3 -m pip install -r requirements.txt --no-deps
RUN python3 -m pip install dist/diva_server-1.0.0-py3-none-any.whl

# cannot install connexion into Python 2...
## for version 2
#RUN pip install -r requirements.txt

# for version 3.7
## RUN python3.7 -m pip install -r requirements.txt

# CMD [ "python3.7", "src/server.py" ]
# use connexion CLI instead. to add other options for validation, etc.
CMD [ "python3", "-m", "diva_server" ]
