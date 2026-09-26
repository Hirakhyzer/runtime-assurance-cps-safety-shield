# Runtime Decision Audit and Traceability Protocol

## Purpose

A runtime assurance system should not only intervene; it should leave enough evidence to reconstruct why the intervention occurred. This repository therefore records a structured audit artifact for every shield decision.

The goal is **decision traceability**, not post-hoc justification. The audit record captures the state-estimation envelope, proposed action, applied action, predicted reachable set, shield status, intervention magnitude, decision reason, and method metadata that existed at decision time.

## Research Question

> Can runtime-assurance interventions remain inspectable and empirically auditable without weakening the online safety logic or conflating explanation with proof?

## Recorded evidence

Each decision audit record contains:

- simulation step;
- state-estimate source;
- estimated state center;
- lower and upper state-estimation bounds;
- nominal/proposed action;
- applied action;
- decision status (`ACCEPT`, `MODIFY`, or `FALLBACK`);
- intervention norm;
- predicted reachable-set lower and upper bounds;
- human-readable decision reason;
- shield metadata such as candidate rank, safety margin, and reachability horizon.

The audit record is intentionally separate from the shield algorithm. Recording evidence must not change which candidate action is selected.

## Exporting a trace

The installed CLI can write a complete JSON trace:

```bash
rtshield \
  --domain battery \
  --steps 40 \
  --seed 7 \
  --attack-scale 1.0 \
  --horizon 2 \
  --trace-output artifacts/battery-seed7-trace.json
```

The artifact contains the experiment configuration, aggregate metrics, and the step-level records returned by the simulation.

## Interpretation boundary

A decision trace is **not** a formal safety certificate. It records what the runtime shield computed under its current model and uncertainty assumptions.

In particular:

- a predicted reachable set is conditional on the reduced-order model and bounded uncertainty;
- a positive safety margin does not establish safety outside the configured horizon;
- a `MODIFY` decision explains that the nominal action was not selected, but does not imply malicious behavior;
- a `FALLBACK` decision means the action-grid search did not produce a certified-safe candidate under the configured screening method;
- an audit explanation should never be treated as stronger evidence than the underlying reachability calculation.

## Evaluation ideas

The trace format enables additional research questions that were previously difficult to study:

1. **Intervention concentration** — are interventions concentrated in a small number of high-risk periods or spread continuously?
2. **Candidate-search burden** — how often does the shield accept the first candidate versus search deeply into the action grid?
3. **Margin before intervention** — how close to the safety boundary are states when modification begins?
4. **Fallback precursors** — which margin, uncertainty, or proposal patterns precede fallback?
5. **Audit stability** — do small telemetry perturbations cause large changes in intervention rationale?
6. **Human verification** — can reviewers correctly reconstruct why an intervention occurred from the audit artifact?

## Reproducibility

A published trace study should report at least:

- repository commit;
- CPS domain;
- random seed;
- attack/fault-effect scale;
- simulation length;
- reachability horizon;
- action-grid density;
- state-estimation radii;
- action uncertainty;
- fallback policy;
- trace artifact identifier.

## Privacy and operational boundary

The current traces contain only synthetic simulation state, bounded abstract cyber/fault effects, and model-generated control decisions. They are not designed for logging sensitive production telemetry or operational attack data.

A deployment-oriented extension would require explicit data-retention, access-control, privacy, and tamper-evidence requirements before adopting a similar trace format.

## Research value

The audit layer makes runtime assurance measurable at the **decision level** rather than only through aggregate benchmark metrics. This supports more rigorous analysis of intervention necessity, explanation quality, uncertainty sensitivity, and human oversight while keeping the distinction between an inspectable decision record and a safety proof explicit.
