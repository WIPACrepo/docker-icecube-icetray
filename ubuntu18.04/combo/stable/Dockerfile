##### first, install a base Ubuntu system (with development packages)

FROM ubuntu:18.04 as base

FROM base as install

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd1-dev \
  libxml2-dev subversion libboost-python-dev \
  libboost-system-dev libboost-signals-dev libboost-thread-dev \
  libboost-date-time-dev libboost-serialization-dev \
  libboost-filesystem-dev libboost-program-options-dev \
  libboost-regex-dev libboost-iostreams-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev \
  libcfitsio-dev libhdf5-serial-dev \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 python-zmq python-pymysql \
  python-dev python-pip nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/v4.5.0.tar.gz && \
    tar -zxf v4.5.0.tar.gz && cd cppzmq-4.5.0 && \
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
RUN mkdir /root/combo && mkdir /root/combo/build && \
    svn co http://code.icecube.wisc.edu/svn/meta-projects/combo/stable /root/combo/src \
           --username=icecube --password=skua --no-auth-cache

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
  tar wget rsync gzip bzip2 xz-utils liblzma5 zlib1g libzstd1 \
  less \
  libboost-python1.65 \
  libboost-system1.65 libboost-signals1.65 libboost-thread1.65 \
  libboost-date-time1.65 libboost-serialization1.65 \
  libboost-filesystem1.65 libboost-program-options1.65 \
  libboost-regex1.65 libboost-iostreams1.65 libgsl23 \
  libcdk5 libarchive13 python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal0 \
  libopenblas-base libsprng2 \
  libsuitesparseconfig5 libspqr2 \
  libamd2 libcamd2 libbtf1 libcolamd2 \
  libccolamd2 libcholmod3 libcxsparse3 \
  libklu1 libldl2 libumfpack5\
  libcfitsio5 libhdf5-100 \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmqpp4 python-zmq python-pymysql \
  python lsb-release \
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
  tar wget rsync gzip bzip2 xz-utils liblzma5 zlib1g libzstd1 \
  less \
  libboost-python1.65 \
  libboost-system1.65 libboost-signals1.65 libboost-thread1.65 \
  libboost-date-time1.65 libboost-serialization1.65 \
  libboost-filesystem1.65 libboost-program-options1.65 \
  libboost-regex1.65 libboost-iostreams1.65 libgsl23 \
  libcdk5 libarchive13 python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal0 \
  libopenblas-base libsprng2 \
  libsuitesparseconfig5 libspqr2 \
  libamd2 libcamd2 libbtf1 libcolamd2 \
  libccolamd2 libcholmod3 libcxsparse3 \
  libklu1 libldl2 libumfpack5\
  libcfitsio5 libhdf5-100 \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  ipython \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmqpp4 python-zmq python-pymysql \
  python lsb-release \
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
    wget -nv -N -t 5 -P /opt/i3-data/baseline_gcds -r -l 1 -A *.i3* -nd http://icecube:skua@convey.icecube.wisc.edu/data/user/followup/baseline_gcds/ && \
    chmod -R u+rwX,go+rX,go-w /opt/i3-data/baseline_gcds

# build the matplotlib font cache (prevents warnings about the font cache on startup)
RUN python -c 'from matplotlib import pyplot'

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
  less build-essential cmake libbz2-dev libzstd1-dev \
  libxml2-dev subversion libboost-python-dev \
  libboost-system-dev libboost-signals-dev libboost-thread-dev \
  libboost-date-time-dev libboost-serialization-dev \
  libboost-filesystem-dev libboost-program-options-dev \
  libboost-regex-dev libboost-iostreams-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev \
  libcfitsio-dev libhdf5-serial-dev \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  ipython \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 python-zmq python-pymysql \
  python-dev python-pip nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/v4.5.0.tar.gz && \
    tar -zxf v4.5.0.tar.gz && cd cppzmq-4.5.0 && \
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
RUN python -c 'from matplotlib import pyplot'

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]


##################################################################
#### Now install the cuda system
##################################################################

FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04 as cuda10.2

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd1-dev \
  libxml2-dev subversion libboost-python-dev \
  libboost-system-dev libboost-signals-dev libboost-thread-dev \
  libboost-date-time-dev libboost-serialization-dev \
  libboost-filesystem-dev libboost-program-options-dev \
  libboost-regex-dev libboost-iostreams-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev \
  libcfitsio-dev libhdf5-serial-dev \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  ipython \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 python-zmq python-pymysql \
  python-dev python-pip nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/v4.5.0.tar.gz && \
    tar -zxf v4.5.0.tar.gz && cd cppzmq-4.5.0 && \
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
RUN python -c 'from matplotlib import pyplot'

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

FROM tensorflow/tensorflow:2.1.0-gpu as tensorflow.2.1.0

MAINTAINER IceCube <developers@icecube.wisc.edu>

WORKDIR /root

# install system packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tar wget rsync gzip bzip2 xz-utils liblzma5 liblzma-dev zlib1g zlib1g-dev \
  less build-essential cmake libbz2-dev libzstd1-dev \
  libxml2-dev subversion libboost-python-dev \
  libboost-system-dev libboost-signals-dev libboost-thread-dev \
  libboost-date-time-dev libboost-serialization-dev \
  libboost-filesystem-dev libboost-program-options-dev \
  libboost-regex-dev libboost-iostreams-dev libgsl0-dev \
  libcdk5-dev libarchive-dev python-scipy \
  python-urwid python-numpy python-matplotlib \
  libz-dev libstarlink-pal-dev \
  libopenblas-dev libsprng2-dev \
  libsuitesparse-dev \
  libcfitsio-dev libhdf5-serial-dev \
  python-numexpr cython python-cffi \
  python-healpy python-urllib3 python-jsonschema \
  ipython \
  python-requests opencl-headers opencl-c-headers opencl-clhpp-headers \
  ocl-icd-libopencl1 ocl-icd-opencl-dev \
  libzmq5 libzmq3-dev libzmqpp-dev libzmqpp4 python-zmq python-pymysql \
  python-dev python-pip nano vim sudo man-db lsb-release \
  && apt-get clean

RUN wget https://github.com/zeromq/cppzmq/archive/v4.5.0.tar.gz && \
    tar -zxf v4.5.0.tar.gz && cd cppzmq-4.5.0 && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make install

RUN pip install Keras==2.3.1 tensorflow-probability==0.8.0

RUN mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# stage in icetray from the previous build
COPY --from=install-tf /usr/local/icetray /usr/local/icetray
COPY --from=devel /opt/i3-data /opt/i3-data

# set environment variables
ENV I3_DATA /opt/i3-data
ENV I3_TESTDATA /opt/i3-data/i3-test-data
ENV TMPDIR /scratch

# build the matplotlib font cache (prevents warnings about the font cache on startup)
RUN python -c 'from matplotlib import pyplot'

# create the scratch directory
RUN mkdir -p /scratch

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/usr/local/icetray/env-shell.sh", "exec"]
CMD ["/bin/bash"]
