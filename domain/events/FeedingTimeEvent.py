class FeedingTimeEvent:
    def __init__(self, schedule_id, animal_id, feeding_time):
        self.schedule_id = schedule_id
        self.animal_id = animal_id
        self.feeding_time = feeding_time