from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserProfileUpdateReq(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None
