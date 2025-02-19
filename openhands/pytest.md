---
name: tests
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- pytest
- tests
- test
---

Here are the best practices for writing tests in this repository:

1. Test Structure and Organization:
   - Use Django's TestCase for most tests
   - Organize tests by app/module in a `tests` directory
   - Use descriptive test class and method names
   - Group related tests in test classes
   - Use `setUp` method for common test initialization

2. Test Writing Guidelines:
   ```python
   class MyFeatureTests(TestCase):
       def setUp(self):
           # Common setup for all tests
           self.client = Client()
           # Use factories instead of direct model creation
           self.user = UserFactory()
   
       def test_specific_feature(self):
           """Clear docstring explaining test purpose"""
           # Arrange
           expected_result = ...
           
           # Act
           result = self.client.get(reverse('my-view'))
           
           # Assert
           self.assertEqual(result.status_code, 200)
   ```

3. Key Principles:
   - Don't change settings when making tests pass
   - Note if implementation is incorrect (tests caught a bug)
   - Use Factories instead of fixtures (most factories already exist)
   - Test migrations locally before pushing:
     ```bash
     python manage.py migrate app_name 0004_previous  # Test rollback
     python manage.py migrate app_name               # Test forward
     ```

4. Test Coverage:
   - Run tests with coverage: `pytest --cov-config=.coveragerc --durations=10 -vvv`
   - Test specific files: `pytest tests/test_specific.py -v`
   - Test specific classes: `pytest tests/test_file.py::TestClass -v`
   - Test specific methods: `pytest tests/test_file.py::TestClass::test_method -v`

5. Test Cases to Include:
   - Happy path (expected behavior)
   - Edge cases and boundary conditions
   - Error cases and invalid inputs
   - Permission and authorization tests
   - API response format tests
   - Database interaction tests

6. Best Practices:
   - Use `subTest` for multiple test cases within a single test
   - Write clear test docstrings explaining purpose
   - Follow AAA pattern (Arrange, Act, Assert)
   - Use meaningful test data
   - Keep tests independent and isolated
   - Clean up test data after tests
   - Use appropriate assertions (e.g., `assertEqual`, `assertIn`, `assertRaises`)

7. Factory Usage:
   - Reuse factories as much as possible
   - If you want a specific feature/attribute set, you can create a subfactory with that name (ie. ArchivedFileRecord) so that it can be re-used later.
   - Always check for existing factories
   ```python
   from factory import Factory, Faker
   
   class UserFactory(Factory):
       class Meta:
           model = User
       
       username = Faker('user_name')
       email = Faker('email')
   ```

9. API Testing:
   ```python
   class APITests(TestCase):
       def test_api_endpoint(self):
           response = self.client.get(reverse('api-endpoint'))
           self.assertEqual(response.status_code, 200)
           self.assertIn('expected_key', response.json())
   ```

10. Database Testing:
   - Use transactions for test isolation
   - Test database constraints
   - Test model methods and properties
   - Verify database state after operations
   - Use Postgres. You should not need to change any database settings.

11. Mocking and Patches:
    ```python
    from unittest.mock import patch
    
    class ServiceTests(TestCase):
        @patch('module.external_service')
        def test_service_call(self, mock_service):
            mock_service.return_value = expected_result
            result = function_under_test()
            self.assertEqual(result, expected_result)
    ```


