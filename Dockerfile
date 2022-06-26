FROM alpine:3.13 AS mpc_builder

WORKDIR /build/
COPY . /build/

ENV JAVA_ALPINE_VERSION=8.275.01-r0

ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk

RUN apk add --no-cache make gcc g++ openssl libressl-dev openjdk8="$JAVA_ALPINE_VERSION" \
  python3 py3-pip python3-dev libffi-dev musl-dev cargo \
  curl

ENV COMMON_CPPFLAGS=-DOPENSSL_IS_BORINGSSL\ -D__ALPINE__

RUN make

RUN apk add --no-cache openssl-dev

ENV LD_LIBRARY_PATH=/build/

RUN pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install --upgrade wheel \
  && pip install -r ./python/requirements.txt

ENV FLASK_APP=/build/python/app.py

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "8080" ]
