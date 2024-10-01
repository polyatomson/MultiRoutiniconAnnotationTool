def sort_glosses(gl_list: list[str]) -> list[str]:
    lex_glosses = sorted([gl for gl in gl_list if gl.upper() != gl])
    gram_glosses = sorted([gl for gl in gl_list if gl not in lex_glosses])
    return lex_glosses + gram_glosses