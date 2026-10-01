# Research Contract

## Research Question

<!-- State the core research question here -->

## Problem

<!-- What real challenge motivates this work? -->

## Gap

<!-- What does existing work not solve? -->

## Insight

<!-- What is the key contribution / observation? -->

## Method

<!-- What was designed, built, or derived? -->

## Experiment Plan Summary

<!-- Reference: EXPERIMENT_TRACKER.md -->

## Claims (initial)

<!-- Reference: CLAIM_MAP.yaml -->

## Evidence Target

<!-- What evidence level (L0-L6) is targeted? -->

## Limitations and Scope

<!-- What will NOT be claimed even if results are positive? -->

## Pipeline State

```yaml
literature:
  anchor_directory: anchor_papers

  anchor_policy:
    enabled: true
    required_when_present: true
    read_before_general_search: true
    extract_references: true
    extract_limitations: true
    extract_future_work: true
    generate_gap_hypotheses: true

  search_policy:
    expand_from_anchors: true
    backward_citations: true
    forward_citations: true
    closest_method_search: true
    limitation_driven_search: true
    recent_updates: true
    competing_methods: true

pipeline_state:
  current_stage: 0
  experiment_iteration: 0
  max_experiment_iterations: 3
  claims_supported: []
  claims_partial: []
  last_updated: "YYYY-MM-DD"
  next_action: "Anchor paper intake (if PDFs present) or define research question"
```
