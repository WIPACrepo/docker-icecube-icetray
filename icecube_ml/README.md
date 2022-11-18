IceTray docker images for ML tasks
==================================

Supported
---------
* Ubuntu 20.04
* Ubuntu 22.04

These images add machine learning tools to tagged version of icetray images,  along with test-data, etc.

Two flavors are created:
* icetray-cuda11.X - GPU enabled nvidia image, with copy of installed icetray, tools, etc (Ubuntu 20.04 and 22.04)
* icetray-ml-base - Adds PyTorch, IceCube low-level-ml to icetray-cuda11 image to serve as base for ML tasks. (20.04 only)

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 20.04 CUDA 11.6 icetray image:
   - icecube/icetray-ml:icetray-cuda11.6-vX.Y.Z-ubuntu20.04
   - icecube/icetray-ml:icetray-cuda11.6-vX.Y.Z-ubuntu20.04-YYYY-MM-DD
   - icecube/icetray-ml:icetray-cuda11.6-current-ubuntu20.04
- 22.04 CUDA 11.8 icetray image:
   - icecube/icetray-ml:icetray-cuda11.8-vX.Y.Z-ubuntu22.04
   - icecube/icetray-ml:icetray-cuda11.8-vX.Y.Z-ubuntu22.04-YYYY-MM-DD
   - icecube/icetray:icetray-cuda11.8-current-ubuntu22.04
- 20.04 IceCube ML base image:
   - icecube/icetray-ml:icetray-ml-base-vX.Y.Z-ubuntu20.04
   - icecube/icetray-ml:icetray-ml-base-vX.Y.Z-ubuntu20.0-YYYY-MM-DD
   - icecube/icetray-ml:icetray-ml-base-ubuntu20.04
