from pydantic import BaseModel, Field

class UserCreateSchema(BaseModel):
    """Schema used to validate data when registering a new supermarket employee."""
    user_name: str = Field(..., max_length=250)
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    first_name: str = Field(..., max_length=250)
    last_name: str = Field(..., max_length=250)
    role_id: int = Field(..., description="1 for Admin, 2 for Cashier")

class UserLoginSchema(BaseModel):
    """Schema used to validate a login request."""
    user_name: str
    password: str
