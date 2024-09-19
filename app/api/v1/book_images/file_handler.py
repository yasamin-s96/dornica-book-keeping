import os
from datetime import datetime

from fastapi import UploadFile
from core.exception.base import ValidateFileException
from settings import settings


def get_file_extension(file_name: str) -> str:
    return file_name.split(".")[-1]


def check_file(
    file: UploadFile,
):
    chunks = file.filename.split(".")
    if len(chunks) != 2:
        raise ValidateFileException(
            error=f"از ذخیره فایل به علت فرمت نامناسب جلوگیری شد"
        )

    if chunks[1] not in settings.image_allowed_extensions:
        raise ValidateFileException(
            error=f"فرمت فایل ورودی پشتیبانی نمی شود. فرمت های قابل قبول: {', '.join(settings.image_allowed_extensions)}"
        )

    if file.content_type not in settings.image_allowed_content_types:
        raise ValidateFileException(
            error=f"نوع محتوای فایل ورودی پشتیبانی نمی شود. انواع قابل قبول: {', '.join(settings.image_allowed_content_types)}"
        )

    if file.size > settings.image_max_size_in_bytes:
        raise ValidateFileException(
            error=f"حجم فایل ورودی بیشتر از حد مجاز است. حداکثر حجم مجاز: {settings.image_max_size_in_mb} MB"
        )


def construct_path_to_store_files(file_name: str, directories: list[str]):
    directories_path = os.path.join("storage", *directories)
    os.makedirs(directories_path, exist_ok=True)

    current_time = datetime.now()

    new_file_name = f"{current_time.strftime('%Y-%m-%d %H-%M-%S')}_{file_name}"
    return os.path.join(directories_path, new_file_name)
