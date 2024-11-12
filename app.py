from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Menambahkan CORS untuk seluruh aplikasi

# Fungsi untuk membuat database dan tabel
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suhu_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idx INTEGER,
            suhu INTEGER,
            humid INTEGER,
            kecerahan INTEGER,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS month_year_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_year TEXT
        )
    ''')
    # Insert sample data
    cursor.execute("INSERT INTO suhu_data (idx, suhu, humid, kecerahan, timestamp) VALUES (101, 36, 36, 25, '2010-09-18 07:23:48')")
    cursor.execute("INSERT INTO suhu_data (idx, suhu, humid, kecerahan, timestamp) VALUES (226, 36, 36, 27, '2011-05-02 12:29:34')")
    cursor.execute("INSERT INTO month_year_data (month_year) VALUES ('9-2010')")
    cursor.execute("INSERT INTO month_year_data (month_year) VALUES ('5-2011')")
    conn.commit()
    conn.close()

# Endpoint untuk mengambil data JSON
@app.route('/api/suhu', methods=['GET'])
def get_suhu_data():
    # Fetch data from database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    
    # Fetch suhu_data
    cursor.execute('SELECT idx, suhu, humid, kecerahan, timestamp FROM suhu_data')
    suhu_data_rows = cursor.fetchall()
    suhu_data = {str(i): {"idx": row[0], "suhu": row[1], "humid": row[2], "kecerahan": row[3], "timestamp": row[4]} for i, row in enumerate(suhu_data_rows)}

    # Fetch month_year_data
    cursor.execute('SELECT month_year FROM month_year_data')
    month_year_rows = cursor.fetchall()
    month_year_data = {str(i): {"month_year": row[0]} for i, row in enumerate(month_year_rows)}
    
    # JSON response
    response = {
        "suhumax": 36,
        "suhumin": 23,
        "suhurata": 28.35,
        "nilai_suhu_max_humid_max": suhu_data,
        "month_year_max": month_year_data
    }
    
    conn.close()
    return jsonify(response)

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
