from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ROOT'  # Replace 'your_secret_key' with a random string

# Dummy user database (replace with a real database)
users = {'Rawdog': 'BBC', 'LKreku': 'Ilovedan'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0')














from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form.get('description')
    amount = request.form.get('amount')
    date = request.form.get('date')
    new_expense = Expense(description=description, amount=float(amount), date=date)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

# Create app context and perform database operations within it
with app.app_context():
    db.create_all()
from flask import redirect, url_for, session

@app.route('/logout', methods=['POST'])
def logout():
    # Remove the 'logged_in' and 'username' keys from the session
    session.pop('logged_in', None)
    session.pop('username', None)
    # Redirect to the login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
