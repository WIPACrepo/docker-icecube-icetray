icecube/icetray
===============

Docker images of IceCube's IceTray codebase - combo metaproject.

Flavors
-------

slim: just icetray

prod: slim + tables and GCD files

devel: prod + compiler toolchain and test data

cudaX: devel + cuda support (X = cuda version)

tensorflow.X: devel + cuda + tensorflow support (X = tensorflow version)

Build versions
--------------

The general pattern is as follows.  More releases available in the tags.

### stable combo

stable-slim, combo-stable-slim, combo-stable-slim-ubuntu18.04

stable-prod, combo-stable-prod, combo-stable-prod-ubuntu18.04

latest, stable, stable-devel, combo-stable, combo-stable-devel, combo-stable-devel-ubuntu18.04

stable-cuda, stable-cuda10.1, combo-stable-cuda, combo-stable-cuda10.1, combo-stable-cuda10.1-ubuntu18.04

stable-tensorflow, stable-tensorflow.1.13.2, combo-stable-tensorflow, combo-stable-tensorflow.1.13.2, combo-stable-tensorflow.1.13.2-ubuntu18.04

### release of combo

combo-V01-00-00-slim combo-V01-00-00-slim-ubuntu18.04

combo-V01-00-00-prod combo-V01-00-00-prod-ubuntu18.04

combo-V01-00-00, combo-V01-00-00-devel combo-V01-00-00-devel-ubuntu18.04

combo-V01-00-00-cuda, combo-V01-00-00-cuda10.1, combo-V01-00-00-cuda10.1-ubuntu18.04

combo-V01-00-00-tensorflow, combo-V01-00-00-tensorflow.1.13.2, combo-V01-00-00-tensorflow.1.13.2-ubuntu18.04
