from typing import List, Tuple

from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.task import Task


class SlideBlockToTarget(Task):
    def init_task(self) -> None:
        self.register_success_conditions(
            [DetectedCondition(Shape("block"), ProximitySensor("success"))]
        )

    def init_episode(self, index: int) -> List[str]:
        self._variation_index = index
        return [
            "slide the block to target",
            "slide the block onto the target",
            "push the block until it is sitting on top of the target",
            "slide the block towards the green target",
            "cover the target with the block by pushing the block in its"
            + " direction",
        ]

    def variation_count(self) -> int:
        return 1

    def get_important_objects(self) -> Tuple[str]:
        return ("block", "success")
