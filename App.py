from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import webbrowser

app = Flask(__name__)
port = 5000
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
    cursor.execute('''SELECT * FROM items''')
    all_item_data = cursor.fetchall()
    cursor.close()
    # print(all_data)

    return render_template("index.html", user_data=all_data, item_data=all_item_data)


@app.route('/items')
def IndexItem():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM items''')
    all_data = cursor.fetchall()
    cursor.close()

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
        cursor.close()

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
        cursor.close()

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
        price = request.form.get('price')
        avail_quantity = request.form['avail_quantity']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO items(name, price, avail_quantity) VALUES(%s, %s, %s)''',
                       [name, price, avail_quantity])
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
        price = request.form['price']
        avail_quantity = request.form['avail_quantity']

        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE items SET name=%s, price=%s, avail_quantity=%s WHERE id=%s ''',
                       [name, price, avail_quantity, _id])
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


@app.route('/shop/<id>', methods=['GET', 'POST'])
def shop(id):

    # fetching user info
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT name, contact FROM users where id=%s''', [id])
    user = cursor.fetchall()
    cursor.close()

    id_list = request.form.getlist("id")
    name_list = request.form.getlist('name')
    price_list = request.form.getlist('price')
    quantity_list = request.form.getlist("quantity")

    myDict = dict()
    for i in range(0, len(id_list)):
        myDict.update(
            {id_list[i]: [name_list[i], price_list[i], quantity_list[i]]})

    # this has the id of the items that are checked
    check_list = request.form.getlist("itemcheck")

    # printing the bill
    f = open("Bill.txt", "w")
    print("Bill:", file=f)
    print("Customer Id:", id, file=f)
    user_name = user[0]["name"]
    user_contact = user[0]["contact"]
    print("Name:", user_name, file=f)
    print("Contact:", user_contact, file=f)

    print("Item_Name", "Price", "Quantity", file=f)
    total_price = 0
    for check_id in check_list:
        check_row = myDict[check_id]
        total_price += int(check_row[1])*int(check_row[2])
        print(check_row[0], check_row[1], check_row[2], file=f)

    print("Total Price: Rs", total_price, file=f)

    # webbrowser.open_new_tab('Bill.txt')

    # return redirect(url_for('Index'))

    return render_template('Bill.html', user_id=id, user_name=user_name, user_contact=user_contact, item_map=myDict, check_id_list=check_list, total_price=total_price)


if __name__ == "__main__":
    app.run(port=port, debug=True)
