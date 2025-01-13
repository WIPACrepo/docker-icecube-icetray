Base docker images for Ubuntus
==============================

Supported
---------
* Ubuntu 22.04
* Rocky linux 9

These packages are not tied to a particular icetray version, but serve as a development and deployable base for other software to be added to.

One flavor is created:
* devel - includes all tools and libraries needed to compile icetray and tools

Note:  "prod" images no longer supported, just use the devel.

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 22.04 includes devel tagged as:
   - icecube/icetray-base:devel-ubuntu22.04
   - icecube/icetray-base:devel-ubuntu22.04-YYYY-MM-DD
- 22.04 includes base tagged as:
   - icecube/icetray-base:prod-ubuntu22.04
   - icecube/icetray-base:prod-ubuntu22.04-YYYY-MM-DD
