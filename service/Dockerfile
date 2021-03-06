FROM alpine:3.11

# Basics
RUN apk update
RUN apk upgrade
RUN apk add g++ gcc git libffi-dev make python3 python3-dev py3-pip cmake libpng-dev libssh2-dev openssl-dev

WORKDIR /opt/dependencies

# glkernel and dependencies

RUN git clone --depth 1 --branch 0.9.9.8 https://github.com/g-truc/glm.git
RUN git clone --depth 1 https://github.com/cginternals/cpplocate.git
RUN git clone --depth 1 https://github.com/cginternals/cppassist.git
RUN git clone --depth 1 https://github.com/cginternals/cppfs.git
RUN git clone --depth 1 https://github.com/cginternals/cppexpose.git
RUN git clone --depth 1 https://github.com/cginternals/glkernel.git

WORKDIR /opt/dependencies/glm

RUN cmake .

ENV CMAKE_PREFIX_PATH=/opt/dependencies/
ENV glm_DIR=/opt/dependencies/glm/cmake/

WORKDIR /opt/dependencies/cpplocate

RUN mkdir build
WORKDIR /opt/dependencies/cpplocate/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DOPTION_BUILD_TESTS=Off
RUN make

WORKDIR /opt/dependencies/cppassist

RUN mkdir build
WORKDIR /opt/dependencies/cppassist/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DOPTION_BUILD_TESTS=Off
RUN make

WORKDIR /opt/dependencies/cppfs

RUN mkdir build
WORKDIR /opt/dependencies/cppfs/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DOPTION_BUILD_TESTS=Off
RUN make

WORKDIR /opt/dependencies/cppexpose

RUN mkdir build
WORKDIR /opt/dependencies/cppexpose/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DOPTION_BUILD_TESTS=Off
RUN make

WORKDIR /opt/dependencies/glkernel

RUN mkdir build
WORKDIR /opt/dependencies/glkernel/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DOPTION_BUILD_TESTS=Off -DOPTION_BUILD_TOOLS=On
RUN make

WORKDIR /opt/glkernel-service

# Service

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# FastAPI, ASGI deployment
# RUN pip install fastapi uvicorn celery
# RUN pip install python-multipart aiofiles
# RUN pip3 freeze

# Deploy
# COPY bin bin
ADD . service

ENV USERNAME=glkernel-service
ENV GLKERNEL_DIRECTORY=/opt/dependencies/gklernel/build
ENV RESULT_DIR=/data/results

# CMD ["uvicorn", "--host=0.0.0.0", "main:app"]
CMD ["python3", "service/main.py"]
