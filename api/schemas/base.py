import re

from datetime import datetime

from enum import Enum

from typing import (
    List,
    Optional,
)

from fastapi import HTTPException

from pydantic import (
    BaseModel,
    EmailStr,
    validator,
)