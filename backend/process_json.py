import json
# import re
from dataclasses import dataclass
from typing import Union, Optional

from mini_handlers import sort_glosses

@dataclass
class Gloss:
    gloss: str
    lex: bool
    gl_class: Optional[str]

    @staticmethod
    def identify_gloss(gloss: str):
        if gloss.upper() == gloss:
            lex = False
        else:
            lex = True
        return Gloss(gloss=gloss, lex=lex, gl_class=None)

@dataclass
class Glossed:
    morph: str
    glosses: list[Gloss]

    @staticmethod
    def glossit(morph: str, glosses: str):
        glosses = [ Gloss.identify_gloss(gloss) for gloss in glosses.split('.')]
        return Glossed(glosses=glosses, morph=morph)
@dataclass
class Unit:
    unit: str
    realization: str
    glossing: str
    glossed_morphs: list[Glossed]
    pos: Optional[str]
    lemma: Optional[str]

    @staticmethod
    def create_unit(unit, lemma, pos, realization, glossing):
        morphs = realization.split('-')
        glosses = glossing.split('-')
        glossing_sorted = '-'.join(['.'.join(sort_glosses([gl for gl in m_glosses.split('.')])) for m_glosses in glosses])
        glossed_morphs = [Glossed.glossit(morph, glosses[i]) for i, morph in enumerate(morphs)]
        return Unit(unit, realization, glossing_sorted, glossed_morphs, pos, lemma)

@dataclass
class Expression:
    expression: str
    units: list[Unit]
    
    
    @staticmethod
    def create_expr(expression:str, realization:str, lemmas:str, pos:str, glossing:str):
        units = expression.split(' ')
        u_realization = realization.split(' ')
        lemmas = lemmas.split(' ')
        pos = pos.split(' ')
        glossing = glossing.split(' ')
        units = [Unit.create_unit(u, lemmas[i], pos[i], u_realization[i], 
                                  glossing[i]) for i, u in enumerate(units)]
        return Expression(expression, units)
    def full_glossing(self) -> str:
        return ' '.join([u.glossing for u in self.units])

@dataclass
class LangCollection:
    lang: str
    collection: list[Expression]

    @staticmethod
    def import_collection_from_file(fn: str="data.json"):
        with open(fn, 'r', encoding='utf-8') as f:
            data = json.load(f)
        collection = data["collection"]
        lang = collection["lang"]
        entries = [Expression.create_expr(expression=e["expression"].lower(), 
                                          realization=e["realization"].lower(),
                                          lemmas=e["lemmas"].lower(),
                                          pos=e["pos"].upper(),
                                          glossing=e["glossing"]
                                          ) for e in collection["entries"]]
        return LangCollection(lang, entries)
    
    # @staticmethod
    # def import_collection_from_object(data: list[dict]):
    #     lang = data[0]["lang"]
    #     entries = [Expression.create_expr(expression=e["expression"].lower(), 
    #                                       realization=e["realization"].lower(),
    #                                       lemmas=e["lemmas"].lower(),
    #                                       pos=e["pos"].upper(),
    #                                       glossing=e["glossing"]
    #                                       ) for e in data]
    #     return LangCollection(lang, entries)

def main():
    dat = LangCollection.import_collection()
    print("json loaded")

if __name__ == "__main__":
    main()