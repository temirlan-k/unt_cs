from pydantic import BaseModel




class UserCreateReq(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserLoginReq(BaseModel):
    email: str
    password: str
