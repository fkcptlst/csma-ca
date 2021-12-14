from typing import Dict, List

from utils.helper import screen_clear


class AreaDrawer:
    def __init__(
        self,
        area_size: int,
        notation: List[Dict] = [],
        default_instance: str = "default",
    ):
        self.area_size = area_size
        self.default_instance = default_instance

        notation.reverse()
        self.instances = [n["instance"] for n in notation]
        self.notations = {n["instance"]: n["notation"] for n in notation}

    def get_locations(self, participants) -> Dict[int, Dict]:
        objects = {}
        for instance in self.instances:
            if instance == self.default_instance:
                continue
            for participant in participants:
                if isinstance(participant, instance):
                    location = participant.location
                    if location is None:
                        continue
                    if objects.get(int(location[0])) is None:
                        objects[int(location[0])] = {}
                    objects[int(location[0])][int(location[1])] = (
                        instance,
                        participant,
                    )
        return objects

    def draw_screen(self, participants):
        objects = self.get_locations(participants)
        screen = ""
        for x in range(0, self.area_size):
            for y in range(0, self.area_size):
                p = objects.get(x, {}).get(y)
                if p:
                    notation = self.notations.get(p[0], "*")
                    if isinstance(notation, str):
                        screen += notation
                    else:
                        screen += notation(p[1])
                else:
                    screen += self.notations.get(self.default_instance, ". ")
            screen += "\n"

        screen_clear()
        print(screen)
