from datetime import time

class FeedingTime:
    def __init__(self, hour: int, minute: int):
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("Некорректное время")
        self.value = time(hour, minute)