import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "hetpatel",
    "password": "hetpatel",
    "database": "learning_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()
