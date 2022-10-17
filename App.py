from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'fyp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users''')
    all_data = cursor.fetchall()

    # print(all_data)

    return render_template("index.html", user_data=all_data)


@app.route('/items')
def IndexItem():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM items''')
    all_data = cursor.fetchall()

    # print(all_data)

    return render_template("items.html", item_data=all_data)


@app.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        #print('I am search bar')
        searchFor = request.form['sTextUser']
        searchFor = '%'+searchFor+'%'
        # print(searchFor)
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''SELECT * FROM users WHERE name LIKE %s ''', [searchFor])
        mysql.connection.commit()
        search_data = cursor.fetchall()

        return render_template("index.html", user_data=search_data)

    return redirect(url_for('Index'))


@app.route('/items/search', methods=['POST', 'GET'])
def searchItem():

    if request.method == 'POST':
        #print('I am search bar')
        searchFor = request.form['sTextItem']
        searchFor = '%'+searchFor+'%'
        # print(searchFor)
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''SELECT * FROM items WHERE name LIKE %s ''', [searchFor])
        mysql.connection.commit()
        search_data = cursor.fetchall()

        return render_template("items.html", item_data=search_data)

    return redirect(url_for('IndexItem'))


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form['contact']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users(name, contact) VALUES(%s,%s)''',
                       [name, contact])
        mysql.connection.commit()
        cursor.close()

        #flash('Data inserted successfully')

        return redirect(url_for('Index'))


@app.route('/items/insert', methods=['POST'])
def insertItem():

    if request.method == 'POST':
        name = request.form.get('name')
        avail_quantity = request.form['avail_quantity']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO items(name, avail_quantity) VALUES(%s,%s)''',
                       [name, avail_quantity])
        mysql.connection.commit()
        cursor.close()

        #flash('Data inserted successfully')

        return redirect(url_for('IndexItem'))


@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        _id = request.form['id']
        name = request.form['name']
        contact = request.form['contact']

        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE users SET name=%s, contact=%s WHERE id=%s ''',
                       [name, contact, _id])
        mysql.connection.commit()
        cursor.close()

        #flash('Data updated successfully')

        return redirect(url_for('Index'))


@app.route('/items/update', methods=['GET', 'POST'])
def updateItem():

    if request.method == 'POST':
        _id = request.form['id']
        name = request.form['name']
        avail_quantity = request.form['avail_quantity']

        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE items SET name=%s, avail_quantity=%s WHERE id=%s ''',
                       [name, avail_quantity, _id])
        mysql.connection.commit()
        cursor.close()

        #flash('Data updated successfully')

        return redirect(url_for('IndexItem'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):

    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM users WHERE id=%s ''', [id])
    mysql.connection.commit()
    cursor.close()

    #flash('Data deleted successfully')

    return redirect(url_for('Index'))


@app.route('/items/delete/<id>/', methods=['GET', 'POST'])
def deleteItem(id):

    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM items WHERE id=%s ''', [id])
    mysql.connection.commit()
    cursor.close()

    #flash('Data deleted successfully')

    return redirect(url_for('IndexItem'))


if __name__ == "__main__":
    app.run(debug=True)
