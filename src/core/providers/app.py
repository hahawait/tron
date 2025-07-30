from dishka import Provider, Scope, provide

from core.config import Config, get_config


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return get_config()
