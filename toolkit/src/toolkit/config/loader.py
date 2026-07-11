from pydantic_settings import BaseSettings


def load_settings[E: BaseSettings](env_cls: type[E]) -> E:
    return env_cls()
