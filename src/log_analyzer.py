import json

from src.argument_parser import get_config
from src.processor import Processor


class LogAnalyzer:
    def __init__(self) -> None:
        self.__result: dict[str, dict] = {}
        self.__config = get_config(None)
        self.__processor = Processor(self.__config)

        self.__process_files()
        self.__create_json()

        print("Done!")

    def __process_files(self) -> None:
        for file in self.__config.input_files:
            file_result = self.__processor.process_file(file)
            self.__result[file] = file_result

    def __create_json(self) -> None:
        with open(self.__config.output_file, "w") as output_file:
            json.dump(self.__result, output_file, indent=4)
