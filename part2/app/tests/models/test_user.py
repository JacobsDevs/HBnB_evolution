from email_validator import EmailNotValidError
import pytest
from app.models.user import User
from app.services.facade import HBnBFacade

class TestClass():
    """Pytest fixtures can be used as below to setup things for testing.
    Keep in mind they don't persist outside their function as far as I can tell
    so you will need to define everything that you want to persist inside the
    fixture.
    """

    @pytest.fixture
    def valid_user(self):
        """
        This will always contain this valid user
        """
        user = User("John", "Smith", "john@smith.com", "password1!")
        yield user
        user.delete_from_database()

    @pytest.fixture
    def setup_facade(self, valid_user):
        """
        This will always contain a facade user_repo object with the valid user.
        """
        facade = HBnBFacade()
        facade.user_repo.add(valid_user)
        yield facade.user_repo

    def testFixturesPersist(self, setup_facade, valid_user):
        """
        You pass fixtures into test like this This tests that the valid_user
        object is stored in the facade's user_repo.
        """
        assert setup_facade.get_all() == [valid_user]

    def testUserInstantiation(self, valid_user):
        user = valid_user
        assert user.first_name == "John"
        assert user.last_name == "Smith"
        assert user.email == "john@smith.com"
        assert user.password == "password1!"
        assert user.is_admin == False

    def testUserFirstNameMissing(self):
        """Required"""
        with pytest.raises(Exception) as exception:
            user = User(last_name="Smith", email="john@smith.com", password="password", is_admin=True)
        assert exception.type == ValueError
        assert "First name is required" in str(exception.value)

    def testUserFirstNameTooLong(self):
        """Maximum length of 50 characters."""
        with pytest.raises(Exception) as exception:
            user = User("J" * 51, "Smith", "john@smith.com", "password", True)
        assert exception.type == ValueError
        assert "First name must be less than 50 characters" in str(exception.value)

    def testUserLastNameMissing(self):
        """Required"""
        with pytest.raises(Exception) as exception:
            user = User(first_name="John", email="john@smith.com", password="password", is_admin=True)
        assert exception.type == ValueError
        assert "Last name is required" in str(exception.value)

    def testUserLastNameTooLong(self):
        """Required, maximum length of 50 characters."""
        with pytest.raises(Exception) as exception:
            user = User("John", "S" * 51, "john@smith.com", "password", True)
        assert exception.type == ValueError
        assert "Last name must be less than 50 characters" in str(exception.value)

    def testUserEmailMissing(self):
        """Required"""
        with pytest.raises(Exception) as exception:
            user = User(first_name="John", last_name="Smith", password="password", is_admin=True)
        assert exception.type == ValueError
        assert "Email is required" in str(exception.value)

    def testUserEmailInvalid(self):
        """Required, maximum length of 50 characters."""
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "invalid", "password", True)
        assert exception.type == EmailNotValidError
        assert "Email is not valid" in str(exception.value)

    def testUserEmailIsUnique(self, setup_facade, valid_user):
        """Email must not already be registered to a user"""
        with pytest.raises(Exception) as exception:
            User("Jack", "Smith", "john@smith.com", "ABCD1234!!")
            User("Jack", "Smith", "john@smith.com", "ABCD1234!!")
        assert exception.type == ValueError
        assert "Email is not unique" in str(exception.value)


    def testUserPasswordShort(self):
        """Password must be 8 characters minimum"""
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "john@smith.com", "weak", True)
        assert exception.type == ValueError
        assert "Password must be at least 8 characters" in str(exception.value)

    def testUserPasswordNoDigits(self):
        """Password requires 1 digit"""
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "john@smith.com", "abcdefgh", True)
        assert exception.type == ValueError
        assert "Password is missing a digit" in str(exception.value)

    def testUserPasswordNoLetters(self):
        """Password requires 1 letter"""
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "john@smith.com", "12345678", True)
        assert exception.type == ValueError
        assert "Password is missing a letter" in str(exception.value)

    def testUserPasswordNoSpecialCharacters(self):
        """Password requires 1 special character"""
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "john@smith.com", "abcdabcd123", True)
        assert exception.type == ValueError
        assert "Password is missing a special character" in str(exception.value)
