from enum import Enum
from typing import Annotated, TypeAlias, Union
from datetime import datetime
from pydantic import BaseModel, Field


class Type(str, Enum):
    text = "text"
    url = "link"


TypeField: TypeAlias = Annotated[Type, Field(description="The type of resource")]


class Resource(BaseModel):
    id: Annotated[
        str,
        Field(
            description="The unique identifier for the text snippet/link, also used as they key in the database. Vanity URL if user chooses to use one",
            examples=["exam-solutions", "x19Kq%p", "important-papers"],
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
    type: Annotated[
        TypeField,
        Field(description="The type of the resource", examples=["text", "link"]),
    ]
    expiration_time: Annotated[
        Union[int, datetime, None],
        Field(
            description="The date and time when the resource will expire, specified by the user. Can be in datetime format, or an integer for the number of hours the resource should last.",
            examples=["2025-10-01T00:00:00", 24, -1],
        ),
    ] = (
        -1
    )  # -1 respresent default no expiration time, allowing the expiration_time field to show up in the request body in the docs. Setting the value to None prevents the field from showing up in the request body in the docs.
    access_count: Annotated[
        int, Field(description="The number of times the resource has been accessed")
    ] = 0
