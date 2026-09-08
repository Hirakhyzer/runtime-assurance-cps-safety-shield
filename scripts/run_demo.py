import json
from rtshield.domains import battery,water,robot,railway
from rtshield.simulation import run_domain
for mod in (battery,water,robot,railway):
    m,_=run_domain(mod.make_spec(),steps=30,seed=7,shielded=True,attack_scale=1.0)
    print(mod.make_spec().name, json.dumps(m,sort_keys=True))
