"""Pydantic models for product data structures."""
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    """Product model with all fields."""
    id: int
    name: str
    description: str
    price: float
    category: str
    tags: List[str] = []
    in_stock: bool = True
    created_at: datetime = datetime.now()


class ProductCreate(BaseModel):
    """Model for creating a new product."""
    name: str
    description: str
    price: float
    category: str
    tags: List[str] = []
    in_stock: bool = True


class ProductUpdate(BaseModel):
    """Model for updating an existing product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None


class User(BaseModel):
    """User model with all fields."""
    id: int
    name: str
    email: str
    password: str
    created_at: datetime = datetime.now()

class UserCreate(BaseModel):
    """Model for creating a new user."""
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class Setting(BaseModel):
    """Setting model with all fields."""
    id: int
    key: str
    value: str
    description: Optional[str] = None
    created_at: datetime = datetime.now()


class SettingCreate(BaseModel):
    """Model for creating a new setting."""
    key: str
    value: str
    description: Optional[str] = None


class SettingUpdate(BaseModel):
    """Model for updating an existing setting."""
    value: Optional[str] = None
    description: Optional[str] = None