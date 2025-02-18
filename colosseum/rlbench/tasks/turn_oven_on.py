from typing import List, Tuple

from pyrep.objects.joint import Joint
from pyrep.objects.object import Object
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import JointCondition
from rlbench.backend.task import Task


class TurnOvenOn(Task):
    def init_task(self) -> None:
        knob_joint = Joint("oven_knob_joint")
        self.register_success_conditions([JointCondition(knob_joint, 1.5)])

    def init_episode(self, index: int) -> List[str]:
        return [
            "turn on the oven",
            "grip the left most knob on the oven and rotate it anti-"
            + "clockwise to turn the oven on",
            "turn the left most knob on the oven to switch the oven on",
            "heat up the oven",
            "get the oven hot",
            "preheat the oven",
            "get the oven heat going",
        ]

    def variation_count(self) -> int:
        return 1

    def base_rotation_bounds(
        self,
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        return (0, 0, -3.14 / 4.0), (0, 0, 3.14 / 4.0)

    def boundary_root(self) -> Object:
        return Shape("turn_oven_on_boundary_root")

    def get_important_objects(self) -> Tuple[str]:
        # TODO: probably need to have more than just the oven knob? idk
        return ("oven_knob_9",)
