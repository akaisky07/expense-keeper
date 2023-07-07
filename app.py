from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
db = SQLAlchemy(app)

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))

# Home page - Dashboard
@app.route('/')
def home():
    with app.app_context():
        total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
        categories = db.session.query(Expense.category, db.func.sum(Expense.amount)).group_by(Expense.category).all()
    return render_template('dashboard.html', total_expenses=total_expenses, categories=categories)

# Add Expense
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date_str = request.form['date']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']

        # Convert date string to a Python date object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        with app.app_context():
            expense = Expense(date=date, amount=amount, category=category, description=description)
            db.session.add(expense)
            db.session.commit()
        return redirect('/')
    else:
        return render_template('add_expense.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

