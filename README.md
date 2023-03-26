Match the Column Game
=====================

This repository contains a Python-based web application, using the Flask framework, which allows users to play a match-the-column game. The game is based on multiple levels with questions related to SAP Business Technology Platform (SAP BTP).

Usage
-----

1.  Register as a new user or log in using your Google account.
2. **Gameplay**: You will start at Level 1. Each level contains five multiple-choice questions randomly selected from a question pool. Your objective is to answer at least three questions correctly in each level to proceed to the next one.

3. **Scoring**: Points are awarded based on the difficulty of each level. You will earn 3 points for each correct answer in Level 1, 7 points in Level 2, and 10 points in Level 3. Your total score will be the sum of points earned across all levels. max score 100.

4. **Progression**: If you answer at least three questions correctly in a level, you will advance to the next level. There are three levels in total.

5. **Leaderboard**: After completing all three levels or answering less than three questions correctly in a level, your game will end, and you will be redirected to the leaderboard page. The leaderboard displays the ranking of all players based on their scores.

6. **Logging Out**: You can log out of the game by clicking the 'Logout' button.

7. **Please note that you can only play the game once per account. **

8. Enjoy the game and test your SAP BTP knowledge! Good luck! !😊
[😈 Press Here ](https://rugved1.pythonanywhere.com)

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

1. Clone the repository:

`git clone https://github.com/rugved88/SAP-Match-the-Columns-Game.git`

2. Navigate to the project directory:

`cd repository`

3. Create a virtual environment:

`python -m venv venv`

4. Activate the virtual environment:

-   On Windows:

`venv\Scripts\activate`

-   On Linux or macOS:

`source venv/bin/activate`

5. Install the required packages:

`pip install -r requirements.txt`

Configuration
-------------

Open the `main.py` file and update the following configurations:

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

For Phone Number Verification we are using [Vonage Verify API](https://dashboard.nexmo.com/getting-started/verify)
- Replace with your Vonage API key
- Replace with your Vonage API secret

Running the Application
-----------------------

To run the application, execute the following command:

`python main.py`

Access the application by opening your web browser and navigating to `http://127.0.0.1:5000/`.

Contributing
------------

Feel free to fork this repository and make changes as you like. If you have any suggestions or improvements, please submit a pull request or open an issue.

License
-------

This project is licensed under the MIT License.
