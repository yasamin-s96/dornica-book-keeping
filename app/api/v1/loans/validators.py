from datetime import datetime
from core.exception import UnprocessableEntity


def iso_date(str_date):
    try:
        return datetime.strptime(str_date, "%Y-%m-%d").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(str_date, "%Y/%m/%d").date()
    except ValueError:
        pass

    raise UnprocessableEntity(
        error=f"تاریخ باید به صورت yyyy/mm/dd یا yyyy-mm-dd وارد شود و معتبر باشد"
    )
