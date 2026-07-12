import sqlite3

DB_PATH = "database/energy.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (username, email, password)
    )

    conn.commit()
    conn.close()
def check_user(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user
def create_sensor_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        voltage REAL,

        current REAL,

        power REAL,

        energy REAL,

        cost REAL,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()
    conn.close()


def save_sensor_data(voltage,current,power,energy,cost):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO sensor_data
    (voltage,current,power,energy,cost)

    VALUES(?,?,?,?,?)

    """,(voltage,current,power,energy,cost))

    conn.commit()

    conn.close()

def get_sensor_data():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT voltage, current, power, energy, cost, timestamp
        FROM sensor_data
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
def get_statistics():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            AVG(voltage),
            AVG(current),
            AVG(power),
            AVG(energy),
            AVG(cost)
        FROM sensor_data
    """)

    stats = cursor.fetchone()

    conn.close()

    return stats

def create_device_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE,

        status TEXT

    )
    """)

    devices = [
        ("Light", "ON"),
        ("Fan", "ON"),
        ("AC", "OFF"),
        ("TV", "ON")
    ]

    for device in devices:
        cursor.execute(
            "INSERT OR IGNORE INTO devices(name,status) VALUES(?,?)",
            device
        )

    conn.commit()
    conn.close()

def get_devices():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices")

    devices = cursor.fetchall()

    conn.close()

    return devices


def toggle_device(device_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM devices WHERE id=?",
        (device_id,)
    )

    status = cursor.fetchone()[0]

    new_status = "OFF" if status == "ON" else "ON"

    cursor.execute(
        "UPDATE devices SET status=? WHERE id=?",
        (new_status, device_id)
    )

    conn.commit()
    conn.close()

    conn.commit()
    conn.close()



create_sensor_table()
create_device_table()
init_db()
print("DATABASE FILE LOADED")