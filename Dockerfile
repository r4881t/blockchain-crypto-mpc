FROM alpine:3.13 AS mpc_builder

ENV JAVA_ALPINE_VERSION=8.275.01-r0

ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk

RUN apk add --no-cache make gcc g++ openssl libressl-dev openjdk8="$JAVA_ALPINE_VERSION" \
  python3 py3-pip python3-dev libffi-dev musl-dev cargo \
  curl

ENV COMMON_CPPFLAGS=-DOPENSSL_IS_BORINGSSL\ -D__ALPINE__

WORKDIR /build/

COPY . /build/

RUN make

FROM python:3.9.9-alpine3.13 as app_builder

RUN apk --update add --no-cache make gcc g++ openssl libressl-dev \
  python3 py3-pip python3-dev libffi-dev musl-dev openssl-dev \
  linux-headers build-base curl libssl1.1

WORKDIR /build/

ENV LD_LIBRARY_PATH=/build

COPY ./python/requirements.txt /build/python/requirements.txt

RUN pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install --upgrade wheel \
  && pip install -r ./python/requirements.txt

COPY --from=mpc_builder /build/libmpc_crypto.so /build/libmpc_crypto.so

COPY ./python /build/python/

ENV FLASK_APP=/build/python/app.py
RUN export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "8080" ]
