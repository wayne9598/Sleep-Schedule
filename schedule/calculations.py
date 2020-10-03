import math


def rate_sleep_quality(duration: float, rem: float, deep: float, restfulness: float, resting_heart_rate: float,
                       efficiency: float, latency: float) -> float:
    """
    calculate sleep quality score based on duration, percentage of REM, percentage of deep, restfulness, resting heart
    rate, sleep efficiency and sleep latency.

    :param duration: sleep duration in minutes
    :param rem: percentage of sleep being rem sleep
    :param deep: percentage of sleep being deep sleep
    :param restfulness: percentage
    :param resting_heart_rate: percentage
    :param efficiency: percentage
    :param latency: minutes
    :return: sleep quality score
    """
    if duration > 0:
        duration_quality = 1 + math.log(1 - (abs(duration/(9 * 60) - 1)))
        rem_quality = rem * 2 + 0.5 if rem > 0.2 else rem * 6 - 0.3 if rem > 0.15 else rem * 12 - 1.2 if rem > 1 else rem / 0.1 - 1
        deep_quality = -2 * (1 + math.exp(10 * deep - 0.375)) ** -1 + 1
        latency_quality = 1 + abs(latency - 15)/15
        return (duration_quality + rem_quality + deep_quality + restfulness + resting_heart_rate + efficiency +
                latency_quality) / sum([1 for i in [duration, rem, deep, restfulness, resting_heart_rate, efficiency,
                                                    latency] if i])
    return 0
