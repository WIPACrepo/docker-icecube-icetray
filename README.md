icecube/icetray
===============

Collection of Docker images for IceCube

Varities
--------
Several image collection are included here, as subdirectories, as well as github actions to build these.  Varietials include:

* icetray_base (see [icetray_base/README.md](/icetray_base/README.md) ) - Base images that add needed system libs to basic ubuntu images
* install_icetray (see install_icetray/README.md) - Build and add icetray from tagged release, include test/production files
* icecube_ml (see icecube_ml/README.md) - Add ML toolkits and GPU support to icetray production images
* nu-sources (see neutrino_sources/README.md) - Add neutrino sources to production icetray iages
* jupyter_nb (see jupyter_nb/README.md) - Add Jupyter notebook tools to existing images (ML images, and neutrino sources)

Old material
------------
Historical collection here provide older support for combo images:
* ubuntu20.04 
* almalinux8
