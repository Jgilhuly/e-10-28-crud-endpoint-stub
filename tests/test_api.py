"""Unit tests for FastAPI endpoints."""
import pytest
from models import ProductCreate, UserCreate


class TestHealthAndRoot:
    """Tests for health check and root endpoints."""

    def test_root_endpoint(self, client):
        """Test GET / returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Product CRUD API"}

    def test_health_check(self, client):
        """Test GET /health returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestProductEndpoints:
    """Tests for product CRUD endpoints."""

    def test_get_all_products(self, client):
        """Test GET /products returns list of products."""
        response = client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) == 3  # Sample data includes 3 products

    def test_get_all_products_have_required_fields(self, client):
        """Test product objects have all required fields."""
        response = client.get("/products")
        products = response.json()
        assert len(products) > 0
        
        for product in products:
            assert "id" in product
            assert "name" in product
            assert "description" in product
            assert "price" in product
            assert "category" in product
            assert "tags" in product
            assert "in_stock" in product
            assert "created_at" in product

    def test_get_product_by_id(self, client):
        """Test GET /products/{id} returns specific product."""
        response = client.get("/products/1")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        assert product["name"] == "Wireless Headphones"

    def test_get_product_not_found(self, client):
        """Test GET /products/{id} returns 404 for non-existent product."""
        response = client.get("/products/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}

    def test_create_product(self, client):
        """Test POST /products creates a new product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 29.99,
            "category": "Test",
            "tags": ["test"],
            "in_stock": True
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == 200
        
        product = response.json()
        assert product["name"] == "Test Product"
        assert product["price"] == 29.99
        assert product["id"] is not None

    def test_create_product_minimal(self, client):
        """Test POST /products with minimal required fields."""
        product_data = {
            "name": "Minimal Product",
            "description": "Minimal",
            "price": 10.0,
            "category": "Test"
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == 200
        product = response.json()
        assert product["tags"] == []
        assert product["in_stock"] is True

    def test_update_product(self, client):
        """Test PUT /products/{id} updates a product."""
        update_data = {
            "price": 249.99,
            "in_stock": False
        }
        response = client.put("/products/1", json=update_data)
        assert response.status_code == 200
        
        product = response.json()
        assert product["id"] == 1
        assert product["price"] == 249.99
        assert product["in_stock"] is False
        # Name should remain unchanged
        assert product["name"] == "Wireless Headphones"

    def test_update_product_not_found(self, client):
        """Test PUT /products/{id} returns 404 for non-existent product."""
        update_data = {"price": 99.99}
        response = client.put("/products/999", json=update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}

    def test_delete_product(self, client):
        """Test DELETE /products/{id} removes a product."""
        # Delete product
        response = client.delete("/products/1")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get("/products/1")
        assert response.status_code == 404

    def test_delete_product_not_found(self, client):
        """Test DELETE /products/{id} returns 404 for non-existent product."""
        response = client.delete("/products/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}

    def test_delete_product_reduces_count(self, client):
        """Test that deleting a product reduces the total count."""
        # Get initial count
        response = client.get("/products")
        initial_count = len(response.json())

        # Delete a product
        client.delete("/products/1")

        # Check new count
        response = client.get("/products")
        new_count = len(response.json())
        assert new_count == initial_count - 1


class TestUserEndpoints:
    """Tests for user CRUD endpoints."""

    def test_get_all_users(self, client):
        """Test GET /users returns list of users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)

    def test_get_all_users_have_required_fields(self, client):
        """Test user objects have all required fields."""
        response = client.get("/users")
        users = response.json()
        
        for user in users:
            assert "id" in user
            assert "name" in user
            assert "email" in user
            assert "password" in user
            assert "created_at" in user

    def test_create_user(self, client):
        """Test POST /users creates a new user."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secure_password"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        user = response.json()
        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
        assert user["id"] is not None

    def test_get_user_by_id(self, client):
        """Test GET /users/{id} returns specific user."""
        # Create a user first
        user_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "pass123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == "Jane Smith"

    def test_get_user_not_found(self, client):
        """Test GET /users/{id} returns 404 for non-existent user."""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_update_user(self, client):
        """Test PUT /users/{id} updates a user."""
        # Create a user
        user_data = {
            "name": "Original Name",
            "email": "original@example.com",
            "password": "pass123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Update the user
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        user = response.json()
        assert user["name"] == "Updated Name"
        assert user["email"] == "updated@example.com"

    def test_update_user_not_found(self, client):
        """Test PUT /users/{id} returns 404 for non-existent user."""
        update_data = {"name": "New Name"}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_delete_user(self, client):
        """Test DELETE /users/{id} removes a user."""
        # Create a user
        user_data = {
            "name": "Delete Me",
            "email": "delete@example.com",
            "password": "pass123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404

    def test_delete_user_not_found(self, client):
        """Test DELETE /users/{id} returns 404 for non-existent user."""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_delete_user_reduces_count(self, client):
        """Test that deleting a user reduces the total count."""
        # Create a user
        user_data = {
            "name": "Count Test",
            "email": "count@example.com",
            "password": "pass123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Get initial count
        response = client.get("/users")
        initial_count = len(response.json())

        # Delete the user
        client.delete(f"/users/{user_id}")

        # Check new count
        response = client.get("/users")
        new_count = len(response.json())
        assert new_count == initial_count - 1


class TestSettingEndpoints:
    """Tests for setting CRUD endpoints."""

    def test_get_all_settings(self, client):
        """Test GET /settings returns list of settings."""
        response = client.get("/settings")
        assert response.status_code == 200
        settings = response.json()
        assert isinstance(settings, list)

    def test_get_all_settings_have_required_fields(self, client):
        """Test setting objects have all required fields."""
        response = client.get("/settings")
        settings = response.json()
        
        for setting in settings:
            assert "id" in setting
            assert "key" in setting
            assert "value" in setting
            assert "created_at" in setting

    def test_create_setting(self, client):
        """Test POST /settings creates a new setting."""
        setting_data = {
            "key": "app_theme",
            "value": "dark",
            "description": "Application theme preference"
        }
        response = client.post("/settings", json=setting_data)
        assert response.status_code == 200
        
        setting = response.json()
        assert setting["key"] == "app_theme"
        assert setting["value"] == "dark"
        assert setting["description"] == "Application theme preference"
        assert setting["id"] is not None

    def test_create_setting_minimal(self, client):
        """Test POST /settings with minimal required fields."""
        setting_data = {
            "key": "debug_mode",
            "value": "false"
        }
        response = client.post("/settings", json=setting_data)
        assert response.status_code == 200
        setting = response.json()
        assert setting["key"] == "debug_mode"
        assert setting["value"] == "false"

    def test_get_setting_by_id(self, client):
        """Test GET /settings/{id} returns specific setting."""
        # Create a setting first
        setting_data = {
            "key": "max_users",
            "value": "100",
            "description": "Maximum number of users"
        }
        create_response = client.post("/settings", json=setting_data)
        setting_id = create_response.json()["id"]

        # Get the setting
        response = client.get(f"/settings/{setting_id}")
        assert response.status_code == 200
        setting = response.json()
        assert setting["id"] == setting_id
        assert setting["key"] == "max_users"
        assert setting["value"] == "100"

    def test_get_setting_not_found(self, client):
        """Test GET /settings/{id} returns 404 for non-existent setting."""
        response = client.get("/settings/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Setting not found"}

    def test_update_setting(self, client):
        """Test PUT /settings/{id} updates a setting."""
        # Create a setting
        setting_data = {
            "key": "api_timeout",
            "value": "30",
            "description": "API timeout in seconds"
        }
        create_response = client.post("/settings", json=setting_data)
        setting_id = create_response.json()["id"]

        # Update the setting
        update_data = {
            "value": "60",
            "description": "API timeout in seconds (updated)"
        }
        response = client.put(f"/settings/{setting_id}", json=update_data)
        assert response.status_code == 200
        
        setting = response.json()
        assert setting["value"] == "60"
        assert setting["description"] == "API timeout in seconds (updated)"
        # Key should remain unchanged
        assert setting["key"] == "api_timeout"

    def test_update_setting_not_found(self, client):
        """Test PUT /settings/{id} returns 404 for non-existent setting."""
        update_data = {"value": "new_value"}
        response = client.put("/settings/999", json=update_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Setting not found"}

    def test_delete_setting(self, client):
        """Test DELETE /settings/{id} removes a setting."""
        # Create a setting
        setting_data = {
            "key": "temp_setting",
            "value": "temporary"
        }
        create_response = client.post("/settings", json=setting_data)
        setting_id = create_response.json()["id"]

        # Delete the setting
        response = client.delete(f"/settings/{setting_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f"/settings/{setting_id}")
        assert response.status_code == 404

    def test_delete_setting_not_found(self, client):
        """Test DELETE /settings/{id} returns 404 for non-existent setting."""
        response = client.delete("/settings/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Setting not found"}

    def test_delete_setting_reduces_count(self, client):
        """Test that deleting a setting reduces the total count."""
        # Create a setting
        setting_data = {
            "key": "count_test",
            "value": "test_value"
        }
        create_response = client.post("/settings", json=setting_data)
        setting_id = create_response.json()["id"]

        # Get initial count
        response = client.get("/settings")
        initial_count = len(response.json())

        # Delete the setting
        client.delete(f"/settings/{setting_id}")

        # Check new count
        response = client.get("/settings")
        new_count = len(response.json())
        assert new_count == initial_count - 1
