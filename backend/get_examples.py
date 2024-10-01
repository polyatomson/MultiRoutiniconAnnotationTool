import config
import psycopg2
from sketchengine_request import get_examples_from_corpus, ExamplesResults


def get_corpname(lang_id: int) -> tuple[str, str]:
    conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
    cursor = conn.cursor()
    cursor.execute("""SELECT link, source_name FROM sketchengine_corpora WHERE lang_id = %s""", (lang_id, ))
    link = cursor.fetchone()
    if link is None:
        return None
    conn.close()
    return link

def get_examples(expressions: list[dict], lang_id: int, page_num: int) -> list[dict]:
    link, corpname = get_corpname(lang_id)
    results = list()
    try:
        for expr in expressions:
            sentence_case = expr['expr_full'][0].upper() + expr['expr_full'][1:]
            expr_examples = get_examples_from_corpus(sentence_case, link, n_examples=10, page_num=page_num).to_dict()
            expr_examples['expr_id'] = expr['expr_id']
            expr_examples['expr_full'] = expr['expr_full']
            expr_examples['corpname'] = corpname
            results.append(expr_examples)
    except Exception as ex:
        return {'error': str(type(ex))}
    return results

# exprs = [
#   {
#     "expr_full": "dobro jutro",
#     "expr_id": 226,
#     "glossing": "good-N.NOM/ACC.SG morning-NOM/ACC.SG",
#     "lemmas": "dober jutro",
#     "pos": "A N",
#     "realization": "dobr-o jutr-o"
#   },
#   {
#     "expr_full": "bejž no bejž",
#     "expr_id": 294,
#     "glossing": "run.2.IMP.REDUC.SG PART run.2.IMP.REDUC.SG",
#     "lemmas": "bežati no bežati",
#     "pos": "V PART V",
#     "realization": "bejž no bejž"
#   }
# ]

# get_examples(exprs, 57, 1)


    
