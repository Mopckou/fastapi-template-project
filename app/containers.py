from dependency_injector import containers, providers

from app.utils.database import PostgresDataBaseMaker
from .services.user import UserService
from .settings import get_settings
from .utils.uow import PgUnitOfWork


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()
    db = providers.Singleton(PostgresDataBaseMaker, db_url=config.db_url, debug_mode=config.debug)


class UnitOfWorks(containers.DeclarativeContainer):
    gateways = providers.DependenciesContainer()

    pg = providers.Factory(
        PgUnitOfWork,
        session_factory=gateways.db.provided.session,
    )


class ApplicationLayerServices(containers.DeclarativeContainer):

    config = providers.Configuration()
    unit_of_works = providers.DependenciesContainer()

    user = providers.Factory(
        UserService,
        uow=unit_of_works.pg
    )


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.from_dict(get_settings().model_dump())

    gateways = providers.Container(
        Gateways,
        config=config,
    )

    uow = providers.Container(
        UnitOfWorks,
        gateways=gateways,
    )

    services = providers.Container(
        ApplicationLayerServices,
        config=config,
        unit_of_works=uow,
    )
