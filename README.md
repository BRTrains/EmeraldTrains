# Emerald Trains

An Irish (ROI and NI) add-on for the BRTrains NewGRF for OpenTTD.

## Build

EmeraldTrains is a BRBuild project and expects the BRBuild checkout beside it:

```bash
BRBUILD_DIR=/home/jon/BRBuild python3 build.py --log
```

The project manifest opts into BRDocs with `project.docs: true`. Documentation generation is deliberately opt-in for normal users; the local hosted documentation build uses:

```bash
BRBUILD_DIR=/home/jon/BRBuild python3 build.py --log --docs
```

Vehicle candidates belong under `src/trains/`, and project-wide GRF metadata belongs in `src/grf/GRF.yaml`.
