from flask import Flask, render_template, request, redirect, jsonify, json
from flask_mysqldb import MySQL
import yaml, os

app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/trains', methods=['GET', 'POST'])
def traindetails():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        if( cur.execute("SELECT * FROM train") > 0 ):
            trains = cur.fetchall()
        cur.close()
        return render_template('/traindetails.html', trains = trains)
    return render_template('/traindetails.html', trains=trains)

@app.route('/trains/insert', methods=['GET', 'POST', 'PUT', 'DELETE'])
def trains():   
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        temp = request.form
        train_id = temp['train_id']
        start_pt = temp['start_pt']
        dest_pt = temp['dest_pt']
        arrival_time = temp['arrival_time']
        dept_time = temp['dept_time']

        cur.execute("INSERT INTO train VALUES(%s, %s, %s, %s, %s)", (train_id, start_pt, dest_pt, arrival_time, dept_time))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/trains')

    elif request.method == 'PUT':
        cur = mysql.connection.cursor()

        #TODO: Take these values from a form
        train_id = 12000
        start_pt = 'GND'
        dest_pt = 'JAI'
        arrival_time = '14:00:12'
        dept_time = '13:22:12'

        cur.execute("UPDATE train SET train_id = %s, start_pt = %s, dest_pt = %s, arrival_time = %s, dept_time = %s WHERE train_id = %s", (train_id, start_pt, dest_pt, arrival_time, dept_time, train_id))
        mysql.connection.commit()
        cur.close()

        return 'train put'
    return render_template('trainform.html')

@app.route('/trains/delete', methods=['GET', 'DELETE'])
def delete_train():
    if request.method == 'GET':
        cur = mysql.connection.cursor()

        id = request.args.get('id')

        cur.execute("""DELETE FROM train WHERE train_id = %s""", (id,))
        mysql.connection.commit()

        if( cur.execute("SELECT * FROM train") > 0 ):
            trains = cur.fetchall()

        cur.close()

        return redirect("/trains")

if __name__=="__main__":
    app.run(debug=True)

