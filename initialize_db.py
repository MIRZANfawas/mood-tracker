import sqlite3


def initialize_db():
    conn = sqlite3.connect('mood_tracker.db')
    c = conn.cursor()

    # Create table for user details
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    # Create table for mood data
    c.execute('''
        CREATE TABLE IF NOT EXISTS mood_entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date DATE NOT NULL,
            mood TEXT NOT NULL,
            rating INTEGER NOT NULL,
            notes TEXT,
            sentiment REAL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
