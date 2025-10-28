"""Database module for in-memory product storage."""
from typing import List, Optional
from datetime import datetime

from models import Product, ProductCreate, ProductUpdate, User, UserCreate, UserUpdate, Setting, SettingCreate, SettingUpdate


class InMemoryDatabase:
    """In-memory database for storing and managing products."""

    def __init__(self):
        self.products: List[Product] = []
        self.users: List[User] = []
        self.settings: List[Setting] = []
        self.next_id = 1
        self.next_user_id = 1
        self.next_setting_id = 1
        self._init_sample_data()

    def _init_sample_data(self):
        """Initialize the database with sample product data."""
        sample_products = [
            ProductCreate(
                name="Wireless Headphones",
                description="High-quality wireless headphones with noise cancellation",
                price=199.99,
                category="Electronics",
                tags=["audio", "wireless", "premium"]
            ),
            ProductCreate(
                name="Coffee Maker",
                description="Programmable coffee maker with built-in grinder",
                price=89.99,
                category="Appliances",
                tags=["kitchen", "coffee", "automatic"]
            ),
            ProductCreate(
                name="Laptop Stand",
                description="Adjustable aluminum laptop stand for ergonomic work",
                price=45.99,
                category="Accessories",
                tags=["ergonomic", "aluminum", "adjustable"]
            )
        ]

        for product_data in sample_products:
            self.create_product(product_data)

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product in the database."""
        product = Product(
            id=self.next_id,
            **product_data.dict(),
            created_at=datetime.now()
        )
        self.products.append(product)
        self.next_id += 1
        return product

    def get_all_products(self) -> List[Product]:
        """Get all products from the database."""
        return self.products

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a specific product by ID."""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def update_product(self, product_id: int, update_data: ProductUpdate) -> Optional[Product]:
        """Update an existing product in the database."""
        product = self.get_product(product_id)
        if not product:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(product, field, value)

        return product

    def delete_product(self, product_id: int) -> bool:
        """Delete a product from the database."""
        for i, product in enumerate(self.products):
            if product.id == product_id:
                del self.products[i]
                return True
        return False

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user in the database."""
        user = User(
            id=self.next_user_id,
            **user_data.dict(),
            created_at=datetime.now()
        )
        self.users.append(user)
        self.next_user_id += 1
        return user

    def get_all_users(self) -> List[User]:
        """Get all users from the database."""
        return self.users

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a specific user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def update_user(self, user_id: int, update_data: UserUpdate) -> Optional[User]:
        """Update an existing user in the database."""
        user = self.get_user(user_id)
        if not user:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(user, field, value)

        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database."""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                return True
        return False

    def create_setting(self, setting_data: SettingCreate) -> Setting:
        """Create a new setting in the database."""
        setting = Setting(
            id=self.next_setting_id,
            **setting_data.dict(),
            created_at=datetime.now()
        )
        self.settings.append(setting)
        self.next_setting_id += 1
        return setting

    def get_all_settings(self) -> List[Setting]:
        """Get all settings from the database."""
        return self.settings

    def get_setting(self, setting_id: int) -> Optional[Setting]:
        """Get a specific setting by ID."""
        for setting in self.settings:
            if setting.id == setting_id:
                return setting
        return None

    def get_setting_by_key(self, key: str) -> Optional[Setting]:
        """Get a specific setting by key."""
        for setting in self.settings:
            if setting.key == key:
                return setting
        return None

    def update_setting(self, setting_id: int, update_data: SettingUpdate) -> Optional[Setting]:
        """Update an existing setting in the database."""
        setting = self.get_setting(setting_id)
        if not setting:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(setting, field, value)

        return setting

    def delete_setting(self, setting_id: int) -> bool:
        """Delete a setting from the database."""
        for i, setting in enumerate(self.settings):
            if setting.id == setting_id:
                del self.settings[i]
                return True
        return False


# Global database instance
db = InMemoryDatabase()
