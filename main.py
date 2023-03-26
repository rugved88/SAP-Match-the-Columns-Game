# pip install Flask-Mail, pip install nexmo
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_oauthlib.client import OAuth
from flask_mail import Mail, Message
import vonage

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sapbtpgame@gmail.com'  # Update with your email
app.config['MAIL_PASSWORD'] = 'password@7710035822'  # Update with your email password

mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    company_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    email_confirmed = db.Column(db.Boolean, default=False)
    logged_in = db.Column(db.Boolean, default=False)  # New logged_in column
    game_played = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'


sap_btp_questions = [
    [
        {'id': 1, 'question': 'SAP BTP is an abbreviation for', 'answer': 'SAP Business Technology Platform'},
        {'id': 2, 'question': 'SAP BTP is a', 'answer': 'Platform-as-a-Service'},
        {'id': 3, 'question': 'One of the key components of SAP BTP is', 'answer': 'SAP HANA'},
        {'id': 4, 'question': 'SAP BTP provides', 'answer': 'Integration services'},
        {'id': 5, 'question': 'SAP BTP supports', 'answer': 'Multi-cloud environment'},
    ],
    # level 2 questions
    [
        {'id': 6, 'question': 'The primary programming language for SAP BTP is', 'answer': 'Java'},
        {'id': 7, 'question': 'SAP BTP allows developers to build', 'answer': 'Extensions for SAP solutions'},
        {'id': 8, 'question': 'SAP BTP offers analytics capabilities through', 'answer': 'SAP Analytics Cloud'},
        {'id': 9, 'question': 'SAP BTP includes a service called', 'answer': 'SAP API Management'},
        {'id': 10, 'question': 'SAP BTP uses which database technology', 'answer': 'SAP HANA'},
    ],
    # level 3 questions
    [
        {'id': 11, 'question': 'Which SAP BTP service enables IoT capabilities?', 'answer': 'SAP IoT Services'},
        {'id': 12, 'question': 'What is the name of the low-code development tool in SAP BTP?',
         'answer': 'SAP AppGyver'},
        {'id': 13, 'question': 'SAP BTP allows developers to use which serverless runtime?',
         'answer': 'SAP Cloud Functions'},
        {'id': 14, 'question': 'Which service in SAP BTP enables AI capabilities?',
         'answer': 'SAP AI Business Services'},
        {'id': 15, 'question': 'What is the name of the blockchain service in SAP BTP?',
         'answer': 'SAP Blockchain Services'},
    ]
]

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='406994588398-rco9spu6b4flk238oqqu8krj49jbb7p6.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/login_google')
def login_google():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/login_google/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('login'))

    access_token = resp['access_token']
    session['access_token'] = access_token
    me = google.get('userinfo')

    # Check if a user with the provided email already exists in the database
    existing_user_email = User.query.filter_by(email=me.data['email']).first()

    if existing_user_email:
        flash('A user with this email already exists. Please use a different email.')
        return redirect(url_for('login'))

    try:
        # If the user doesn't exist, create a new user with Google Account information
        new_user = User(
            name=me.data.get('given_name', 'Temp'),
            surname=me.data.get('family_name', 'User'),
            company_name='login_by_gmail',
            username=me.data['email'].split('@')[0],
            phone_number=str(random.randint(1000000000, 9999999999)),  # Generate a random phone number
            email=me.data.get('email', 'temp@example.com'),
            password=generate_password_hash(me.data['id'], method='sha256')  # Use Google Account ID as password
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id

        flash('Login successful!')
        return redirect(url_for('index'))

    except:
        db.session.rollback()
        flash('A user with this phone number or email already exists. Please use a different phone number or email.')
        return redirect(url_for('login'))

    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id

    flash('Login successful!')
    return redirect(url_for('index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('access_token')

def generate_otp():
    return str(random.randint(100000, 999999))



VONAGE_API_KEY = '8cd6dea0'  # Replace with your Vonage API key
VONAGE_API_SECRET = 'c7W27ZR2PeysarUA'  # Replace with your Vonage API secret

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        company_name = request.form['company_name']
        username = request.form['username']
        country_code = request.form['country_code']  # Get the country code
        phone_number = request.form['phone_number']
        full_phone_number = country_code + phone_number  # Combine country code and phone number
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if a user with the provided email and phone number already exists in the database
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_phone = User.query.filter_by(phone_number=phone_number).first()

        if existing_user_email or existing_user_phone:
            flash('A user with this email and/or phone number already exists. Please use a different email and/or phone number.')
            return redirect(url_for('register'))

        # Store user data in session
        session['user_data'] = {
            'name': name,
            'surname': surname,
            'company_name': company_name,
            'username': username,
            'phone_number': phone_number,
            'email': email,
            'password': hashed_password
        }

        client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
        verify = vonage.Verify(client)

        response = verify.start_verification(number=full_phone_number, brand="YourCompanyName")

        if response["status"] == "0":
            session['request_id'] = response["request_id"]
            flash('A PIN has been sent to your phone number for verification. Please enter the PIN below.')
            return redirect(url_for('verify_check'))
        else:
            flash(f"Error: {response['error_text']}")

    return render_template('register.html')


@app.route('/verify_check', methods=['GET', 'POST'])
def verify_check():
    if request.method == 'POST':
        code = request.form['code']
        request_id = session['request_id']

        client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
        verify = vonage.Verify(client)

        response = verify.check(request_id, code=code)

        if response["status"] == "0":
            # Retrieve user data from session and create a new user
            user_data = session['user_data']
            new_user = User(name=user_data['name'], surname=user_data['surname'], company_name=user_data['company_name'], username=user_data['username'],
                            phone_number=user_data['phone_number'], email=user_data['email'], password=user_data['password'])
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id

            flash("Verification successful")
            return redirect(url_for('login')) # Replace with the route you want to redirect after successful verification
        else:
            flash(f"Error: {response['error_text']}")

    return render_template('verify_check.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        user = User.query.filter_by(phone_number=phone_number).first()
        users = User.query.all()
        for i in users:
            print(i.phone_number)
        if user and check_password_hash(user.password, password):
            if user.game_played:  # Check if the user has already played the game
                flash('You have already played the game. Redirecting to leaderboard.')
                return redirect(url_for('leaderboard'))

            session['user_id'] = user.id
            user.logged_in = True
            db.session.commit()
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid phone number or password. Please try again.')

    return render_template('login.html')



@app.route('/logout')
def logout():
    user = User.query.get(session['user_id'])
    user.game_played = True  # Set game_played to True after the game is finished
    user.logged_in = False  # Set logged_in to False
    db.session.commit()
    session.pop('user_id', None)
    flash('You have been logged out.')
    edit_all_users()
    return redirect(url_for('login'))

@app.route('/next_level', methods=['GET'])
def next_level():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    level = int(request.args.get('level', 0))

    if user.game_played and level >= len(sap_btp_questions):  # Check if the user has played all levels
        flash('You have already played the game. Redirecting to leaderboard.')
        return redirect(url_for('leaderboard'))

    return redirect(url_for('index', level=level))


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.game_played:  # Check if the user has already played the game
        flash('You have already played the game. Redirecting to leaderboard.')
        return redirect(url_for('leaderboard'))

    if request.method == 'POST':
        user_answers = request.form.to_dict()
        correct_answers = 0
        level = int(user_answers.get('level', 0))

        for k, v in user_answers.items():
            if k.startswith('answer_'):
                print(f"Submitted answer: {k}: {v}")
                question_id = int(k.split('_')[-1])
                for question in sap_btp_questions[level]:
                    if question['id'] == question_id and question['answer'] == v.strip():
                        correct_answers += 1
                        print(f"Correct answer found: {question['question']} - {question['answer']}")

        print(f"Correct answers count: {correct_answers}")

        points_per_level = [3, 7, 10]

        user.score += correct_answers * points_per_level[level]
        db.session.commit()

        if correct_answers >= 3:
            if level + 1 < len(sap_btp_questions):
                flash('Congratulations! You passed level {} with {} correct answers!'.format(level + 1, correct_answers))
                return redirect(url_for('next_level', level=level + 1))  # Redirect to the next_level route
            else:
                flash('Congratulations! You completed all levels!')
                user.game_played = True  # Set game_played to True after the game is finished
                db.session.commit()
                return redirect(url_for('leaderboard'))
        else:
            flash('You got {} correct answers in level {}. You are now logged out.'.format(correct_answers, level + 1))
            session.pop('user_id', None)
            user.game_played = True  # Set game_played to True after the game is finished
            db.session.commit()
            return redirect(url_for('leaderboard'))

    level = int(request.args.get('level', 0))
    questions = random.sample(sap_btp_questions[level], 5)
    random_answers = [q['answer'] for q in questions]
    random.shuffle(random_answers)

    return render_template('index.html', questions=questions, answers=random_answers, level=level)


@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.score.desc()).all()
    user_rank = 0
    user_score = 0

    if 'user_id' in session:
        user_id = session['user_id']
        for rank, user in enumerate(users, 1):
            if user.id == user_id:
                user_rank = rank
                user_score = user.score
                break

    return render_template('leaderboard.html', users=users, user_rank=user_rank, user_score=user_score)

def add_admin():
    admin_username = "admin"
    admin_phone_number = "1234567890"
    admin_email = "admin@example.com"
    admin_password = generate_password_hash("admin_password", method='sha256')

    existing_admin = User.query.filter_by(username=admin_username).first()

    if not existing_admin:
        admin = User(
            name="Admin",
            surname="Admin",
            company_name="Admin",
            username=admin_username,
            phone_number=admin_phone_number,
            email=admin_email,
            password=admin_password,
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user added.")

@app.route('/edit_all_users', methods=['GET', 'POST'])
def edit_all_users():
    # Ensure the user editing this page is the admin
    # if session.get('user_id') is None or User.query.get(session['user_id']).username != 'admin':
    #     flash('You do not have permission to edit users.')
    #     return redirect(url_for('leaderboard'))

    users = User.query.all()

    if request.method == 'POST':
        for user in users:
            user_id = str(user.id)
            user.name = request.form['name_' + user_id]
            user.surname = request.form['surname_' + user_id]
            user.company_name = request.form['company_name_' + user_id]
            user.username = request.form['username_' + user_id]
            user.phone_number = request.form['phone_number_' + user_id]
            user.email = request.form['email_' + user_id]
            if request.form['password_' + user_id]:
                user.password = generate_password_hash(request.form['password_' + user_id], method='sha256')
            user.score = int(request.form['score_' + user_id])
            user.game_played = request.form['game_played_' + user_id] == 'True'

        db.session.commit()
        flash('User information has been updated.')
        return redirect(url_for('edit_all_users'))

    return render_template('edit_all.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} has been deleted.")
    else:
        flash("User not found.")
    return redirect(url_for('edit_all_users'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_admin()  # Call the add_admin function before running the app
    app.run(debug=True)