from typing import List, Tuple

from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task


class MoveHanger(Task):
    def init_task(self) -> None:
        self.hanger = Shape("clothes_hanger0")
        self.register_graspable_objects([self.hanger])
        success_detector = ProximitySensor("success_detector")
        hanger_visual = Shape("clothes_hanger_visual0")
        self.register_success_conditions(
            [
                DetectedCondition(hanger_visual, success_detector),
                NothingGrasped(self.robot.gripper),
            ]
        )

    def init_episode(self, index: int) -> List[str]:
        return [
            "move hanger onto the other rack"
            + "move the hanger from one rack to the other",
            "put the hanger on the other rack",
            "pick up the hanger and place it on the other rack",
        ]

    def variation_count(self) -> int:
        return 1

    def is_static_workspace(self) -> bool:
        return True

    def get_important_objects(self) -> Tuple[str]:
        # the racks are not even visible, so just showing the hanger
        return (self.hanger.get_name(),)
