from typing import List, Tuple

from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, GraspedCondition
from rlbench.backend.task import Task


class Hockey(Task):
    def init_task(self) -> None:
        self._stick = Shape("hockey_stick")
        self._goal = Shape("hockey_goal")
        self._ball = Shape("hockey_ball")

        self._init_relpose_stick_to_goal = self._stick.get_pose(
            relative_to=self._goal
        )
        self._init_relpose_ball_to_goal = self._ball.get_pose(
            relative_to=self._goal
        )

        self.register_success_conditions(
            [
                DetectedCondition(
                    Shape("hockey_ball"), ProximitySensor("success")
                ),
                GraspedCondition(self.robot.gripper, self._stick),
            ]
        )
        self.register_graspable_objects([self._stick])

    def init_episode(self, index: int) -> List[str]:
        self._stick.set_pose(
            self._init_relpose_stick_to_goal, relative_to=self._goal
        )
        self._ball.set_pose(
            self._init_relpose_ball_to_goal, relative_to=self._goal
        )

        return [
            "hit the ball into the net",
            "use the stick to push the hockey ball into the goal",
            "pick up the hockey stick, then swing at the ball in the "
            + "direction of the net",
            "score a hockey goal",
            "grasping one end of the hockey stick, swing it such that the "
            + "other end collides with the ball such that the ball goes "
            + "into the goal",
        ]

    def variation_count(self) -> int:
        return 1

    def get_important_objects(self) -> Tuple[str]:
        return ("hockey_stick", "hockey_ball", "hockey_goal")