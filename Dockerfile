FROM alpine:3.13

WORKDIR /build/
COPY . /build/

ENV JAVA_ALPINE_VERSION=8.275.01-r0

ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk

RUN apk add --no-cache make gcc g++ openssl libressl-dev openjdk8="$JAVA_ALPINE_VERSION"

ENV COMMON_CPPFLAGS=-DOPENSSL_IS_BORINGSSL\ -D__ALPINE__

RUN make

ENV LD_LIBRARY_PATH=.
