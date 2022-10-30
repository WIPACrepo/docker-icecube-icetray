Base docker images for Ubuntus
==============================

Supported
---------
* Ubuntu 20.04
* Ubuntu 22.04

These packages are not tied to a particular icetray version, but serve as a development and deployable base for other software to be added to.

Deploying
---------
Uses docker github actions to build per docker/setup-buildx-action

Versions
--------
- 20.04 includes base-devel tagged as:
   - icecube/icetray:base-devel-ubuntu20.04
   - icecube/icetray:base-devel-ubuntu20.04-YYYY-MM-DD
   - icecube/icetray:base-devel-ubuntu20.04-latest
   - icecube/icetray:base-devel
   - icecube/icetray:base-devel-latest
- 20.04 includes base tagged as:
   - icecube/icetray:base-ubuntu20.04
   - icecube/icetray:base-ubuntu20.04-YYYY-MM-DD
   - icecube/icetray:base-ubuntu20.04-latest
   - icecube/icetray:base
   - icecube/icetray:base-latest

- 22.04 includes base-devel tagged as:
   - icecube/icetray:base-devel-ubuntu22.04
   - icecube/icetray:base-devel-ubuntu22.04-YYYY-MM-DD
   - icecube/icetray:base-devel-ubuntu22.04-latest
- 22.04 includes base tagged as:
   - icecube/icetray:base-ubuntu22.04
   - icecube/icetray:base-ubuntu22.04-YYYY-MM-DD
   - icecube/icetray:base-ubuntu22.04-latest
