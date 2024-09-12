import pytest

from src.parser import LogLine, Parser


class TestParser:
    @pytest.mark.parametrize("log_line", [
        (
            "1157689323.718   3856 10.105.21.199 TCP_MISS/200 30169 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html\n"  # noqa: E501
        ),
        (
            "1335542309 35 127.0.0.1 TCP_MISS/303 -1 GET http://gadm.geovocab.org/id/1_3214_geometry_1km - NONE/- text/html\n"  # noqa: E501
        ),
        (
            "1035085753.021      0 210.8.79.118 UDP_MISS/000 38 ICP_QUERY http://www.house/ - NONE/- -\n"  # noqa: E501
        )
    ])
    def test_parse_must_match(self, log_line: str) -> None:
        parser = Parser()
        parsed_log_line = parser.parse_line(log_line)
        assert parsed_log_line is not None

        # For this simple examples we can compare the regex match
        # with a simple line.split()
        fields = log_line.split()
        assert len(fields) == 10
        assert parsed_log_line == LogLine(*fields)

    @pytest.mark.parametrize("log_line", [
        (
            "1035085753.021 -99 210.8.79.118 UDP_MISS/000 38 ICP_QUERY http://www.house/ - NONE/- -\n"  # noqa: E501
        ),
        (
            ""
        ),
        (
            "\n"
        ),
        (
            "1035085753.021 100 210.8.79.118 UDP_MISS/000 38 ICP_QUERY http://www.house/ - MISSING_FIELD\n"  # noqa: E501
        )
    ])
    def test_parse_non_matches(self, log_line: str) -> None:
        parser = Parser()
        parsed_log_line = parser.parse_line(log_line)
        assert parsed_log_line is None

    def test_extra_fields(self) -> None:
        log_line = "1157689323.718   3856 10.105.21.199 TCP_MISS/200 30169 GET goonernews.com badeyek DIRECT/207.58.145.61 text/html EXTRA_FIELDS"  # noqa: E501
        parser = Parser()
        parsed_log_line = parser.parse_line(log_line)
        assert parsed_log_line is None
