from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict
from datetime import datetime
from ipaddress import IPv4Address
from typing import Optional

from src.argument_parser import Configuration
from src.parser import LogLine


class Stat(ABC):
    @abstractmethod
    def process_line(self, log_line: LogLine) -> None:
        pass

    @abstractmethod
    def serialize(
        self, configuration: Configuration
    ) -> dict[str, str | int | float | None]:
        pass


class TotalBytesStat(Stat):
    def __init__(self) -> None:
        self.__accumulator = 0

    def process_line(self, log_line: LogLine) -> None:
        self.__accumulator += max(log_line.response_size, 0)

    def serialize(
        self, _: Configuration
    ) -> dict[str, str | int | float | None]:
        return {"total_bytes": self.__accumulator}


class IPFrequencyStat(Stat):
    def __init__(self) -> None:
        self.__ip_count: dict[IPv4Address, int] = defaultdict(int)

    def process_line(self, log_line: LogLine) -> None:
        self.__ip_count[log_line.client_ip] += 1

    def serialize(
        self, configuration: Configuration
    ) -> dict[str, str | int | float | None]:
        serialized_dict: dict[str, str | int | float | None] = {}

        if configuration.least_frequent_ip:
            serialized_dict["least_frequent_ip"] = None
        if configuration.most_frequent_ip:
            serialized_dict["most_frequent_ip"] = None

        if not self.__ip_count:
            return serialized_dict

        sorted_ip_count = OrderedDict(
            sorted(self.__ip_count.items(), key=lambda x: x[1])
        )
        sorted_keys = list(sorted_ip_count.keys())
        if configuration.least_frequent_ip:
            serialized_dict["least_frequent_ip"] = str(sorted_keys[0])
        if configuration.least_frequent_ip:
            serialized_dict["most_frequent_ip"] = str(sorted_keys[-1])

        return serialized_dict


class EventsPerSecondStat(Stat):
    def __init__(self) -> None:
        self.__second_event_count: dict[datetime, int] = defaultdict(int)

    def process_line(self, log_line: LogLine) -> None:
        self.__second_event_count[log_line.timestamp.replace(microsecond=0)] \
            += 1

    def serialize(
        self, _: Configuration
    ) -> dict[str, str | int | float | None]:
        value: Optional[float] = None

        if self.__second_event_count:
            counts = [count for count in self.__second_event_count.values()]
            value = sum(counts) / len(counts)

        return {"events_per_second": value}
