import json
from rtshield.simulation import run_domain
from rtshield.domains import battery,water,robot,railway

def run_suite(seeds=(0,1,2)):
    out={}
    for mod in (battery,water,robot,railway):
        spec=mod.make_spec(); rows=[]
        for shielded in (False,True):
            for attack in (0.0,1.0,3.0):
                vals=[]
                for seed in seeds:
                    m,_=run_domain(spec,steps=50,seed=seed,shielded=shielded,attack_scale=attack)
                    vals.append(m)
                rows.append({'shielded':shielded,'attack_scale':attack,'unsafe_states_mean':sum(v['unsafe_states'] for v in vals)/len(vals),'intervention_rate_mean':sum(v['intervention_rate'] for v in vals)/len(vals)})
        out[spec.name]=rows
    return out
