from src.settings import KinopoiskConfig


class KinopoiskSaveInfoFileRepository:
    def __init__(self, config: KinopoiskConfig) -> None:
        self._file_path = config.info_file_path
        self._default_value = 1

    def write(self, data: int) -> None:
        with open(self._file_path, "w") as file:
            file.write(str(data))

    def read(self) -> int:
        try:
            with open(self._file_path, "r") as file:
                data = file.readline()
            return int(data)
        except FileNotFoundError:
            return self._default_value
