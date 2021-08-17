FROM diva-rest-base:latest

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

# cannot install connexion into Python 2...
## for version 2
#RUN pip install -r requirements.txt

# for version 3.7
RUN python3.7 -m pip install -r requirements.txt

# CMD [ "python3.7", "src/server.py" ]
# use connexion CLI instead. to add other options for validation, etc.
CMD [ "connexion", "run", "-p", "8080", "--mock=notimplemented", "--debug", "spec/swagger.yaml" ]
