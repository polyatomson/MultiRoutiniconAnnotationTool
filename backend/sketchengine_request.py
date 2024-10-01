from dataclasses import dataclass, asdict
import requests
import re
import config
from typing import Optional

@dataclass
class CQL:
    exact_match: str #cf. No way
    within_sentence: bool = True
    lemmas: bool = False
    ignore_capital: bool = False
    ends_w_any_punc: bool = False
    end_punc: Optional[str] = None

    @staticmethod
    def ignore_caps(word: str) -> str:
        return '(' + word[0].lower() + '|' + word[0].upper() + ')' + word[1:]
    
    def form_query(self) -> str:
        words = self.exact_match.split(' ')
        qualificator = 'lemma' if self.lemmas else 'word'
        result = ([f'[{qualificator}=\"' + w + '\"]' if not self.ignore_capital else f'[{qualificator}=\"' + CQL.ignore_caps(w) + '\"]' for w in words])
        if self.end_punc is not None:
            punc = re.escape(self.end_punc)
            result.append(f'[word="{punc}"]')
        elif self.ends_w_any_punc:
            result.append('[word="\.|!|\?"] ')
        if self.within_sentence:
            result.append('within <s/>')
        return 'q'+' '.join(result)


@dataclass
class Query:
    corpname: str
    q: str # [word="No"][word="way"] within <s/>
    fcrit: str = 'lemma/i 2'
    flimit: int = 0
    fromp: int = 1
    pagesize: int = 10
    kwicleftctx: str = '100#'
    kwicleftctx: str = '100#'

@dataclass
class Example:
    left: str
    kwic: str
    right: str
    full: str
    source_code: str
    source_name: Optional[str]
    year: Optional[int]

    @staticmethod
    def parse_sketch_engine_line(line: dict) -> 'Example':
        left = ' '.join([word['str'] for word in line['Left'] if 'str' in word])
        right = ' '.join([word['str'] for word in line['Right'] if 'str' in word])
        kwic = ' '.join([word['str'] for word in line['Kwic'] if 'str' in word])
        source_code = line['Refs'][0]
        if len(line['Refs']) > 1:
            source_name = line['Refs'][1]
            try:
                year = int(line['Refs'][2])
            except:
                year = None
        else:
            source_name = None
            year = None
        full = ' '.join([left, kwic, right])
        return Example(left, kwic, right, full, source_code, source_name, year)

@dataclass
class ExamplesResults:
    examples: list[Example]
    query: str
    fullsize: int
    ipm: int
    page_num: int

    @staticmethod
    def parse_sketch_engine_response(response: dict, page_num: int) -> 'ExamplesResults':
        examples = [Example.parse_sketch_engine_line(line) for line in response['Lines']]
        if response['concsize'] > 0:
            return ExamplesResults(examples, response['q'][0], response['fullsize'], response['relsize'], page_num)
        else:
            return ExamplesResults([], response['Desc'][0]['arg'], 0, 0, 0)
    
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Req:
    req_q: Query
    base_url: str
    auth_name: str
    auth_code: str
    interm_url: str = '/search/concordance?' #introduce a method variable later

    def qu_run(self):
        # link = requests.request('GET', url=self.base_url + self.interm_url, params=asdict(self.req_q)|{'corpname': self.req_q.corpname}, auth=(self.auth_name, self.auth_code))
        try:
            received = requests.get(
                self.base_url + self.interm_url,
                params=asdict(self.req_q), auth=(self.auth_name, self.auth_code))
        except Exception as ex:
            raise ConnectionError
        if not received.ok:
            raise ValueError(str(received.content))
        result = received.json()
        if 'error' in result:
            raise ValueError(str(result['error']))
        return result


def get_examples_from_corpus(match: str, corpname: str, n_examples: int, page_num: int=1) -> ExamplesResults:
    cql = CQL(exact_match=match, ignore_capital=False, ends_w_any_punc=True)
    full_query = Query(corpname=corpname, q=cql.form_query(), pagesize=n_examples, fromp=page_num)
    request = Req(req_q=full_query, 
              base_url=config.SKETCHENGINE_BASE_URL, 
              auth_name=config.SKETCHENGINE_USERNAME,
              auth_code=config.SKETCHENGINE_API_KEY)
    try:
        received = request.qu_run()
    except Exception as ex:
        raise ex
    received = ExamplesResults.parse_sketch_engine_response(received, page_num)
    return received

