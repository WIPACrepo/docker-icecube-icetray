icecube/icetray
===============

Collection of Docker images for IceCube

Varieties
---------
Several image collection are included here, as subdirectories, as well as github actions to build these.   All images are also tagged with a build date if a specific version must be used. Varietials include:

* icetray_base (see [icetray_base/README.md](/icetray_base/README.md) ) - Base images that add needed system libs to basic ubuntu images, generates:
  * icecube/icetray-base:devel-ubuntu22.04
  * icecube/icetray-base:devel-ubuntu22.04-cudaX.X-cudnnX (e.g. devel-ubuntu22.04-cuda12.1.0-cudnn8)
  * icecube/icetray-base:devel-ubuntu22.04-pytorchX.X-cudaX.X-cudnnX (e.g. devel-ubuntu22.04-pytorch2.2.2-cuda12.1.0-cudnn8)
  * icecube/icetray-base:devel-rocky9
  * icecube/icetray-base:devel-rocky9-cudaX.X-cudnnX.X (e.g. devel-rocky9-cuda12.1.0-cudnn8)
* install_icetray (see [install_icetray/README.md](/install_icetray/README.md) ) - Build and add icetray from tagged release, generates:
  * icecube/icetray:icetray-devel-ICETRAY_VERSION-ubuntu22.04 (e.g. icetray-devel-v1.13.0-ubuntu22.04)
* icecube_ml (see [icecube_ml/README.md](/icecube_ml/README.md) ) - Add ML toolkits and GPU support to ML base images, and add icetray software from icetray images, generates:
  * icecube/icetray-ml:icetray-ICETRAY_VERSION-cudaX.X-cudnnX-ubuntu22.04
  * icecube/icetray-ml:icetray-ICETRAY_VERSION-cuda12.1-cudnn8-graphnet-ubuntu22.04-devel
* nu-sources (see [neutrino_sources/README.md](/neutrino_sources/README.md) ) - Add neutrino sources tools to icetray images, generates:
  * icecube/nu-sources:base-current-ubuntu22.04
* jupyter_nb (see [jupyter_nb/README.md](/jupyter_nb/README.md) ) - Add Jupyter notebook tools to existing images (ML images, and neutrino sources), generates:
  * icecube/icetray-nb:icetray-ml-base-current-ubuntu20.04
  * icecube/icetray-nb:nu-sources-nb-current-ubuntu22.04,
* realtime_images (see [realtime_images/README.md](realtime_images/README.md) ) - Compile Icetray and use it for a parasitic build of realtime metaproject.  It also adds needed python/system packages and reference files. Generates:
  * icecube/icetray-realtime:icetray-realtime-current-ubuntu22.04

