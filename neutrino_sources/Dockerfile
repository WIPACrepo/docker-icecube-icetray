ARG BASEIMAGE=icecube/icetray:icetray-prod-current-ubuntu22.04-X64
FROM ${BASEIMAGE} as icetray_base

MAINTAINER IceCube <developers@icecube.wisc.edu>

#Add some standard nu-sources tools
RUN mkdir /usr/local/icecube
WORKDIR /usr/local/icecube

## Skyllh  v22_04_28a
RUN curl -L https://github.com/icecube/skyllh/archive/refs/tags/v22_04_28a.tar.gz | tar xz
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/icecube/skyllh-22_04_28a"

## I3sklyllh v22_04_28
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/i3skyllh/archive/refs/tags/v22_04_28.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" | tar xz
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/icecube/i3skyllh-22_04_28"

RUN mkdir /root/src
WORKDIR /root/src

## Skylab v2.17
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/skylab/archive/refs/tags/v2.17.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" |tar xz &&\
  cd skylab-2.17 && pip3 install ./ 

## CSKY v1.1.14b
WORKDIR /root/src
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/csky/archive/refs/tags/v1.1.14b.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" | tar xz && \
  cd csky-1.1.14b && pip3 install pybind11 histlite && pip3 install ./

# provide the entry point
WORKDIR /root
CMD ["/bin/bash"]
