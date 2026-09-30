# Experiment Integrity — Global Rule

These rules govern all experiments in ARIS Engineering Robotics.

## Reproducibility requirements

Every experiment must document:
- Exact software version (git commit hash)
- Exact launch command or script
- All configuration parameters (not "default parameters")
- Random seed policy
- Result file paths

## Artifact requirements

Result files must exist before they are cited as evidence.
Metric values in summary files must match values in source result files.
Scripts that generated results must be identified.

## Baseline fairness (hard requirement)

All methods and baselines compared in the same paper must be tested under
identical conditions:
- Same initial conditions
- Same reference trajectory / target
- Same noise seeds
- Same disturbance seeds
- Same constraint set
- Same control rate
- Same estimator (if comparing controllers)

Any asymmetry must be explicitly documented and justified.

## Single-run prohibition

Do not report a single trial as the primary evidence for any performance claim.
Use N ≥ 5 trials for aggregate statistics.

## Negative result obligation

If the proposed method fails on a test, report it.
Do not selectively report only trials where the method succeeded.
