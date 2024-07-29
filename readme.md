A Django project with JWT authentication for managing employees.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Running Tests](#running-tests)
- [Additional Notes](#additional-notes)

## Installation

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/Mudka/Operations-Task.git>
   cd myproject

2. Install Dependencies: poetry install
3. Run migrations: make migrate
4. Create a Superuser: make createsuperuser 
   Or you can use an existing one:{
    username: mantas
    password: mantas
   }
5. Run the Development server: make run

### Usage

1. Send a POST request to /employees/api/token/ with your username and password to get the access and refresh tokens.

curl -X POST /employees/api/token/ -d "username=<your_username>&password=<your_password>"

2. You will get a response:

{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}

3. You will need to include the access token in the Authorization header to perform authenticated requests to protected endpoints. Example:

curl -H "Authorization: Bearer your_access_token" http://127.0.0.1:8000/employees/

### API Endpoints

1.  Get All Employees:
URL: /employees/
Method: GET
Auth: Requires JWT token
Description: Retrieve a list of all employees.

2. Get Single Employee by their ID:
URL: /employees/{id}/
Method: GET
Auth: Requires JWT token
Description: Retrieve a single employee by ID.

3. Create an Employee:
URL: /employees/
Method: POST
Auth: Requires JWT token
Description: Create a new employee.
Body Parameters:
{
    name: Employee's name (string)
    department: Employee's department (string)
    workflow: Employee's workflow (float)
}

4. Update an Employee:
URL: /employees/{id}/
Method: PUT
Auth: Requires JWT token
Description: Update an existing employee by ID.
Body Parameters:
{
    name: Employee's name (string)
    department: Employee's department (string)
    workflow: Employee's workflow (float)
}

5. Delete an Employee:
URL: /employees/{id}/
Method: DELETE
Auth: Requires JWT token
Description: Delete an employee by ID.


### Tests
To execute all the test cases in the project use:
"make test"

### Additional notes

1. Database configuration and port can be configurable via the db_config.json file.
2. Use Postman or another API client to interact with the edpoints.
