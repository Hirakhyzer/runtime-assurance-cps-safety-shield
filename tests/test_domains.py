from rtshield.domains import battery,water,robot,railway

def test_domain_shapes_and_initial_safety():
    for mod in (battery,water,robot,railway):
        s=mod.make_spec(); assert s.model.state_dim==len(s.initial_state); assert s.property.safe.contains_point(s.initial_state); assert s.model.action_dim==len(s.action_lower)
