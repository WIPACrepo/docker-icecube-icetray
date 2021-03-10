##### first, install a base Ubuntu system (with development packages)

FROM ubuntu:20.04 as base

FROM base as install

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd-dev \
  libxml2-dev subversion git libboost-python1.71-dev \
  libboost-system1.71-dev libboost-thread1.71-dev libboost-numpy1.71-dev \
  libboost-date-time1.71-dev libboost-serialization1.71-dev \
  libboost-filesystem1.71-dev libboost-program-options1.71-dev \
  libboost-regex1.71-dev libboost-iostreams1.71-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python3-scipy \
  python3-urwid python3-numpy python3-matplotlib \
  python3-numexpr cython3 python3-cffi python3-requests \
  python3-healpy python3-urllib3 python3-jsonschema \
  python3-zmq python3-pymysql python3-dev python3-pip \
  zlib1g-dev liberfa-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev libfftw3-dev \
  libcfitsio-dev libhdf5-dev libhealpix-cxx-dev \
  opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 \
  nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/master.tar.gz && \
    tar -zxf master.tar.gz && cd cppzmq-master && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make install

######################## BASE SYSTEM DONE ########################
#### install icetray
##################################################################

# set up test data directory
RUN mkdir /opt/i3-data
ENV I3_DATA /opt/i3-data
RUN mkdir /opt/i3-data/i3-test-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data

# check out icetray
RUN mkdir /root/combo && mkdir /root/combo/build
COPY icetray /root/combo/src

# build icetray
WORKDIR /root/combo/build
RUN cmake /root/combo/src \
      -DCMAKE_BUILD_TYPE=Release \
      -DINSTALL_TOOL_LIBS=OFF \
      -DUSE_GFILT=OFF \
      -DCMAKE_INSTALL_PREFIX=/usr/local/icetray \
      -DUSE_PYTHON3=OFF \
    && make -j4

# install icetray
RUN make install

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/root/combo/build/env-shell.sh", "exec"]
CMD ["/bin/bash"]

# create an icecube user
#RUN adduser icecube --disabled-password
#USER icecube
#WORKDIR /home/icecube


##################################################################
#### Now install the slim system, copying icetray from the base.
##################################################################

FROM base as slim

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 zlib1g libzstd1 less \
  libboost-python1.71.0-py38 libboost-system1.71.0 libboost-thread1.71.0 \
  libboost-date-time1.71.0 libboost-serialization1.71.0 \
  libboost-filesystem1.71.0 libboost-program-options1.71.0 \
  libboost-regex1.71.0 libboost-iostreams1.71.0 libgsl23 \
  libcdk5nc6 libarchive13 python3 python3-scipy \
  python3-urwid python3-numpy python3-matplotlib \
  python3-numexpr cython3 python3-cffi python3-requests \
  python3-healpy python3-urllib3 python3-jsonschema \
  libzmq5 libzmqpp4 python3-zmq python3-pymysql \
  zlib1g-dev liberfa1 libstarlink-pal0 \
  libopenblas-base libsprng2 libfftw3-3 \
  libsuitesparseconfig5 libspqr2 \
  libamd2 libcamd2 libbtf1 libcolamd2 \
  libccolamd2 libcholmod3 libcxsparse3 \
  libklu1 libldl2 libumfpack5 \
  libcfitsio8 libhdf5-103 libhdf5-cpp-103 libhealpix-cxx2 \
  opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev lsb-release \
  && apt-get clean

COPY --from=install /usr/include/zmq.hpp /usr/include/zmq.hpp
COPY --from=install /usr/include/zmq_addon.hpp /usr/include/zmq_addon.hpp

# stage in icetray from the previous build
COPY --from=install /usr/local/icetray /usr/local/icetray
COPY --from=install /opt/i3-data /opt/i3-data

# set environment variables
ENV I3_DATA /opt/i3-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data
ENV TMPDIR /scratch

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]


##################################################################
#### Now install the prod system, with i3-data and GCD files.
##################################################################

FROM base as prod

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 zlib1g libzstd1 less \
  libboost-python1.71.0-py38 libboost-system1.71.0 libboost-thread1.71.0 \
  libboost-date-time1.71.0 libboost-serialization1.71.0 \
  libboost-filesystem1.71.0 libboost-program-options1.71.0 \
  libboost-regex1.71.0 libboost-iostreams1.71.0 libgsl23 \
  libcdk5nc6 libarchive13 python3 python3-scipy \
  python3-urwid python3-numpy python3-matplotlib \
  python3-numexpr cython3 python3-cffi python3-requests \
  python3-healpy python3-urllib3 python3-jsonschema \
  libzmq5 libzmqpp4 python3-zmq python3-pymysql \
  zlib1g-dev liberfa1 libstarlink-pal0 \
  libopenblas-base libsprng2 libfftw3-3 \
  libsuitesparseconfig5 libspqr2 \
  libamd2 libcamd2 libbtf1 libcolamd2 \
  libccolamd2 libcholmod3 libcxsparse3 \
  libklu1 libldl2 libumfpack5 \
  libcfitsio8 libhdf5-103 libhdf5-cpp-103 libhealpix-cxx2 \
  opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev lsb-release \
  && apt-get clean

COPY --from=install /usr/include/zmq.hpp /usr/include/zmq.hpp
COPY --from=install /usr/include/zmq_addon.hpp /usr/include/zmq_addon.hpp

