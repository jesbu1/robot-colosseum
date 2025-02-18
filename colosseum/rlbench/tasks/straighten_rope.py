from typing import List, Tuple

from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.task import Task


class StraightenRope(Task):
    def init_task(self) -> None:
        self.register_success_conditions(
            [
                DetectedCondition(
                    Shape("head"), ProximitySensor("success_head")
                ),
                DetectedCondition(
                    Shape("tail"), ProximitySensor("success_tail")
                ),
            ]
        )

    def init_episode(self, index: int) -> List[str]:
        return [
            "straighten rope",
            "pull the rope straight",
            "grasping each end of the rope in turn, leave the rope straight"
            + " on the table",
            "pull each end of the rope until is is straight",
            "tighten the rope",
            "pull the rope tight",
        ]

    def variation_count(self) -> int:
        return 1

    def get_important_objects(self) -> Tuple[str]:
        # TODO: probably need to have the whole rope...
        return (
            "head",
            "tail",
            "success_head",
            "success_tail",
            *(f"Joint{i}" for i in range(0, 17)),  # rope joints
        )
