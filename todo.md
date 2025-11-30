- prompting to implement parametrized tests
- and reimplement playwright fixtures

1. Refactor login page test to parametrized - Create separate variables using Faker for values, use only negative pairs
   of data
2. Use boundary values and class partition test design techniques - Generate test data using boundary value analysis and
   equivalence class partitioning
3. Refactor fixtures to have ability to not restart browser on every test
4. Implement fixtures from scratch based on Playwright documentation - Instantiate playwright, browser, browser context
   and page manually; if login fixture is used
   it should reuse active browser context but should be clean
5. Implement usage of such fixtures - Update tests to use the new fixture structure
6. The test_login_invalid should use the same approach - Reuse browser context and not close the browser on every
   iteration and reuse opened page
