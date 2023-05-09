from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

# Here we define the environment variable for the development environment
ENV = 'dev'
# Here we define the environment variable for the production environment
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Here we define the secret key for the application
db = SQLAlchemy(app)

# Here we define the database model


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
# Here we define the constructor for the Feedback class

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

# Here we define the submit route and we use the POST method to submit the form data to the database


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            # We call the send_email method to send feedback here and it takes in the data from the form as arguments
            send_mail(customer, dealer, rating, comments)
            # user successfully submitted feedback
            return render_template('success.html')
        else:
            # user has already submitted feedback
            return render_template('index.html', message='You have already submitted feedback')

    return render_template('index.html')


# Here we define the view route and we use the GET method to view the feedback data from the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
