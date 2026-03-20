from pydantic import BaseModel, EmailStr

class UserRegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attributes = True
