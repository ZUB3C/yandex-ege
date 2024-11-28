import re

auth_cookies = {}
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://education.yandex.ru",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}
TIMEOUT = 10
YANDEX_EDUCATION_DOMAIN = "education.yandex.ru"
UUID_REGEX = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"
COLLECTIONS_PATTERN = re.compile(r"^/ege/collections/(?P<uuid>(" + UUID_REGEX + r"))(/task/\d+)")
TASK_PATTERN = re.compile(r"^/ege/task/(?P<uuid>(" + UUID_REGEX + "))")
