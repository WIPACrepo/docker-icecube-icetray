IceTray docker images for Ubuntus
==============================

Supported
---------
* Ubuntu 22.04

These images install particular tagged version of icetray along with test-data, etc.

Two flavors are created:
* devel - install of icetray in /usr/local/icetray, with /usr/local/icetray\_src

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 22.04 includes devel tagged as:
   - icecube/icetray:icetray-devel-vX.Y.Z-ubuntu22.04
   - icecube/icetray:icetray-devel-vX.Y.Z-ubuntu22.04-YYYY-MM-DD
   - icecube/icetray:icetray-devel-current-ubuntu22.04
- 22.04 includes prod tagged as:
   - icecube/icetray:icetray-prod-vX.Y.Z-ubuntu22.04
   - icecube/icetray:icetray-prod-vX.Y.Z-ubuntu22.04-YYYY-MM-DD
   - icecube/icetray:icetray-prod-current-ubuntu22.04
