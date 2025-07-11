from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime




class UserCreate(BaseModel):
    name: str
    email_id: str
    phone_number: str
    password: str
    is_admin: bool = False

class UserAddressUpdate(BaseModel):
    addresses: List[str]

class CartItemRequest(BaseModel):
    user_id: int
    menu_id: int
    quantity: int



class AddressItem(BaseModel):
    address: str
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    is_default: Optional[bool] = False

class UserAddressUpdate(BaseModel):
    addresses: List[AddressItem]



class OrderRequest(BaseModel):
    user_id: int
    status: str = "PLACED"
    delivery_time: Optional[datetime] = None
    comments: Optional[str] = None
    discount_name: Optional[str] = None
    discount: Optional[float] = 0.0
    payment_method: Optional[str] = None
    payment_made: Optional[bool] = False
    transaction_id: Optional[str] = None


 
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    user_id: Optional[int] = None