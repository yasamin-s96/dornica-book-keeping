import time
from datetime import datetime
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, applications
from fastapi.openapi.docs import get_swagger_ui_html
from app import api_router
from settings import settings
from core.exception import CustomException


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        content = {
            "code": (
                exc.error_code.value
                if hasattr(exc.error_code, "value")
                else exc.error_code
            ),
            "message": exc.message,
            "errors": exc.error,
        }
        if hasattr(exc, "internal_code"):
            content["internal_code"] = exc.internal_code

        return JSONResponse(
            status_code=exc.code,
            content=content,
        )

    # @app_.exception_handler(RequestValidationError)
    # async def validation_exception_handler(request: Request, exc):
    #     errors = {}
    #     for err in exc.errors():
    #         error_code = err["type"]
    #         translated_message = error_messages.get(error_code, error_code)
    #         error = err["ctx"]
    #         recursive_errors_to_dict(errors, err["loc"][1:], error)
    #
    #     content = {
    #         "code": 422,
    #         "message": "خطا در نوع داده ورودی وجود دارد",
    #         "errors": errors,
    #     }
    #
    #     return JSONResponse(
    #         status_code=422,
    #         content=content,
    #     )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(api_router)


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_favicon_url="",
        swagger_css_url="/static/swagger/swagger-ui.css",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
    )


def disable_swagger_cdn():
    applications.get_swagger_ui_html = swagger_monkey_patch


def init_static_files(app_: FastAPI) -> None:
    app_.mount("/storage", StaticFiles(directory="storage"), name="book-images")


def init_cors(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def active_https_only(app_: FastAPI) -> None:
    app_.add_middleware(HTTPSRedirectMiddleware)


def create_app() -> FastAPI:
    # init app
    app = FastAPI(title="Library")
    # init_cors(app_=app)
    # init_logger(app_=app)

    init_routers(app_=app)
    init_listeners(app_=app)

    # disable_swagger_cdn()
    # custom_openapi(app_=app)
    init_static_files(app_=app)

    # init_limiter(app_=app, limit=1000)

    init_static_files(app_=app)
    # active_https_only(app_=app_)
    # initDb()

    return app


app = create_app()


LOG_DIR = "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

today_date = datetime.now().strftime("%Y-%m-%d")
log_file = f"{LOG_DIR}/{today_date}.log"

file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[file_handler],
)

logger = logging.getLogger("app")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    requested_path = request.url.path
    http_method = request.method

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"IP: {client_ip}, Route: {http_method} {requested_path}, "
        f"Status: {response.status_code}, Duration: {duration:.2f}s"
    )

    return response
