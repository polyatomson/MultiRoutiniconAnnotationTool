import config
import psycopg2

def clear_db():
    conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
    conn.set_session(autocommit=True)
    cursor = conn.cursor()
    cursor.execute(open("sql_queries/truncate.sql", 'r').read())
    print('db cleared')

if __name__ == '__main__':
    clear_db()