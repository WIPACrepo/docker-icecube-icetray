IceTray docker images for Jupyter NB
====================================

Supported
---------
* Ubuntu 20.04

These images add a jupyter NB framework to existing IceTray image

Two versions are created:
* icetray-ml - Add jupyter interface to icetray-ml-base image
* nu-sources - Add jupyter interface to nu-sources base image

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 20.04 CUDA 11.6 icecube ml based Jupyter images:
   - icecube/icetray-nb:icetray-ml-base-current-ubuntu20.04
   - icecube/icetray-nb:icetray-ml-base-current-ubuntu20.04-YYYY-MM-DD
- 20.04 nu-sources base image Jupyter images:
   - icecube/icetray-nb:nu-sources-nb-current-ubuntu20.04
   - icecube/icetray-nb:nu-sources-nb-current-ubuntu20.04-YYYY-MM-DD
