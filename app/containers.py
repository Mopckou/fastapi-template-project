from dependency_injector import containers, providers

from .database import DataBase
from .repositories.user import UserRepository
from .services.user import UserService
from .settings import get_settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(get_settings().model_dump())

    db = providers.Singleton(DataBase, db_url=config.db_url, debug_mode=config.debug)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )
