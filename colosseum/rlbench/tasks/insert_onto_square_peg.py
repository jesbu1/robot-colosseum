from typing import List, Tuple

import numpy as np
from pyrep.objects import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import ConditionSet, DetectedCondition
from rlbench.backend.spawn_boundary import SpawnBoundary
from rlbench.backend.task import Task
from rlbench.const import colors


class InsertOntoSquarePeg(Task):
    def init_task(self) -> None:
        self._square_ring = Shape("square_ring")
        self.__chosen_pillar = None
        self._success_centre = Dummy("success_centre")
        success_detectors = [
            ProximitySensor("success_detector%d" % i) for i in range(4)
        ]
        self.register_graspable_objects([self._square_ring])
        success_condition = ConditionSet(
            [
                DetectedCondition(self._square_ring, sd)
                for sd in success_detectors
            ]
        )
        self.register_success_conditions([success_condition])

    def init_episode(self, index: int) -> List[str]:
        color_name, color_rgb = colors[index]
        spokes = [Shape("pillar0"), Shape("pillar1"), Shape("pillar2")]
        self._chosen_pillar = np.random.choice(spokes)  # type: ignore
        self._chosen_pillar.set_color(color_rgb)
        _, _, z = self._success_centre.get_position()
        x, y, _ = self._chosen_pillar.get_position()
        self._success_centre.set_position([x, y, z])

        color_choices = np.random.choice(
            list(range(index)) + list(range(index + 1, len(colors))),
            size=2,
            replace=False,
        )
        spokes.remove(self._chosen_pillar)
        for spoke, i in zip(spokes, color_choices):
            name, rgb = colors[i]
            spoke.set_color(rgb)
        b = SpawnBoundary([Shape("boundary0")])
        b.sample(self._square_ring)
        return [
            "put the ring on the %s spoke" % color_name,
            "slide the ring onto the %s colored spoke" % color_name,
            "place the ring onto the %s spoke" % color_name,
        ]

    def variation_count(self) -> int:
        return len(colors)


    def get_important_objects(self) -> Tuple[str]:
        assert self._chosen_pillar is not None, "must init_task first before calling get_important_objects"
        return ("square_ring", self._chosen_pillar.get_name())