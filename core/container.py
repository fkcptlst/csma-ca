from dependency_injector import containers, providers

from core.time.line import TimeLine


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = config.settings

    timeline = providers.Singleton(
        TimeLine,
        notation=config.notation,
        interval=config.settings.interval,
        step=config.settings.step,
        max_time=config.settings.max_time,
        area_size=config.settings.area_size,
        log_screen=config.settings.log_screen,
    )
    medium = providers.Factory(config.medium)
    station = providers.Factory(config.station)
    frame = providers.Factory(config.frame)
    frame_storage = providers.Factory(config.frame_storage)
    transmitter = providers.Factory(config.transmitter)
    csma = providers.Factory(config.csma)
