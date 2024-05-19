import sqlite3


def create_database():
    conn = sqlite3.connect('rasa.db')
    cursor = conn.cursor()

    # Delete table if exist
    cursor.execute('DROP TABLE IF EXISTS reservation')

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    date TEXT, 
    nber_pers INTEGER, 
    phone TEXT, 
    comment TEXT
    )''')

    # Insert example data
    reservation = [
        ('Robert', '2 Juillet', 2, "06.30.20.52.70", "Je suis intolérant au lactose"),
        ('Madeleine', '14 Juillet', 3, "06.30.26.52.85", ""),
        ('Michel', '2 Juin', 4, "06.75.26.98.41", "")
    ]
    cursor.executemany('INSERT INTO reservation (name, date, nber_pers, phone, comment) VALUES (?,?,?,?,?)', reservation)

    # Save (commit) the changes
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
