from pydantic import BaseModel
from typing import Union, List


class InferenceRequest(BaseModel):
    data: Union[str, List[str]]