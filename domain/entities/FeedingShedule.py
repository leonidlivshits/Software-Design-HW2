class FeedingSchedule:
    def __init__(self, id, animal, feeding_time, food_type):
        self.id = id
        self.animal = animal
        self.feeding_time = feeding_time
        self.food_type = food_type
        self.is_completed = False

    def mark_as_completed(self):
        self.is_completed = True