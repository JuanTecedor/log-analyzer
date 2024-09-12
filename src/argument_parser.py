from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Optional, Self


def __get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="Log Analyzer",
        description="Parses a log file and outputs key "
                    "statistical metrics as a JSON file"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to one or more input files",
        nargs="+"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to a file to save output in plain JSON format"
    )
    parser.add_argument(
        "--mfip",
        action="store_true",
        help="Calculate most frequent IP"
    )
    parser.add_argument(
        "--lfip",
        action="store_true",
        help="Calculate least frequent IP"
    )
    parser.add_argument(
        "--eps",
        action="store_true",
        help="Calculate events per second"
    )
    parser.add_argument(
        "--bytes",
        action="store_true",
        help="Calculate total amount of bytes exchanged"
    )
    return parser


def __get_parser_args(argv: Optional[list[str]]) -> Namespace:
    return __get_parser().parse_args(argv)


@dataclass
class Configuration:
    input_files: list[str]
    output_file: str
    most_frequent_ip: bool
    least_frequent_ip: bool
    events_per_second: bool
    bytes_exchanged: bool

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> Self:
        return cls(
            input_files=namespace.input,
            output_file=namespace.output,
            least_frequent_ip=namespace.mfip,
            most_frequent_ip=namespace.lfip,
            events_per_second=namespace.eps,
            bytes_exchanged=namespace.bytes,
        )


def get_config(argv: Optional[list[str]]) -> Configuration:
    return Configuration.from_namespace(__get_parser_args(argv))
