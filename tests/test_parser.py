import pytest

from src.parser import Parser


class TestParser:
    @pytest.mark.parametrize("log_line", [
        (
            "1157689323.718   3856 10.105.21.199 TCP_MISS/200 30169 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html"  # noqa: E501
        ),
        (
            "1335542309 35 127.0.0.1 TCP_MISS/303 -1 GET http://gadm.geovocab.org/id/1_3214_geometry_1km - NONE/- text/html"  # noqa: E501
        ),
        (
            "1035085753.021      0 210.8.79.118 UDP_MISS/000 38 ICP_QUERY http://www.house/ - NONE/- -"  # noqa: E501
        )
    ])
    def test_parse_must_match(self, log_line: str) -> None:
        parser = Parser()
        _ = parser.parse_line(log_line)
