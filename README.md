Match the Column Game
=====================

This repository contains a Python-based web application, using the Flask framework, which allows users to play a match-the-column game. The game is based on multiple levels with questions related to SAP Business Technology Platform (SAP BTP).

Features
--------

-   User registration and login
-   Google authentication
-   Multiple levels of game
-   Leaderboard
-   Admin functionality to edit and delete users

Installation
------------

Before running the application, ensure you have Python installed on your system.

Clone the repository:

bashCopy code

`git clone https://github.com/username/repository.git`

Navigate to the project directory:

bashCopy code

`cd repository`

Create a virtual environment:

bashCopy code

`python -m venv venv`

Activate the virtual environment:

-   On Windows:

bashCopy code

`venv\Scripts\activate`

-   On Linux or macOS:

bashCopy code

`source venv/bin/activate`

Install the required packages:

bashCopy code

`pip install -r requirements.txt`

Configuration
-------------

Open the `app.py` file and update the following configurations:

-   Replace `your_secret_key` with a secret key of your choice.
-   Update the `app.config['MAIL_USERNAME']` and `app.config['MAIL_PASSWORD']` with your email and password, respectively.

If you want to enable Google authentication, follow these steps:

1.  Go to the [Google API Console](https://console.developers.google.com/).
2.  Create a new project.
3.  Go to the "Credentials" section and click on "Create credentials."
4.  Choose "OAuth client ID."
5.  Select "Web application" as the application type.
6.  Enter the authorized redirect URIs as `http://127.0.0.1:5000/login_google/authorized`.
7.  Click on "Create" and copy the client ID and client secret.
8.  Update the `consumer_key` and `consumer_secret` in the `app.py` file with your client ID and client secret, respectively.

Running the Application
-----------------------

To run the application, execute the following command:

bashCopy code

`python app.py`

Access the application by opening your web browser and navigating to `http://127.0.0.1:5000/`.

Usage
-----

1.  Register as a new user or log in using your Google account.
2.  Start the game by selecting a level.
3.  Match the questions with the correct answers.
4.  Complete all levels and view your rank on the leaderboard.

Contributing
------------

Feel free to fork this repository and make changes as you like. If you have any suggestions or improvements, please submit a pull request or open an issue.

License
-------

This project is licensed under the MIT License.
