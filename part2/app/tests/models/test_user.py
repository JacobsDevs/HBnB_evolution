import pytest
import sys
sys.path.append('../../../')
from app.models.user import User

class TestClass():

    def testUserInstantiation(self):
        user = User("John", "Smith", "john@smith.com", "password", True)
        assert user.first_name == "John"
        assert user.last_name == "Smith"
        assert user.email == "john@smith.com"
        assert user.password == "password"
        assert user.is_admin == True

    def testUserPasswordValidation(self):
        with pytest.raises(Exception) as exception:
            user = User("John", "Smith", "john@smith.com", "weak", True)

