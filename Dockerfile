FROM continuumio/anaconda3:2019.03

RUN apt-get -y update && apt-get -y install vim
RUN pip install --upgrade pip && pip install autopep8
RUN apt install unzip
ARG project_dir=/projects
WORKDIR $project_dir
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md
RUN pip install scispacy
COPY . $project_dir
CMD ["/bin/bash"]