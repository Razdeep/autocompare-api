from pydantic import BaseModel

class GenericResponse:
    data: object
    message: str