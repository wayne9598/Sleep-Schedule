from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
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
    rem: float = None
    deep: float = None
    restfulness: float = None
    resting_heart_rate: float = None
    efficiency: float = None
    latency: float = None
    name: str = 'sleep'

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).seconds / 60

    def quality(self) -> float:
        """
            calculate sleep quality score based on duration, percentage of REM, percentage of deep, restfulness,
            resting heart rate, sleep efficiency and sleep latency.

            :return: sleep quality score
            """
        if not(all([self.rem, self.deep, self.restfulness, self.resting_heart_rate, self.efficiency, self.latency])):
            raise Exception("sleep quality unavailable due to missing sleep measures")
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
    nap_allowed: bool


@dataclass
class AirTransport(Transport):
    prep_time: float
    start_timezone: int
    end_timezone: int
    nap_allowed = True

    def __post_init__(self):
        self.start_time = self.start_time.replace(tzinfo=timezone(timedelta(hours=self.start_timezone)))
        self.end_time = self.end_time.replace(tzinfo=timezone(timedelta(hours=self.start_timezone)))

    @property
    def latest_wake_time(self):
        return self.start_time - timedelta(minutes=self.prep_time)


@dataclass
class SpaceTransport(AirTransport):
    prep_time = hr(5)
    nap_allowed = True


def time_of_day(date: datetime, hour: int, minute: int) -> datetime:
    return date.replace(hour=hour, minute=minute)


@dataclass
class Schedule:
    events: Set[Event]

    def recommend_sleep(self):
        transports = [e for e in self.events if isinstance(e, AirTransport)]
        for transport in transports:
            standard_start_sleep_time = time_of_day(transport.start_time - timedelta(days=1), 23, 0)
            standard_end_sleep_time = time_of_day(transport.start_time, 7, 0)
            recommended_start_sleep_time = standard_start_sleep_time
            recommended_end_sleep_time = standard_end_sleep_time
            destination_standard_sleep_time = standard_start_sleep_time.replace(
                tzinfo=timezone(timedelta(hours=transport.end_timezone))).astimezone(
                timezone(timedelta(hours=transport.start_timezone)))
            destination_standard_wake_time = standard_end_sleep_time.replace(
                tzinfo=timezone(timedelta(hours=transport.end_timezone))).astimezone(
                timezone(timedelta(hours=transport.start_timezone)))

            if transport.start_time - timedelta(minutes=transport.prep_time) > standard_end_sleep_time:
                self.events.add(
                    Sleep(label=Label.RECOMMENDED,
                          start_time=standard_start_sleep_time,
                          end_time=standard_end_sleep_time))

            if transport.end_time - timedelta(minutes=90) > destination_standard_sleep_time:
                self.events.add(
                    Sleep(label=Label.RECOMMENDED,
                          start_time=destination_standard_sleep_time,
                          end_time=destination_standard_wake_time))

            if transport.start_time - timedelta(minutes=transport.prep_time) < standard_end_sleep_time:
                self.events.add(
                    Sleep(label=Label.RECOMMENDED,
                          start_time=max(transport.start_time - timedelta(minutes=transport.prep_time + hr(1))
                                         - timedelta(hours=8),
                                         time_of_day(standard_start_sleep_time, 21, 0)),
                          end_time=transport.start_time - timedelta(minutes=transport.prep_time + hr(1))))

            if transport.start_time > time_of_day(transport.start_time, 22, 30) or transport.start_time < time_of_day(transport.start_time, 1, 0):
                # if spaceship departs after 10:30pm, take a 3-hr nap waking up an hour before the start prepping time
                # then take a 5-hr nap 5 hours after departure
                if isinstance(transport, SpaceTransport):
                    self.events.add(
                        Sleep(label=Label.RECOMMENDED,
                              start_time=transport.start_time - timedelta(minutes=transport.prep_time + hr(4)),
                              end_time=transport.start_time - timedelta(minutes=transport.prep_time + hr(1))))
                    self.events.add(
                        Sleep(label=Label.RECOMMENDED,
                              start_time=transport.start_time + timedelta(minutes=hr(5)),
                              end_time=transport.start_time + timedelta(minutes=hr(10))))

                # if flight departs after 10:30pm or before 1am, sleep starts 30mins after departure
                if isinstance(transport, AirTransport) and not isinstance(transport, SpaceTransport):
                    self.events.add(
                        Sleep(label=Label.RECOMMENDED,
                              start_time=transport.start_time + timedelta(minutes=30),
                              end_time=min(transport.end_time - timedelta(minutes=30), standard_end_sleep_time)))

            # if arrive before local time 7am, sleep till 7am
            if transport.end_time + timedelta(minutes=90) < destination_standard_wake_time:
                self.events.add(
                    Sleep(label=Label.RECOMMENDED,
                          start_time=transport.end_time + timedelta(minutes=90),
                          end_time=destination_standard_wake_time))


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
