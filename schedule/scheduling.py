from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Set
from enum import Enum
import math


def hr(n: int) -> int:
    return n * 60


class Action(Enum):
    SLEEP_MORE = 'Sleep More'
    SLEEP_LESS = 'Sleep Less'
    MEDITATION = 'Meditation'
    TAKE_NAP = 'Take Nap'
    EXERCISE = 'Exercise'
    AMAZING = 'No further action required'
    

class Label(Enum): 
    USER_INPUT = 'user input'
    RECOMMENDED = 'system recommendation'


@dataclass
class Event:
    name: str
    label: Label
    start_time: datetime
    end_time: datetime


@dataclass
class Sleep(Event):
    name = 'sleep'
    rem: float
    deep: float
    restfulness: float
    resting_heart_rate: float
    efficiency: float
    latency: float

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).seconds / 60

    def quality(self) -> float:
        """
            calculate sleep quality score based on duration, percentage of REM, percentage of deep, restfulness,
            resting heart rate, sleep efficiency and sleep latency.

            :return: sleep quality score
            """
        if self.duration > 0:
            duration_quality = 1 + math.log(1 - (abs(self.duration / hr(9) - 1)))
            rem_quality = self.rem * 2 + 0.5 if self.rem > 0.2 else self.rem * 6 - 0.3 if self.rem > 0.15 else \
                self.rem * 12 - 1.2 if self.rem > 1 else self.rem / 0.1 - 1
            deep_quality = -2 * (1 + math.exp(10 * self.deep - 0.375)) ** -1 + 1
            latency_quality = 1 + abs(self.latency - 15) / 15
            return (duration_quality + rem_quality + deep_quality + self.restfulness + self.resting_heart_rate +
                    self.efficiency + latency_quality) / sum([1 for i in [self.duration, self.rem, self.deep,
                                                                          self.restfulness, self.resting_heart_rate,
                                                                          self.efficiency, self.latency] if i])
        return 0


@dataclass
class Exercise(Event):
    name = 'exercise'


@dataclass
class FoodIntake(Event):
    name = 'eat'


@dataclass
class Transport(Event):
    planned_duration: float


@dataclass
class AirTransport(Transport):
    prep_time: float
    start_timezone: int
    end_timezone: int

    @property
    def latest_wake_time(self):
        return self.start_time - timedelta(minutes=self.prep_time)


@dataclass
class SpaceTransport(AirTransport):
    prep_time = hr(5)


@dataclass
class Schedule:
    events: Set[Event]

    def recommend_sleep(self):
        # do some calculation here
        # self.events.add(Sleep(label=Label.RECOMMENDED))
        pass


@dataclass
class Day(Schedule):
    date: date

    @property
    def total_sleep(self) -> float:
        return sum([sleep.duration for sleep in self.events if isinstance(sleep, Sleep)])

    @property
    def average_sleep_quality(self) -> float:
        sleep_qualities = [sleep.quality for sleep in self.events if isinstance(sleep, Sleep)]
        return sum(sleep_qualities) / len(sleep_qualities)

    def sleep_recommendation(self, subjective_score):
        sleep_quality_score = self.average_sleep_quality
        recommend = set()

        if self.total_sleep > hr(9) and subjective_score >= 7:
            recommend.add(Action.SLEEP_LESS)
            recommend.add(Action.EXERCISE)

        if self.total_sleep < hr(7) and sleep_quality_score < 0.65:
            recommend.add(Action.SLEEP_MORE)
            if sleep_quality_score < 0.5:
                recommend.add(Action.MEDITATION)

        if self.total_sleep < hr(6):
            recommend.add(Action.SLEEP_MORE)

        if self.total_sleep < hr(5):
            recommend.add(Action.TAKE_NAP)

        if subjective_score > 7 or sleep_quality_score < 0.5:
            recommend.add(Action.MEDITATION)
        
        if not recommend:
            recommend.add(Action.AMAZING)

        return recommend
