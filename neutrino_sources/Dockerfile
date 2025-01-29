ARG BASEIMAGE=icecube/icetray:icetray-devel-current-ubuntu22.04
FROM ${BASEIMAGE} as icetray_base

#Add some standard nu-sources tools
RUN mkdir /usr/local/icecube
WORKDIR /usr/local/icecube

# update setuptools and pip
RUN pip install --upgrade pip setuptools packaging

## Skyllh  v24_01_00
RUN curl -L https://github.com/icecube/skyllh/archive/refs/tags/v24.1.0.tar.gz | tar xz
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/icecube/skyllh-24.1.0"


## I3sklyllh v24_01_00
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/i3skyllh/archive/refs/tags/v24.1.0.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" | tar xz
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/icecube/i3skyllh-24.1.0"


RUN mkdir /root/src
WORKDIR /root/src

## Skylab v2.18
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/skylab/archive/refs/tags/v2.18.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" |tar xz &&\
  cd skylab-2.18 && pip3 install ./ 

## CSKY v1.1.14f
WORKDIR /root/src
RUN --mount=type=secret,id=GHTOKEN GHTOKEN=$(cat /run/secrets/GHTOKEN) && \
  curl  -L --url 'https://github.com/icecube/csky/archive/refs/tags/v1.1.14f.tar.gz' --header "Authorization: Bearer ${GHTOKEN}" | tar xz && \
  cd csky-1.1.14f && pip3 install pybind11 histlite && pip3 install ./

# provide the entry point
WORKDIR /root
CMD ["/bin/bash"]
