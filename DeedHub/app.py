from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector
import base64
import bcrypt

app = Flask(__name__)

# Database connection
db_config = {
    "host": "localhost",
    "user": "sqluser",
    "password": "password",
    "database": "site_details"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('choice.html')

@app.route('/index')
def next_page():
    return render_template('signup.html')

@app.route('/signin')
def sig():
    return render_template('signin.html')
# uploading data
@app.route('/upload/<username>', methods=['POST'])
def upload(username):
    name = request.form['name']
    contact = request.form['ph_no']
    dimension = request.form['dim']
    site_desc = request.form['des']
    site_loc = request.form['loc']
    image = request.files['image']
    dist = request.form['dist']
    s_no = request.form['s_no']
    connection = get_db_connection()
    image_data = image.read()
    image_data = mysql.connector.Binary(image_data)

    cursor = connection.cursor()

    cursor.execute("INSERT INTO seller_information (username, password, name, contact, dimension, site_desc, site_loc, district, image,s_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                   (username, "", name, contact, dimension, site_desc, site_loc, dist, image_data,s_no))

    connection.commit()
    cursor.close()
    connection.close()

    return "Data Logged In successfully"

# getting particular seller data
@app.route('/get_user_data/<username>', methods=['GET', 'POST'])
def get_user_data(username):
    if request.method == 'POST':
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM seller_information WHERE username=%s", (username,))
        user_data = cursor.fetchall()
        return render_template('table.html', data=user_data, base64=base64)
    else:
        return "No data found for the provided username."

# data retrive
@app.route('/display_data')
def display_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    Y = "SELECT * FROM seller_information"
    cursor.execute(Y)

    data = cursor.fetchall()
    filtered_data = [row for row in data if row[3]]

    cursor.close()
    connection.close()
    return render_template('data.html', data = filtered_data,base64=base64)

# signup
@app.route('/signup', methods=['POST'])
def signup():
    connection = get_db_connection()
    cursor = connection.cursor()
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return "Password and Confirm Password do not match."

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO seller_information (username, password) VALUES (%s, %s)", (username, hashed_password))
    connection.commit()
    return redirect('/signin')

#signin
@app.route('/signin', methods=['POST'])
def signin():
    connection = get_db_connection()
    cursor = connection.cursor()
    render_template('signin.html')
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM seller_information WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and user[2] and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return render_template('index.html', username=username)

    return "Invalid username or password."

#delete row
@app.route('/delete_row/<int:id>', methods=['POST'])
def delete_row(id):
    if request.method == 'POST':
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM seller_information WHERE id=%s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
    return "Data Deleted"



#area price
@app.route('/area_display')
def display_areas():
    areas_data = [
    {"name":"JP Nagar","price":"₹4,125 - ₹5,486"},
    {"name":"Vidyaranya Puram","price":"₹3,058 - ₹6,333"},
    {"name":"Kuvempunagara","price":"₹6,842 - ₹19,047"},
    {"name":"Bogadi","price":"₹4,032 - ₹6,200"},
    {"name":"Gokulam","price":"₹4,526 - ₹6,000"},
    {"name":"Hebbal","price":"₹5,034 - ₹14,375"},
    {"name":"Yadavagiri","price":"₹3,940 - ₹7,555"},
    {"name":"Deepanagar","price":"₹3,603 - ₹7,937"},
    {"name":"Rajarajeshwari Nagar","price":"₹ ₹7,400"},
    {"name":"Vani Vilas Mohalla","price":"₹4,597 - ₹7,500"},
    {"name":"Kalyangiri","price":"₹4,261 - ₹4,261"},
    {"name":"Jayalakshmipuram","price":"₹4,491 - ₹7,812"},
    {"name":"Hootagalli","price":"₹3,738 - ₹5,250"},
    {"name":"Metagalli","price":"₹5,294 - ₹7,182"},
    {"name":"Roopa Nagar","price":"₹5,000 - ₹10,000"},
    {"name":"Ilavala Hobli","price":"₹2,000"},
    {"name":"Chamundipuram","price":"₹5,208 - ₹5,668"},
    {"name":"Rajendra Nagar","price":"₹3,609 - ₹3,707"},
    {"name":"Vijayanagara","price":"₹4,766 - ₹5,545"},
    {"name":"Saraswathipuram","price":"₹9201"},
    {"name":"TK Layout","price":"₹6,363 - ₹9,579"},
    {"name":"Daddakallahalli","price":"₹5,000 - ₹5,000"},
    {"name":"Koorgalli","price":"₹2,416 - ₹2,416"},
    {"name":"Lakshmipuram","price":"₹6,457 - ₹10,000"},
    {"name":"Jayanagara","price":"₹6,250 - ₹6,250"},
    {"name":"Mandi Mohalla","price":"₹5,166 - ₹10,068"},
    {"name":"Agrahara","price":"₹14,652 - ₹14,652"},
    {"name":"Ramakrishnanagara","price":"₹5,833 - ₹5,833"},
    {"name":"Srirampura","price":"₹6,666"},
    {"name":"Siddhartha Layout","price":"₹7,364 - ₹10,000"},
]
    taluk=[
        {"name":"Mysuru Taluk","price":"₹2,800"},
        {"name":"Heggadadevanakote(H.D Kote)","price":"₹1,130"},
        {"name":"Hunsur","price":"₹1,000 - ₹2,500"},
        {"name":"Krishnarajanagara(K.R Nagar)","price":"₹2,000"},
        {"name":"Nanjangud","price":"₹1,500"},
        {"name":"Periyapatna","price":"₹2,100"},
        {"name":"T.Narsipu","price":"₹2,500-₹3,500"},
    ]
    return render_template('list.html', areas=areas_data,taluk_data=taluk)

if __name__ == '__main__':
    app.run(debug=True)                                                                                                                                                                                                                                                                                                                            