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

@app.route('/trains', methods=['GET'])
def traindetails():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        trains = []
        schedule = []
        if( cur.execute("SELECT * FROM train") > 0 ):
            trains = cur.fetchall()
        if( cur.execute("SELECT * FROM train_schedule") > 0):
            schedule = cur.fetchall()
        cur.close()
        return render_template('/train_details.html', trains = trains, schedule = schedule)
    return render_template('/train_details.html', trains=trains, schedule = schedule)

@app.route('/trains/insert', methods=['GET', 'POST'])
def trains(): 
    
    id = request.args.get('id')

    if request.method == 'POST':
        cur = mysql.connection.cursor()

        temp = request.form

        train_id = temp['train_id']

        start_pt = temp['start_pt']
        dest_pt = temp['dest_pt']
        arrival_time = temp['arrival_time']
        dept_time = temp['dept_time']

        day = temp['day']
        platform = temp['platform']

        try:
            cur.execute("INSERT INTO train VALUES(%s, %s, %s, %s, %s)", (train_id, start_pt, dest_pt, arrival_time, dept_time))
            cur.execute("INSERT INTO train_schedule VALUES(%s, %s, %s)", (train_id, day, platform))
        except:
            cur.execute("UPDATE train SET train_id = %s, start_pt = %s, dest_pt = %s, arrival_time = %s, dept_time = %s WHERE train_id = %s", (train_id, start_pt, dest_pt, arrival_time, dept_time, train_id))
            cur.execute("UPDATE train_schedule SET train_id = %s, arrival_day = %s, platform = %s WHERE train_id = %s", (train_id, day, platform, train_id))

        mysql.connection.commit()
        cur.close()
        
        return redirect('/trains')

    return render_template('train_form.html')

@app.route('/trains/delete', methods=['GET'])
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

#Code For Passengers
@app.route('/passengers', methods=['GET'])
def passengerdetails():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        passengers = []
        transactions=[]
        tickets=[]
        if( cur.execute("SELECT * FROM passenger") > 0 ):
            passengers = cur.fetchall()
        if( cur.execute("SELECT * FROM transact") > 0 ):
            transactions = cur.fetchall()
        if( cur.execute("SELECT * FROM ticket") > 0 ):
            tickets = cur.fetchall()
        cur.close()
        return render_template('/passenger_details.html', passengers=passengers,transactions=transactions,tickets=tickets)
    return render_template('/passenger_details.html', passengers=passengers,transactions=transactions,tickets=tickets)

@app.route('/passenger/insert', methods=['GET', 'POST'])
def passengers(): 
    
    id = request.args.get('aadhar_no')

    if request.method == 'POST':
        cur = mysql.connection.cursor()

        temp = request.form

        first_name= temp['first_name']
        last_name= temp['last_name']
        dob= temp['dob']
        aadhar= temp['aadhar']
        
        transaction_id= temp['trans_id']
        mode_of_payment= temp['mode_of_payment']
        date_of_payment= temp['date_of_payment']
        amount= temp['amount']
        
        train_id= temp['train_id']
        seat_no= temp['seat_no']
        coach= temp['coach']
        status= temp['status']
        dot= temp['date_of_travel']

        try:
            cur.execute("INSERT INTO passenger VALUES(%s, %s, %s, %s)", (aadhar, first_name, last_name, dob))
            cur.execute("INSERT INTO transact VALUES(%s, %s, %s,%s)", (transaction_id,mode_of_payment,amount,date_of_payment))
            cur.execute("INSERT INTO ticket VALUES(%s, %s, %s,%s, %s, %s, %s)", (aadhar, train_id, transaction_id, seat_no, coach, status, dot))
        except:
            cur.execute("UPDATE ticket SET aadhar_no = %s, train_id = %s, transaction_id = %s, seat_no = %s, coach_no = %s,ticket_status=%s,date_of_travel=%s WHERE aadhar_no = %s", (aadhar,train_id,transaction_id,seat_no,coach,status,dot,aadhar))
            cur.execute("UPDATE transact SET transaction_id = %s, mode_of_payment = %s, amount = %s,date_of_payment=%s WHERE transaction_id = %s", (transaction_id,mode_of_payment,amount,date_of_payment,transaction_id))
            cur.execute("UPDATE passenger SET aadhar_no = %s, first_name = %s, last_name = %s,dob=%s WHERE aadhar_no = %s", (aadhar, first_name, last_name, dob,aadhar))

        mysql.connection.commit()
        cur.close()
        
        return redirect('/passengers')

    return render_template('passenger_form.html')

@app.route('/passenger/delete', methods=['GET'])
def delete_passenger():
    if request.method == 'GET':
        cur = mysql.connection.cursor()

        id = request.args.get('id')
        print(id)

        cur.execute("""DELETE FROM passenger WHERE aadhar_no = %s""", (id,))
        mysql.connection.commit()

        cur.close()

        return redirect("/passenger_form")

if __name__=="__main__":
    app.run(debug=True)

