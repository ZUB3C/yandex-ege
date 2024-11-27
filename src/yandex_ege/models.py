from typing import Any
from uuid import UUID

from msgspec import Struct


class AnswerControlLayoutContent(Struct):
    correct_answers: str | Any
    id: int
    type: str


class AnswerControlLayout(Struct):
    kind: str
    content: AnswerControlLayoutContent


class MarkupLayoutContent(Struct):
    text: str


class MarkupLayout(Struct):
    kind: str
    content: MarkupLayoutContent


class Markup(Struct):
    answer_control_layout: list[AnswerControlLayout]
    layout: list[MarkupLayout]
    resources: list[Any]
    solution: str
    tools: list[Any]


class Theory(Struct):
    content: str | None
    link: str | None
    title: str


class Task(Struct):
    category_title: str
    difficulty_level: int
    id: UUID
    is_dialog_possible: bool
    markup: Markup
    theory: list[Theory] | None
    number: int
    outdated: bool
    task_source_link: str | None
    task_source_title: str
    tested_skill: str
    year: int


class TaskInfo(Struct):
    category_title: str
    difficulty_level: int
    number: int
    outdated: bool
    tested_skill: str
    theory: list[Theory] | None
    year: int


class Settings(Struct):
    ai_support: bool


class Variant(Struct):
    created_by: str
    exam_id: UUID
    explanation_link: str | None
    id: UUID
    is_correct_ege_variant: bool
    number: int
    outdated: bool
    release_date: str
    relevant: bool
    settings: Settings
    release_date: str
    tasks: list[Task]
    tasks_info: dict[UUID, TaskInfo]
    title: str
    type: str
