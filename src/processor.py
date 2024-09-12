from src.argument_parser import Configuration
from src.parser import Parser
from src.stats import (EventsPerSecondStat, IPFrequencyStat, Stat,
                       TotalBytesStat)

# TODO assume empty log files are not a problem


class Processor:
    def __init__(self, configuration: Configuration) -> None:
        self.__configuration = configuration

    def process_file(
        self, file_name: str
    ) -> dict[str, str | int | float | None]:
        # TODO Assume stats are per-file basis
        stats: list[Stat] = []
        if self.__configuration.bytes_exchanged:
            stats.append(TotalBytesStat())
        if self.__configuration.events_per_second:
            stats.append(EventsPerSecondStat())
        if self.__configuration.most_frequent_ip \
           or self.__configuration.least_frequent_ip:
            stats.append(IPFrequencyStat())

        print(f'Processing file: "{file_name}"')
        parser = Parser()
        with open(file_name) as log_file:
            for line in log_file:
                log_line = parser.parse_line(line)
                if log_line is not None:
                    for stat in stats:
                        stat.process_line(log_line)

        print("File processed, saving stats")
        result: dict[str, str | int | float | None] = {}
        for stat in stats:
            result |= stat.serialize(self.__configuration)

        print(f'Done with file: "{file_name}"', end="\n\n")
        return result