# stage in icetray from the previous build
COPY --from=install /usr/local/icetray /usr/local/icetray
COPY --from=install /opt/i3-data /opt/i3-data

# set environment variables
ENV I3_DATA /opt/i3-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data
ENV TMPDIR /scratch

# install photon tables
RUN mkdir /opt/i3-data/photon-tables && \
    mkdir /opt/i3-data/photon-tables/splines && \
    wget -nv -t 5 -O /opt/i3-data/photon-tables/splines/ems_mie_z20_a10.abs.fits       http://prod-exe.icecube.wisc.edu/spline-tables/ems_mie_z20_a10.abs.fits && \
    wget -nv -t 5 -O /opt/i3-data/photon-tables/splines/ems_mie_z20_a10.prob.fits      http://prod-exe.icecube.wisc.edu/spline-tables/ems_mie_z20_a10.prob.fits

# install baseline GCDs
RUN mkdir /opt/i3-data/baseline_gcds && \
    wget -nv -N -t 5 -P /opt/i3-data/baseline_gcds -r -l 1 -A *.i3* -nd https://icecube:skua@convey.icecube.wisc.edu/data/user/followup/baseline_gcds/ && \
    chmod -R u+rwX,go+rX,go-w /opt/i3-data/baseline_gcds

# build the matplotlib font cache (prevents warnings about the font cache on startup)
RUN python3 -c 'from matplotlib import pyplot'

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]


##################################################################
#### Now install the devel system, with a compiler and test data
##################################################################

FROM base as devel

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd-dev \
  libxml2-dev subversion git libboost-python1.71-dev \
  libboost-system1.71-dev libboost-thread1.71-dev libboost-numpy1.71-dev \
  libboost-date-time1.71-dev libboost-serialization1.71-dev \
  libboost-filesystem1.71-dev libboost-program-options1.71-dev \
  libboost-regex1.71-dev libboost-iostreams1.71-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python3-scipy \
  python3-urwid python3-numpy python3-matplotlib \
  python3-numexpr cython3 python3-cffi python3-requests \
  python3-healpy python3-urllib3 python3-jsonschema \
  python3-zmq python3-pymysql python3-dev python3-pip \
  zlib1g-dev liberfa-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev libfftw3-dev \
  libcfitsio-dev libhdf5-dev libhealpix-cxx-dev \
  opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 \
  nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/master.tar.gz && \
    tar -zxf master.tar.gz && cd cppzmq-master && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make install

# stage in icetray from the previous build
COPY --from=install /usr/local/icetray /usr/local/icetray
COPY --from=prod /opt/i3-data /opt/i3-data

# set environment variables
ENV I3_DATA /opt/i3-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data
ENV TMPDIR /scratch

# install test data
RUN rsync -vrlpt --delete code.icecube.wisc.edu::Offline/test-data/trunk/ /opt/i3-data/i3-test-data/

# build the matplotlib font cache (prevents warnings about the font cache on startup)
RUN python3 -c 'from matplotlib import pyplot'

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]


##################################################################
#### Now install the cuda system
##################################################################

FROM nvidia/cuda:11.1-cudnn8-devel-ubuntu20.04 as cuda11.1

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd-dev \
  libxml2-dev subversion git libboost-python1.71-dev \
  libboost-system1.71-dev libboost-thread1.71-dev libboost-numpy1.71-dev \
  libboost-date-time1.71-dev libboost-serialization1.71-dev \
  libboost-filesystem1.71-dev libboost-program-options1.71-dev \
  libboost-regex1.71-dev libboost-iostreams1.71-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python3-scipy \
  python3-urwid python3-numpy python3-matplotlib \
  python3-numexpr cython3 python3-cffi python3-requests \
  python3-healpy python3-urllib3 python3-jsonschema \
  python3-zmq python3-pymysql python3-dev python3-pip \
  zlib1g-dev liberfa-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev libfftw3-dev \
  libcfitsio-dev libhdf5-dev libhealpix-cxx-dev \
  opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 \
  nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/master.tar.gz && \
    tar -zxf master.tar.gz && cd cppzmq-master && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make install

RUN mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# stage in icetray from the previous build
COPY --from=install /usr/local/icetray /usr/local/icetray
COPY --from=devel /opt/i3-data /opt/i3-data

# set environment variables
ENV I3_DATA /opt/i3-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data
ENV TMPDIR /scratch

# build the matplotlib font cache (prevents warnings about the font cache on startup)
RUN python3 -c 'from matplotlib import pyplot'

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]


##################################################################
#### Now install the tensorflow system
##################################################################

FROM install as install-tf

# build NewNuFlux
RUN svn co http://code.icecube.wisc.edu/svn/sandbox/cweaver/NewNuFlux /root/combo/src/NewNuFlux \
           --username=icecube --password=skua --no-auth-cache

WORKDIR /root/combo/build
RUN cmake /root/combo/src \
      -DCMAKE_BUILD_TYPE=Release \
      -DINSTALL_TOOL_LIBS=OFF \
      -DUSE_GFILT=OFF \
      -DCMAKE_INSTALL_PREFIX=/usr/local/icetray \
      -DUSE_PYTHON3=OFF \
    && make -j4

# install icetray
RUN make install

### now make the tensorflow image

FROM cuda11.1 as tensorflow.2.4.1

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# build tensorflow
RUN pip3 install tensorflow==2.4.1

# stage in icetray from the previous build
COPY --from=install-tf /usr/local/icetray /usr/local/icetray

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]
