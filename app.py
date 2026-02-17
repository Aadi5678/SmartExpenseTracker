from flask import Flask, render_template, request, redirect
from db_config import db

app = Flask(__name__)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    return render_template("index.html", expenses=data)

@app.route('/dashboard')
def dashboard():
    cursor = db.cursor()

    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_data = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    return render_template("dashboard.html", category_data=category_data, total=total)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

@app.route('/add', methods=['POST'])
def add():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    note = request.form['note']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO expenses(amount,category,expense_date,note) VALUES(%s,%s,%s,%s)",
        (amount,category,date,note)
    )
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
