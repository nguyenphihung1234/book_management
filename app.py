from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Kết nối MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library_DBB"
)

@app.route('/')
def index():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM members")  # Thay bằng tên bảng thành viên của bạn
    members = cursor.fetchall()

    cursor.execute("SELECT * FROM transactions")  # Thay bằng tên bảng giao dịch của bạn
    transactions = cursor.fetchall()

    return render_template('index.html', members=members, transactions=transactions)

# Route thêm thành viên mới
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        address = request.form['address']

        cursor = connection.cursor()
        cursor.execute("INSERT INTO members (name, birth_date, address) VALUES (%s, %s, %s)", (name, birth_date, address))
        connection.commit()
        return redirect(url_for('index'))
    
    return render_template('add_member.html')

# Route thêm sách mới
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        published_date = request.form['published_date']

        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (title, author, published_date) VALUES (%s, %s, %s)", (title, author, published_date))
        connection.commit()
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
