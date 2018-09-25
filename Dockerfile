FROM continuumio/miniconda3

# docker build -t openschemas/openschemas .
# docker run -v $PWD:/data openschemas/openschemas

# This should build (and push) from master on merge into it

RUN apt-get update && apt-get install -y git wget
RUN mkdir -p /data /code
ADD . /code
WORKDIR /code
RUN python setup.py install
ENTRYPOINT ["/opt/conda/bin/openschemas"]
