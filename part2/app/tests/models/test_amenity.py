import pytest
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade


class TestClass():
    """
    Test class for the Amenity model.
    
    This class contains tests to verify that the Amenity model correctly implements:
    - Basic attributes as specified in the class diagram (name, description)
    - Validation for attribute constraints (name required, max length 50)
    - Inherited BaseEntity attributes (id, created_at, updated_at)
    - All required methods (create, update, delete)
    - Data conversion for API responses
    """

    def test_amenity_documentation(self):
        """
        Tests that the Amenity class and its methods have docstrings.
        This ensures that the code is properly documented.
        """
        # Check class docstring
        assert Amenity.__doc__ is not None
        assert len(Amenity.__doc__) > 0

        # Check method docstrings
        assert Amenity.__init__.__doc__ is not None
        assert Amenity.create.__doc__ is not None
        assert Amenity.update.__doc__ is not None
        assert Amenity.delete.__doc__ is not None
        assert Amenity.list_all.__doc__ is not None

    @pytest.fixture
    def valid_amenity(self):
        """
        Creates and returns a valid Amenity instance for testing.
        
        This fixture provides a reusable Amenity object with valid data
        that can be used across different test methods. Using a fixture
        ensures consistency and avoids code duplication.
        
        Returns:
            Amenity: A valid Amenity instance with name "Wi-Fi" and description
        """
        amenity = Amenity("Wi-Fi", "High-speed wireless internet")
        yield amenity  # The yield statement allows pytest to handle cleanup after tests

    @pytest.fixture
    def setup_facade(self, valid_amenity):
        """
        Sets up the Facade with a valid amenity stored in the repository.
        
        This fixture:
        1. Creates a HBnBFacade instance
        2. Adds the valid_amenity to its amenity_repo
        3. Returns the amenity_repo for testing
        
        Args:
            valid_amenity: The Amenity fixture to add to the repository
            
        Returns:
            Repository: The amenity repository from the facade
        """
        facade = HBnBFacade()
        facade.amenity_repo.add(valid_amenity)
        yield facade.amenity_repo

    def test_fixtures_persist(self, setup_facade, valid_amenity):
        """
        Tests that fixtures are properly set up and the repository works.
        
        This test verifies that:
        - The valid_amenity is correctly stored in the repository
        - The repository's get_all() method returns the expected objects
        
        Args:
            setup_facade: The repository fixture
            valid_amenity: The Amenity fixture
        """
        assert setup_facade.get_all() == [valid_amenity]

    def test_amenity_instantiation(self, valid_amenity):
        """
        Tests basic amenity creation with all required attributes.
        
        Verifies that:
        - The Amenity constructor correctly sets name and description
        - The Amenity inherits id, created_at, and updated_at from BaseEntity
        
        Args:
            valid_amenity: The Amenity fixture to test
        """
        amenity = valid_amenity
        # Test that provided attributes are set correctly
        assert amenity.name == "Wi-Fi"
        assert amenity.description == "High-speed wireless internet"

        # Test that BaseEntity attributes are inherited
        assert hasattr(amenity, "id")
        assert hasattr(amenity, "created_at")
        assert hasattr(amenity, "updated_at")

    def test_amenity_name_missing(self):
        """
        Tests that name is required for Amenity creation.
        
        Verifies that:
        - Creating an Amenity with name=None raises ValueError
        - The error message is specific about name being required
        """
        # The with statement captures the exception that should be raised
        with pytest.raises(Exception) as exception:
            amenity = Amenity(name=None, description="Description")

        # Verify that the right type of exception was raised
        assert exception.type == ValueError
        # Verify that the error message is informative
        assert "Amenity name is required" in str(exception.value)

    def test_amenity_name_empty(self):
        """
        Tests that name cannot be an empty string.
        
        Verifies that:
        - Creating an Amenity with name="" raises ValueError
        - The error message is specific about name being required
        """
        with pytest.raises(Exception) as exception:
            amenity = Amenity(name="", description="Description")
        assert exception.type == ValueError
        assert "Amenity name is required" in str(exception.value)

    def test_amenity_name_too_long(self):
        """
        Tests that name cannot exceed 50 characters.
        
        According to the specification, amenity names must have a maximum
        length of 50 characters. This test verifies this constraint.
        """
        with pytest.raises(Exception) as exception:
            # Create a name with 51 'A' characters to exceed the limit
            amenity = Amenity("A" * 51, "Description")
        assert exception.type == ValueError
        assert "Amenity name cannot exceed 50 characters" in str(exception.value)

    def test_amenity_description_optional(self):
        """
        Tests that description is optional.
        
        Verifies that:
        - An Amenity can be created without providing a description
        - The description attribute is set to None in this case
        """
        amenity = Amenity("Pool")
        assert amenity.name == "Pool"
        assert amenity.description is None

    def test_amenity_update(self, valid_amenity):
        """
        Tests updating amenity attributes.
        
        Verifies that:
        - The update method correctly changes name and description
        - The updated_at timestamp is updated after calling update
        
        Args:
            valid_amenity: The Amenity fixture to test
        """
        amenity = valid_amenity
        # Save the original updated_at value to compare later
        original_updated_at = amenity.updated_at

        # Update the amenity with new values
        amenity.update({
            "name": "High-Speed Wi-Fi",
            "description": "5G wireless internet"
        })

        # Check that attributes were updated correctly
        assert amenity.name == "High-Speed Wi-Fi"
        assert amenity.description == "5G wireless internet"
        # Check that the updated_at timestamp was updated
        assert amenity.updated_at > original_updated_at

    def test_amenity_to_dict(self, valid_amenity):
        """
        Tests conversion to dictionary for API responses.
        
        Verifies that the to_dict method properly serializes the Amenity
        with all required fields for API responses.
        
        Args:
            valid_amenity: The Amenity fixture to test
        """
        amenity = valid_amenity
        amenity_dict = amenity.to_dict()

        # Check that dictionary contains all required fields
        assert amenity_dict["id"] == amenity.id
        assert amenity_dict["name"] == "Wi-Fi"
        assert amenity_dict["description"] == "High-speed wireless internet"
        assert "created_at" in amenity_dict
        assert "updated_at" in amenity_dict
        assert "__class__" in amenity_dict
        assert amenity_dict["__class__"] == "Amenity"

    def test_amenity_creation_method(self, valid_amenity):
        """
        Tests the create() method.
        
        Verifies that:
        - The create() method returns the amenity instance
        - This matches the create() method in the class diagram
        
        Args:
            valid_amenity: The Amenity fixture to test
        """
        amenity = valid_amenity
        result = amenity.create()

        # The create() method should return the amenity instance
        assert result == amenity

    def test_amenity_list_all_method(self):
        """
        Tests the list_all() class method.
        
        Verifies that:
        - The list_all() method can be called as a class method
        - It returns a list (which would contain all amenities in a real implementation)
        - This matches the list_all() method in the class diagram
        """
    # Call the class method
        result = Amenity.list_all()

    # Check that it returns a list (even if empty in testing)
        assert isinstance(result, list)

    def test_amenity_delete_method(self, valid_amenity):
        """
        Tests the delete() method.
        
        Verifies that:
        - The delete() method returns True for success
        - This matches the delete() method in the class diagram
        
        Args:
            valid_amenity: The Amenity fixture to test
        """
        amenity = valid_amenity
        result = amenity.delete()

        # The delete() method should return True for success
        assert result is True

    def test_amenity_name_wrong_type(self):
        """
        Tests that providing a non-string value for name raises an error.
        This ensures type validation is working correctly.
        """
        with pytest.raises(Exception) as exception:
            amenity = Amenity(name=123, description="Description")  # Number instead of string
        # The exact error message may vary based on your implementation
        assert exception.type in [ValueError, TypeError]

    def test_amenity_update_with_invalid_data(self, valid_amenity):
        """
        Tests how the update method handles invalid data.
        This ensures that validation still occurs during updates.
        """
        amenity = valid_amenity
        
        # Try to update with invalid name (too long)
        with pytest.raises(Exception) as exception:
            amenity.update({"name": "A" * 51})
        assert "cannot exceed 50 characters" in str(exception.value)
        
        # Verify the original name is unchanged
        assert amenity.name == "Wi-Fi"

    def test_amenity_non_existent_attribute(self, valid_amenity):
        """
        Tests updating a non-existent attribute.
        This ensures the update method only updates valid attributes.
        """
        amenity = valid_amenity
        
        # Try to update with a non-existent attribute
        amenity.update({"nonexistent_field": "Some value"})
        
        # Verify the attribute wasn't added
        assert not hasattr(amenity, "nonexistent_field")