Base docker images for Ubuntus
==============================

Supported
---------
* Ubuntu 20.04
* Ubuntu 22.04

These packages are not tied to a particular icetray version, but serve as a development and deployable base for other software to be added to.

Two flavors are created:
* devel - includes all tools and libraries needed to compile icetray and tools
* prod - includes only libraries needed at runtime in deployment situations 

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 20.04 includes devel tagged as:
   - icecube/icetray-base:devel-ubuntu20.04
   - icecube/icetray-base:devel-ubuntu20.04-YYYY-MM-DD
- 20.04 includes prod tagged as:
   - icecube/icetray-base:prod-ubuntu20.04
   - icecube/icetray-base:prod-ubuntu20.04-YYYY-MM-DD
- 22.04 includes devel tagged as:
   - icecube/icetray-base:devel-ubuntu22.04
   - icecube/icetray-base:devel-ubuntu22.04-YYYY-MM-DD
- 22.04 includes base tagged as:
   - icecube/icetray-base:prod-ubuntu22.04
   - icecube/icetray-base:prod-ubuntu22.04-YYYY-MM-DD
