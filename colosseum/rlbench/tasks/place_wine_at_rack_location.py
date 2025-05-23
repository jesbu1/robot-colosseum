from typing import List, Tuple

import numpy as np
from pyrep.objects.dummy import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task


class PlaceWineAtRackLocation(Task):
    def init_task(self):
        self.wine_bottle = Shape("wine_bottle")
        self.wine_rack = Shape("rack_bottom")
        self._init_pose_bottle_to_rack = self.wine_bottle.get_pose(
            relative_to=self.wine_rack
        )

        self.register_graspable_objects([self.wine_bottle])

        self.locations = ["middle", "left", "right"]

        self.register_waypoint_ability_start(3, self._move_to_rack)

        self.register_waypoint_ability_start(5, self._is_last)
        self.register_waypoint_ability_start(6, self._is_last)
        self.register_waypoint_ability_start(7, self._is_last)
        self.register_waypoint_ability_start(8, self._is_last)

    def init_episode(self, index: int) -> List[str]:
        self.wine_bottle.set_pose(
            self._init_pose_bottle_to_rack, relative_to=self.wine_rack
        )

        self._variation_index = index
        location = self.locations[self._variation_index]
        self.register_success_conditions(
            [
                DetectedCondition(
                    self.wine_bottle, ProximitySensor(f"success_{location}")
                ),
                NothingGrasped(self.robot.gripper),
            ]
        )

        return [
            "stack the wine bottle to the %s of the rack" % (location),
            "slide the bottle onto the %s part of the rack" % (location),
            "put the wine on the %s" % (location),
            "leave the wine on the %s section of the shelf" % (location),
            "grasp the bottle and put it away on the %s" % (location),
        ]

    def _move_to_rack(self, _):
        next1, next2 = Dummy("waypoint3"), Dummy("waypoint4")
        left1, left2 = Dummy("waypoint5"), Dummy("waypoint6")
        right1, right2 = Dummy("waypoint7"), Dummy("waypoint8")

        if self._variation_index == 1:
            next1.set_position(left1.get_position())
            next1.set_orientation(left1.get_orientation())

            next2.set_position(left2.get_position())
            next2.set_orientation(left2.get_orientation())
        elif self._variation_index == 2:
            next1.set_position(right1.get_position())
            next1.set_orientation(right1.get_orientation())

            next2.set_position(right2.get_position())
            next2.set_orientation(right2.get_orientation())

    def _is_last(self, waypoint):
        waypoint.skip = True

    def variation_count(self) -> int:
        return 3

    def base_rotation_bounds(
        self,
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        return (0, 0, -np.pi / 4.0), (0, 0, np.pi / 4.0)

    def get_important_objects(self) -> Tuple[str]:
        return (self.wine_bottle.get_name(), f"success_{self.locations[self._variation_index]}")