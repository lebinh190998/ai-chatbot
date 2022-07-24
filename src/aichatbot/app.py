import asyncio
import httpx
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from importlib.metadata import entry_points, version
except ImportError:
    from importlib_metadata import entry_points, version

from cdislogging import get_logger

from . import logger
from .config import config, DEFAULT_CFG_PATH


# Load the configuration *before* importing models
try:
    if os.environ.get("AICHATBOT_CONFIG_PATH"):
        config.load(config_path=os.environ["AICHATBOT_CONFIG_PATH"])
    else:
        CONFIG_SEARCH_FOLDERS = [
            "/src",
            "{}/.gt/aichatbot".format(os.path.expanduser("~")),
        ]
        config.load(search_folders=CONFIG_SEARCH_FOLDERS)
except Exception as err:
    logger.exception(err)
    logger.warning("Unable to load config, using default config...", exc_info=True)
    config.load(config_path=DEFAULT_CFG_PATH)

def load_modules(app: FastAPI = None) -> None:
    for ep in entry_points()["aichatbot.modules"]:
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                init_app(app)


def app_init() -> FastAPI:
    logger.info("Initializing app")

    debug = config["DEBUG"]
    app = FastAPI(
        title="aichatbot",
        version=version("aichatbot"),
        debug=debug,
    )
    logger.info("RUN_ENV: {}".format(os.environ.get("RUN_ENV")))
    # if os.environ.get("RUN_ENV") == "dev":
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ClientDisconnectMiddleware)
    app.async_client = httpx.AsyncClient()

    # Following will update logger level, propagate, and handlers
    get_logger("aichatbot", log_level="debug" if debug == True else "info")

    # db.init_app(app)
    load_modules(app)

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Closing async client.")
        await app.async_client.aclose()

    return app


class ClientDisconnectMiddleware:
    def __init__(self, app):
        self._app = app

    async def __call__(self, scope, receive, send):
        loop = asyncio.get_running_loop()
        rv = loop.create_task(self._app(scope, receive, send))
        waiter = None
        cancelled = False
        if scope["type"] == "http":

            def add_close_watcher():
                nonlocal waiter

                async def wait_closed():
                    nonlocal cancelled
                    while True:
                        message = await receive()
                        if message["type"] == "http.disconnect":
                            if not rv.done():
                                cancelled = True
                                rv.cancel()
                            break

                waiter = loop.create_task(wait_closed())

            scope["add_close_watcher"] = add_close_watcher
        try:
            await rv
        except asyncio.CancelledError:
            if not cancelled:
                raise
        if waiter and not waiter.done():
            waiter.cancel()
