import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def setup():
    db = settings.DATABASES['default']
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=db.get('USER', 'hetpatel'),
            password=db.get('PASSWORD', 'hetpatel'),
            host=db.get('HOST', '127.0.0.1'),
            port=db.get('PORT', '5432')
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db['NAME'],))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db['NAME'])))
            print(f"Created database {db['NAME']}")
        cur.close()
        conn.close()

        call_command('migrate')
        print("Migrations complete.")
    except Exception as e:
        print(f"Database setup error: {e}")

if __name__ == '__main__':
    setup()
