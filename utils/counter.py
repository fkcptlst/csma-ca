class Counter:
    value: int

    def __init__(self, slot=1, value=0):
        self.slot = int(slot)
        self.value = int(slot * value)

    def increase(self, step=1):
        self.value += step

    def decrease(self, step=1):
        self.value -= step

    def reset(self, value=0):
        self.value = int(self.slot * value)

    def is_left(self) -> bool:
        return self.value > 0
