import config
import psycopg2
from markupsafe import escape
from typing import Optional

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
cursor = conn.cursor()

def ex_sources() -> list[str]:
    cursor.execute("""select t.ex_source from (
                        SELECT ex_source from examples where ex_source is not null 
                        union all 
                        SELECT DISTINCT ex_source from examples4cxs where ex_source is not null) t 
                   group by t.ex_source order by count(*) desc, ex_source asc;""")
    sources = cursor.fetchall()
    if sources is None:
        return []
    else:
        return {'sources': [s[0] for s in sources]}