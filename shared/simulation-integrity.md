# Simulation Integrity — Global Rule

## Physics configuration must be documented

All simulation experiments must document:
- Simulator name and version
- Physics step size (ms)
- Control sampling rate (Hz)
- Sensor update rate (Hz)
- Real-time factor during run
- Vehicle dynamics model source
- Actuator limits
- Collision model

## Shared condition requirement

Method and baseline must share:
- Same world / environment file
- Same physics configuration
- Same vehicle dynamics
- Same sensor models
- Same collision model

Any difference invalidates a fair comparison.

## Real-time factor threshold

For timing results:
- RTF must be ≥ 0.95 during the experiment
- If RTF < 0.95, timing results cannot be reported as valid

## Reproducibility

Simulation experiments must be reproducible from:
- Documented world file
- Documented launch command
- Documented seed
