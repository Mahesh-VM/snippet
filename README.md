# Overview
Web app to provide endpoints for snippets.

### Requirements
The requirements needed for this project is included in the requirements.txt file in the project directory.

### Installation
Todo:
1. create a virtual environment, for more information regarding how to create a virtual environment refer [here](https://docs.python.org/3/library/venv.html).
2. then activate the environment by `source <environment_name>/bin/activate`.
3. run the requirements.txt file by using command `pip install -r requirements.txt`.
4. check that all requirements are installed by command pip freeze.

### Start up the Django server
Prerequisite:
1. `python manage.py makemigrations authapp snippetapp` to create migration scripts.
2. `python manage.py migrate authapp snippetapp` to migrate and create sqlite DB.

Todo:
1. `python manage.py runserver` to run the server.
2. Go to the [docs](127.0.0.1:8000/docs/) in the browser, it will display the api endpoints using swagger template.
3. Since the API are protected with jwt tokens so need to create an user account.
4. First create user account using [register url](http://127.0.0.1:8000/auth/register-user/) in postman passing post data as e.g.
`{
    "email": "test@mail.com",
    "password": "test123",
    "confirm_password": "test123",
    "roles": "user",
    "first_name": "Test",
    "last_name": "User",
    "username": "user_one"
}`
5. Use the username and password to generate access token using [token url](http://127.0.0.1:8000/token/)
6. Click on `Authorize` see [image](git_img/auth_unlock.jpg)
7. Copy the access token and prefix `Bearer ` to the token and paste it in the input field named value as shown in the [image](git_img/authorize.jpg).
8. Now go ahead interact with the swagger UI to test the endpoints in browser or can use postman.

### Testing
Test cases is added which test all the API endpoints and is maintained up-to-date.
To test that everything is working fine run `pytest` in the terminal or cmd.

### Documentation and Support
Full documentation regarding djangorestframework is available at https://www.django-rest-framework.org/.