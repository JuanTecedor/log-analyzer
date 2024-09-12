import re
from datetime import datetime
from ipaddress import IPv4Address
from logging import Logger
from typing import Final, Optional

logger = Logger(__name__)


class LogLine:
    def __init__(
        self,
        timestamp: str,
        response_header_size: str,
        client_ip: str,
        response_code: str,
        response_size: str,
        http_method: str,
        url: str,
        username: str,
        type_of_access_and_dest_address: str,
        response_type: str
    ) -> None:
        self.timestamp = datetime.fromtimestamp(float(timestamp))
        self.response_header_size = int(response_header_size)
        self.client_ip = IPv4Address(client_ip)
        self.response_code = response_code
        self.response_size = int(response_size)
        self.http_method = http_method
        self.url = url
        self.username = username
        self.type_of_access_and_dest_address = type_of_access_and_dest_address
        self.response_type = response_type

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, LogLine):
            return False
        return vars(self) == vars(value)


class Parser:
    __EXPECTED_FIELD_COUNT: Final[int] = 10

    __DELIMITER_RE = r'\s'
    __DELIMITER_MULTIPLE_RE = r'\s+'
    __TIMESTAMP_RE = r'(\d+(?:\.\d+)*)'
    __RESPONSE_HEADER_SIZE_RE = r'(\d+)'
    __RESPONSE_SIZE_RE = r'(-?\d+)'
    __CLIENT_IP_RE = r'((?:[0-9]{1,3}\.){3}[0-9]{1,3})'
    __RESPONSE_CODE_RE = r'([A-Z_]+/\d{3})'
    __HTTP_METHOD_RE = r'([A-Z\_]+)'
    __URL_RE = r'(\S+)'
    __USERNAME_RE = r'(\S+)'
    __TYPE_OF_ACCESS_AND_DEST_ADDRESS_RE = r'(\S+)'
    __REPONSE_TYPE_RE = r'(\S+)'
    __LOG_RE = (
        __TIMESTAMP_RE + __DELIMITER_MULTIPLE_RE
        + __RESPONSE_HEADER_SIZE_RE + __DELIMITER_RE
        + __CLIENT_IP_RE + __DELIMITER_RE
        + __RESPONSE_CODE_RE + __DELIMITER_RE
        + __RESPONSE_SIZE_RE + __DELIMITER_RE
        + __HTTP_METHOD_RE + __DELIMITER_RE
        + __URL_RE + __DELIMITER_RE
        + __USERNAME_RE + __DELIMITER_RE
        + __TYPE_OF_ACCESS_AND_DEST_ADDRESS_RE + __DELIMITER_RE
        + __REPONSE_TYPE_RE
    )
    __COMPILED_RE = re.compile(__LOG_RE)

    def __init__(self) -> None:
        self.__ignored_lines = 0

    def __ignore_line(self, line: str) -> None:
        self.__ignored_lines += 1
        logger.warning(f"Ignoring line: {line}")
        logger.warning(f"Ignored lines so far: {self.__ignored_lines}")

    def parse_line(self, line: str) -> Optional[LogLine]:
        if line == '\n':
            return None

        match = Parser.__COMPILED_RE.match(line)
        if match is None:
            self.__ignore_line(line)
            logger.warning(
                f'Line "{line}" does not follow regex expression "'
                f'{Parser.__LOG_RE}", ignoring it.'
            )
            logger.warning("Wrong format")
            return None

        fields = match.groups()
        if len(fields) != Parser.__EXPECTED_FIELD_COUNT:
            self.__ignore_line(line)
            logger.warning(
                f"Wrong format, we found {len(fields)} "
                f"when we were expecting {Parser.__EXPECTED_FIELD_COUNT}"
            )
            return None

        return LogLine(*fields)
