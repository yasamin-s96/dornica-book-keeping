import random
import string


def generate_verification_code():
    code = "".join(random.choice(string.digits) for _ in range(5))
    return code
