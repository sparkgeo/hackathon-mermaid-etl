import re
from datetime import datetime


def convert(input: str):
    return datetime.fromisoformat(re.sub("Z$", "", input))
