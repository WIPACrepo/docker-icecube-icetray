###############################################################
# Dockerfile to build the combo icetray meta-project
###############################################################

FROM icecube/ubuntu_with_i3data:2016.09.04

MAINTAINER Claudio Kopper <ckopper@icecube.wisc.edu>

# make sure to use the icecube user
USER icecube
WORKDIR /home/icecube

# check out icetray/combo/trunk
RUN mkdir /home/icecube/combo && mkdir /home/icecube/combo/build && \
    svn co http://code.icecube.wisc.edu/svn/meta-projects/combo/trunk \
           /home/icecube/combo/src \
           --username=icecube --password=skua --no-auth-cache

# build icetray
WORKDIR /home/icecube/combo/build
RUN cmake /home/icecube/combo/src \
      -DCMAKE_BUILD_TYPE=Release \
    && make -j`nproc`
# these two options seem to conflict with the way C++11/14 is
# being enabled in cmake/config.cmake
#      -DCMAKE_CXX_STANDARD_REQUIRED=True \
#      -DCMAKE_CXX_STANDARD=14 \

# build icetray test binaries
RUN make test-bins -j`nproc`

# provide the entry point to run commands
ENTRYPOINT ["/bin/bash", "/home/icecube/combo/build/env-shell.sh", "exec"]
CMD ["/bin/bash"]
