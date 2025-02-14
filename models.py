from enum import Enum
from typing import Annotated, TypeAlias
from datetime import datetime
from pydantic import BaseModel, Field


class User:
    id: int


class Resource(BaseModel):
    id: Annotated[
        int,
        Field(
            description="The unique identifier for the text snippet/link",
            examples=[1, 2, 24],
        ),
    ]
    content: Annotated[
        str,
        Field(
            description="The text snippet content or original target link",
            examples=[
                "Hello World!",
                "https://www.google.com/QWLJdhwjdHQLJDWQHLJdaHSJifadhofiewhiofelfdh",
            ],
        ),
    ]
    vanity_url: Annotated[
        str | None,
        Field(
            description="The vanity path URL for the text snippet",
            examples=["exam-solutions", "important-papers"],
        ),
    ] = None
    custom_url: Annotated[
        str | None,
        Field(
            description="The custom URL generated for the original content submitted",
            examples=[
                "www.pastebin.com/exam-solutions",
                "www.pastebin.com/x19Kq%p",
                "short.url/important-papers",
            ],
        ),
    ] = None
    type: Annotated[
        str, Field(description="The type of the resource", examples=["text", "link"])
    ]
    expiration_time: Annotated[
        datetime | None,
        Field(
            description="The date and time when the resource will expire, specified by the user.",
            examples=[datetime.now()],
        ),
    ] = None
    access_count: Annotated[
        int, Field(description="The number of times the resource has been accessed")
    ] = 0
