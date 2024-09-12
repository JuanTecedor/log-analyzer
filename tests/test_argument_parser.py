import pytest

from src.argument_parser import Configuration, get_config


class TestParser:
    def test_defaults(self) -> None:
        with pytest.raises(SystemExit):
            _ = get_config([""])

    @pytest.mark.parametrize(
        "input_args, expected",
        [
            (
                ["-i", "file1", "-o", "file2"],
                Configuration(
                    input_files=['file1'], output_file='file2',
                    most_frequent_ip=False, least_frequent_ip=False,
                    events_per_second=False, bytes_exchanged=False
                )
            ),
            (
                [
                    "-i", "f1", "-o", "f2",
                    "--mfip", "--lfip", "--eps", "--bytes"
                ],
                Configuration(
                    input_files=['f1'], output_file='f2',
                    most_frequent_ip=True, least_frequent_ip=True,
                    events_per_second=True, bytes_exchanged=True
                )
            ),
            (
                [
                    "-i", "f1", "f2", "-o", "f2",
                    "--mfip", "--lfip", "--eps", "--bytes"
                ],
                Configuration(
                    input_files=["f1", "f2"], output_file='f2',
                    most_frequent_ip=True, least_frequent_ip=True,
                    events_per_second=True, bytes_exchanged=True
                )
            ),
        ]
    )
    def test_valid(
        self, input_args: list[str], expected: Configuration
    ) -> None:
        args = get_config(input_args)
        assert args == expected
