---
name: lint
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- lint
- black
- pr
- push
---

Before pushing to any remote location please run linting.

Here are the linting best practices for this project:

1. Code Formatting with Black:
   - The project uses `black` as the primary code formatter
   - Must be run on ALL files before committing
   - Do NOT use flake8 (explicitly mentioned in instructions)

   ```bash
   # Format all Python files
   black .
   
   # Format specific file or directory
   black path/to/file_or_dir
   ```

2. Black Configuration:
   - Default line length (88 characters)
   - Double quotes for strings
   - No manual line breaks inside parentheses/brackets
   - Trailing commas in multi-line structures

   Example of Black-compliant code:
   ```python
   def example_function(
       long_parameter_name: str,
       another_parameter: int,
       optional_param: bool = False,
   ) -> Dict[str, Any]:
       return {
           "key": "value",
           "long_key": [
               "item1",
               "item2",
               "item3",
           ],
       }
   ```

3. Security Checks with Bandit:
   - Bandit is configured to run security checks
   - Skips B101 (assert warnings)
   - Excludes test files from security checks
   - Runs automatically in pre-commit hooks

4. Code Style Guidelines:
   - Use type hints
   - Follow Python's naming conventions:
     ```python
     # Classes: PascalCase
     class UserProfile:
         pass
     
     # Functions/variables: snake_case
     def calculate_total():
         user_count = 0
     
     # Constants: UPPER_CASE
     MAX_RETRIES = 3
     ```
