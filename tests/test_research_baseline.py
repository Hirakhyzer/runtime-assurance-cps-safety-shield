from rtshield.domains import robot, battery
from rtshield.simulation import run_domain


def test_robot_shield_improves_nominal_baseline():
    spec=robot.make_spec()
    unshielded,_=run_domain(spec,steps=50,seed=0,shielded=False,attack_scale=0.0)
    shielded,_=run_domain(spec,steps=50,seed=0,shielded=True,attack_scale=0.0)
    assert unshielded['unsafe_states'] > 0
    assert shielded['unsafe_states'] == 0


def test_high_battery_corruption_triggers_shield_without_counting_shadow_actions():
    spec=battery.make_spec()
    unshielded,_=run_domain(spec,steps=50,seed=0,shielded=False,attack_scale=3.0)
    shielded,_=run_domain(spec,steps=50,seed=0,shielded=True,attack_scale=3.0)
    assert unshielded['interventions'] == 0
    assert shielded['interventions'] > 0
