import dataclasses


@dataclasses.dataclass
class Messages:
    start_message: str = "Расскажите нам какие сериалы вы уже смотрели, для формирования хороших рекомендаций :)"
