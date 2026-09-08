import argparse,json
from rtshield.domains import battery,water,robot,railway
from rtshield.simulation import run_domain
MODS={'battery':battery,'water':water,'robot':robot,'railway':railway}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--domain',choices=MODS,default='battery'); p.add_argument('--steps',type=int,default=40); p.add_argument('--attack-scale',type=float,default=0.0); p.add_argument('--unshielded',action='store_true'); a=p.parse_args()
    m,_=run_domain(MODS[a.domain].make_spec(),steps=a.steps,attack_scale=a.attack_scale,shielded=not a.unshielded); print(json.dumps(m,indent=2))
