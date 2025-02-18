from typing import List, Tuple

import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task
from rlbench.const import colors


class StackCups(Task):
    def init_task(self) -> None:
        success_sensor = ProximitySensor("success")
        self.cup1 = Shape("cup1")
        self.cup2 = Shape("cup2")
        self.cup3 = Shape("cup3")
        self.cup1_visual = Shape("cup1_visual")
        self.cup2_visual = Shape("cup2_visual")
        self.cup3_visaul = Shape("cup3_visual")

        self.register_graspable_objects([self.cup1, self.cup2, self.cup3])
        self.register_success_conditions(
            [
                DetectedCondition(self.cup1, success_sensor),
                DetectedCondition(self.cup3, success_sensor),
                NothingGrasped(self.robot.gripper),
            ]
        )

    def init_episode(self, index: int) -> List[str]:
        self.variation_index = index
        target_color_name, target_rgb = colors[index]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        _, other1_rgb = colors[random_idx]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        _, other2_rgb = colors[random_idx]

        self.cup2_visual.set_color(target_rgb)
        self.cup1_visual.set_color(other1_rgb)
        self.cup3_visaul.set_color(other2_rgb)

        return [
            "stack the other cups on top of the %s cup" % target_color_name,
            "place two of the cups onto the odd cup out",
            "put the remaining two cups on top of the %s cup"
            % target_color_name,
            "pick up and set the cups down into the %s cup" % target_color_name,
            "create a stack of cups with the %s cup as its base"
            % target_color_name,
            "keeping the %s cup on the table, stack the other two onto it"
            % target_color_name,
        ]

    def variation_count(self) -> int:
        return len(colors)

    def get_important_objects(self) -> Tuple[str]:
        return (self.cup1.get_name(), self.cup2.get_name(), self.cup3.get_name())