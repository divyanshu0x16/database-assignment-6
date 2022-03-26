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
    return render_template('vendors.html')

@app.route('/trains', methods=['GET', 'POST', 'PUT', 'DELETE'])
def trains():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        if( cur.execute("SELECT * FROM train") > 0 ):
            trains = cur.fetchall()
        cur.close()
        print(trains)
        return render_template('trains.html')
    elif request.method == 'POST':
        cur = mysql.connection.cursor()

        trainDetails = request.form
        train_id = trainDetails['train_id']
        start_pt = trainDetails['start_pt']
        dest_pt = trainDetails['dest_pt']
        arrival_time = trainDetails['arrival_time']
        dept_time = trainDetails['dept_time']

        cur.execute("INSERT INTO train VALUES(%s, %s, %s, %s, %s)", (train_id, start_pt, dest_pt, arrival_time, dept_time))
        mysql.connection.commit()
        cur.close()
        
        return render_template('trains.html')

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

    elif request.method == 'DELETE':
        cur = mysql.connection.cursor()

        #TODO: Take id from form
        train_id = 12000

        cur.execute("""DELETE FROM train WHERE train_id = %s""", (train_id,))
        mysql.connection.commit()
        cur.close()

        return 'train delete' 
    return render_template('trains.html')
if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)), debug=True)