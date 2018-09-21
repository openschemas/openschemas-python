FROM continuumio/miniconda3

#########################################
# The Robot Namer
# 
# docker build -t vanessa/openschemas-namer .
# docker run vanessa/openschemas-namer
#########################################

LABEL maintainer vsochat@stanford.edu
ADD generate.py /
ENV PATH /usr/local/bin:$PATH
ENTRYPOINT ["python", "/generate.py"]
