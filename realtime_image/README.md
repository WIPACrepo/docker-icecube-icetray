IceTray + Realtime docker images for Ubuntu
===========================================

Supported
---------
* Ubuntu 22.04

These images install particular tagged version of icetray along with realtime compliled against it etc.

One flavors is created:
* devel - install of icetray in /usr/local/icetray, with /usr/local/icetray\_src

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 22.04 includes devel tagged as:
   - icecube/icetray-realtime:icetray-vX.Y.Z-realtime-vX.Y.Z-ubuntu22.04
   - icecube/icetray-realtime:icetray-realtime-current-ubuntu22.04
