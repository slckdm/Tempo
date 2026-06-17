from fastapi import FastAPI

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka

from app.inbound.http.stream.router import make_stream_router
from app.main.config.loader import load_app_settings, load_keycloak_settings, load_s3_settings
from app.main.config.settings import AppSettings, KeycloakSettings, S3Settings
from app.main.ioc.core import CoreProvider
from app.main.ioc.provider_registry import get_providers
from app.outbound.providers import get_outbound_providers
from app.outbound.keycloak_client_provider import KeycloakClientProvider

def create_service() -> FastAPI:
    app_settings = load_app_settings()
    s3_settings = load_s3_settings()
    keycloak_settings = load_keycloak_settings()
    app = FastAPI(debug=app_settings.DEBUG, title=app_settings.NAME, routes=[*make_stream_router().routes])
    container = make_async_container(
        KeycloakClientProvider(),
        CoreProvider(),
        FastapiProvider(),
        *get_providers(),
        *get_outbound_providers(),
        context={
            AppSettings: app_settings,
            S3Settings: s3_settings,
            KeycloakSettings: keycloak_settings,
        },
    )
    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    import uvicorn

    app_settings = load_app_settings()

    uvicorn.run(app=create_service(), port=app_settings.PORT)
