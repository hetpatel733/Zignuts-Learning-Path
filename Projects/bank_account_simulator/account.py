from database import get_connection


class BankAccount:
    def __init__(self, name, balance=0.0, account_id=None):
        self.id = account_id
        self.name = name
        self.balance = balance

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO accounts (name, balance) VALUES (%s, %s)",
                (self.name, self.balance),
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE accounts SET name = %s, balance = %s WHERE id = %s",
                (self.name, self.balance, self.id),
            )
        conn.commit()
        cursor.close()
        conn.close()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.save()

    def check_balance(self):
        return self.balance

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = %s", (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_id(account_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, balance FROM accounts WHERE id = %s", (account_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return BankAccount(row[1], float(row[2]), row[0])
        return None

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM accounts")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [BankAccount(r[1], float(r[2]), r[0]) for r in rows]
