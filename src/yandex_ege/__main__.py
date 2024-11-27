from datetime import datetime
from typing import Annotated, Any, AnyStr
from uuid import UUID

import msgspec.json
import requests
import typer
from yarl import URL

from .const import (
    COLLECTIONS_PATTERN,
    DEFAULT_HEADERS,
    TASK_PATTERN,
    TIMEOUT,
    YANDEX_EDUCATION_DOMAIN,
    auth_cookies,
)
from .models import Task, Variant


def get_crsf_token() -> str:
    data = requests.get(
        "https://education.yandex.ru/api/v5/get-csrf-token", timeout=TIMEOUT
    ).json()
    return data["sk"].split(":")[0]


app = typer.Typer()
DEFAULT_HEADERS["x-csrf-token"] = get_crsf_token()
ANONYMOUS_SESSION = requests.session()
ANONYMOUS_SESSION.headers.update(DEFAULT_HEADERS)


def get_variant(variant_id: UUID) -> Variant:
    payload = [
        {
            "type": "public_get_variant_request_item",
            "variant_id": str(variant_id),
        },
    ]
    response = ANONYMOUS_SESSION.post(
        "https://education.yandex.ru/api/v5/gpttr", json=payload, timeout=TIMEOUT
    )
    return msgspec.json.decode(response.text, type=Variant)


def get_task(task_id: UUID) -> Task:
    json_data = [
        {
            "type": "get_task_by_id",
            "task_id": str(task_id),
        }
    ]

    response = ANONYMOUS_SESSION.post(
        "https://education.yandex.ru/api/v5/gpttr",
        cookies={},
        json=json_data,
        timeout=TIMEOUT,
    )
    return msgspec.json.decode(response.text, type=Task)


def get_task_answer(task: Task) -> str | int | float | list[list[str]] | list[list[int]]:
    return task.markup.answer_control_layout[0].content.correct_answers


def submit_variant_answers(
    variant_id: str,
    tasks_data: list[tuple[str, AnyStr]],
    date_started: datetime | None = None,
    date_finished: datetime | None = None,
) -> dict[str, Any]:
    if not date_finished:
        date_finished = datetime.now()

    date_started_str = date_started.strftime("%Y-%m-%dT%H:%M:%S.000Z") if date_started else None
    date_finished_str = date_finished.strftime("%Y-%m-%dT%H:%M:%S.000Z") if date_finished else None
    json_data = [
        {
            "type": "make_variant_attempt_request",
            "variantId": variant_id,
            "dateStarted": date_started_str,
            "dateFinished": date_finished_str,
            "taskAttempts": [
                {
                    "taskId": task_id,
                    "userAttempt": answer,
                    "solution": "",
                }
                for task_id, answer in tasks_data
            ],
        },
    ]

    response = ANONYMOUS_SESSION.post(
        "https://education.yandex.ru/api/v5/gpttr",
        cookies=auth_cookies,
        json=json_data,
        timeout=TIMEOUT,
    )
    return response.json()


@app.command()
def main(urls: Annotated[list[str], typer.Argument(help="Collection and/or task urls.")]):
    urls: list[URL] = list(map(URL, urls))
    print("Ответы на задания и варианты:")
    for i, url in enumerate(urls):
        if url.host != YANDEX_EDUCATION_DOMAIN:
            print(f"Invalid domain for url {url!s}, skipping it.\n")
            continue
        collection_match = COLLECTIONS_PATTERN.match(url.path)
        if collection_match:
            collection_uuid = UUID(collection_match.group("uuid"))
            variant = get_variant(collection_uuid)
            print(f"{variant.title} (https://education.yandex.ru/ege/collections/{variant.id}/task/1)")
            for i, task in enumerate(variant.tasks, start=1):
                correct_answers = get_task_answer(task)
                print(f"{i}. {correct_answers}")
            if i != len(urls) - 1:
                print()
        else:
            task_match = TASK_PATTERN.match(url.path)
            if task_match:
                task_uuid = UUID(task_match.group("uuid"))
                task = get_task(task_uuid)
                print(
                    f"{task.category_title}: {get_task_answer(task)} (задание {task.number}, https://education.yandex.ru/ege/task/{task_uuid})"
                )
            if i != len(urls) - 1:
                print()
