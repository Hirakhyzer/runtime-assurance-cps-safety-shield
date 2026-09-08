from __future__ import annotations
import numpy as np
from rtshield.estimation.interval import IntervalStateEstimator
from rtshield.shields.reachability import ReachabilityShield
from rtshield.core.types import ActionProposal, DecisionStatus
from rtshield.metrics import RuntimeMetrics

def run_domain(spec,steps=60,seed=0,shielded=True,attack_scale=0.0,horizon=2):
    rng=np.random.default_rng(seed); x=spec.initial_state.copy(); metrics=RuntimeMetrics(); records=[]
    estimator=IntervalStateEstimator(measurement_radius=np.ones_like(x)*0.04,twin_radius=np.ones_like(x)*0.08)
    shield=ReachabilityShield(spec.model,spec.property,spec.action_lower,spec.action_upper,spec.fallback_action,horizon=horizon,grid_points=7,action_uncertainty=0.03)
    twin=x.copy()
    for k in range(steps):
        active = bool(attack_scale and k>=steps//3 and k<2*steps//3)
        measurement=x+rng.normal(0,0.015,size=x.shape)
        if active:
            # Synthetic bounded telemetry displacement, independent of any real protocol.
            measurement=measurement+attack_scale*np.sign(np.arange(x.size)%2-0.5)*0.03
        estimate=estimator.estimate(measurement,twin)
        nominal=np.asarray(spec.nominal_controller(estimate.center),float)
        proposed=nominal.copy()
        if active:
            # Abstract controller-output corruption; the shield sees and filters the corrupted proposal.
            proposed=proposed + attack_scale*0.75*np.asarray(spec.attack_action_direction,float)
        decision=shield.filter(estimate,ActionProposal(proposed,controller="synthetic_corrupted" if active else "nominal"))
        u=decision.applied_action if shielded else np.clip(proposed,spec.action_lower,spec.action_upper)
        w=rng.uniform(spec.model.disturbance.lower,spec.model.disturbance.upper)
        x=spec.model.step_point(x,u,w)
        twin=spec.model.step_point(twin,u,np.zeros(spec.model.state_dim))
        actual_safe=spec.property.safe.contains_point(x); margin=float(min(np.min(x-spec.property.safe.lower),np.min(spec.property.safe.upper-x)))
        if shielded:
            metrics.update(decision,actual_safe,margin)
        else:
            # Do not count shadow-shield recommendations as interventions actually applied.
            class Shadow:
                status=DecisionStatus.ACCEPT; intervention_norm=0.0
            metrics.update(Shadow(),actual_safe,margin)
        records.append({'step':k,'safe':actual_safe,'attack_active':active,'status':decision.status.value if shielded else 'UNSHIELDED','intervention':decision.intervention_norm if shielded else 0.0,'margin':margin})
    return metrics.summary(),records
