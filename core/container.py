from dependency_injector import containers, providers

from core.timeline import TimeLine


class DIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    timeline = providers.Singleton(
        TimeLine,
        notation=config.timeline.notation,
        log_screen=config.timeline.log_screen,
        step=config.timeline.step,
    )
    medium = providers.Factory(config.medium)
    station = providers.Factory(config.station)
    frame = providers.Factory(config.frame)
    frame_storage = providers.Factory(config.frame_storage)
    transmitter = providers.Factory(config.transmitter)
    csma = providers.Factory(config.csma)
