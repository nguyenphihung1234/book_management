from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Kết nối MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="library_DBB"
)
cursor = connection.cursor()

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    genre = StringField('Genre')
    submit = SubmitField('Add Book')

class MemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthdate = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Member')

class TransactionForm(FlaskForm):
    member_id = IntegerField('Member ID', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    borrow_date = DateField('Borrow Date', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d')
    status = SelectField('Status', choices=[('Borrowed', 'Borrowed'), ('Returned', 'Returned')])
    submit = SubmitField('Add Transaction')

@app.route('/')
def index():
    cursor.execute("SELECT transactions.id, members.name, books.title, transactions.borrow_date, transactions.return_date, transactions.status FROM transactions JOIN members ON transactions.member_id = members.id JOIN books ON transactions.book_id = books.id")
    transactions = cursor.fetchall()
    return render_template('index.html', transactions=transactions)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        publish_date = form.publish_date.data
        cursor.execute("INSERT INTO books (title, author, publish_date) VALUES (%s, %s, %s)", (title, author, publish_date))
        connection.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        name = form.name.data
        birthdate = form.birthdate.data
        address = form.address.data
        cursor.execute("INSERT INTO members (name, birthdate, address) VALUES (%s, %s, %s)", (name, birthdate, address))
        connection.commit()
        return redirect(url_for('index'))
    return render_template('add_member.html', form=form)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        member_id = form.member_id.data
        book_id = form.book_id.data
        borrow_date = form.borrow_date.data
        return_date = form.return_date.data
        status = form.status.data
        cursor.execute("INSERT INTO transactions (member_id, book_id, borrow_date, return_date, status) VALUES (%s, %s, %s, %s, %s)", 
                       (member_id, book_id, borrow_date, return_date, status))
        connection.commit()
        return redirect(url_for('index'))
    return render_template('add_transaction.html', form=form)

@app.route('/report')
def report():
    cursor.execute("SELECT members.name, members.birthdate, members.address, books.title, transactions.borrow_date, transactions.return_date, transactions.status FROM transactions JOIN members ON transactions.member_id = members.id JOIN books ON transactions.book_id = books.id")
    report_data = cursor.fetchall()
    return render_template('report.html', report_data=report_data)

@app.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    if request.method == 'POST':
        status = request.form.get('status')
        cursor.execute("UPDATE transactions SET status = %s WHERE id = %s", (status, id))
        connection.commit()
        return redirect(url_for('report'))

    cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
    transaction = cursor.fetchone()
    return render_template('edit_transaction.html', transaction=transaction)

if __name__ == '__main__':
    app.run(debug=True)
