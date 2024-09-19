from .base import AuthenticationFailedException


class EmailNotVerifiedException(AuthenticationFailedException):
    error = {
        "email_unverified": [
            "ایمیل شما تایید نشده است، جهت تایید به صندوق ورودی آدرس ایمیل خود مراجعه کنید."
        ]
    }
