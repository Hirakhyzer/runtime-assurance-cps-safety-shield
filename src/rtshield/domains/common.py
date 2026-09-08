from dataclasses import dataclass
import numpy as np
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty

@dataclass
class DomainSpec:
    name: str
    model: AffineDiscreteModel
    property: SafeBoxProperty
    initial_state: np.ndarray
    action_lower: np.ndarray
    action_upper: np.ndarray
    fallback_action: np.ndarray
    nominal_controller: object
    state_names: tuple[str,...]
    action_names: tuple[str,...]
    attack_action_direction: np.ndarray
