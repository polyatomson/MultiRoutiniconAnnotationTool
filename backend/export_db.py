import psycopg2
import datetime
import json
import config

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()

# def export_expressions():
    
def export_glosses():
    comment = input('Enter identifier for the filename if needed: ')
    output_fn = 'glosses_' + comment + datetime.datetime.now().strftime('%y-%m-%d-%H:%M:%S') + '.json'
    cursor.execute("SELECT JSON_AGG(t) FROM (SELECT * FROM public.glosses) t")
    result = cursor.fetchone()[0]
    with open(f"backups/{output_fn}", 'w', encoding='utf-8') as fp:
        json.dump({'glosses': result}, fp, indent=3)
    print('gloss table exported')

def export_expressions_as_data():
    
    cursor.execute(open('sql_queries/export_expressions_data.sql', 'r').read())
    collections = cursor.fetchall()[0][0]
    for coll in collections:
        lang = coll['lang']
        output_fn = 'expressions_' + lang + '_' + datetime.datetime.now().strftime('%y-%m-%d-%H:%M:%S') + '.json'
        with open(f"backups/{output_fn}", 'w', encoding='utf-8') as fp:
            json.dump({'collection': coll}, fp, indent=3)
    print('lang collections exported to separate files')

def main():
    export_type = input('Export glosses only (g), expressions only (e), or both (Enter)? ')
    if export_type == 'g':
        export_glosses()
    elif export_type == 'e':
        export_expressions_as_data()
    else:
        export_glosses()
        export_expressions_as_data()

if __name__ == '__main__':
    main()