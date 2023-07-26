from fastapi import FastAPI
import requests
import logging

from model.AutocompleteTerm import AutocompleteTerm
from model.GenericResponse import GenericResponse

app = FastAPI()

logger = logging.getLogger()

@app.get("/")
async def root():
    return {"message": "Autocompare API is running!"}

@app.get("/lowes")
async def lowes(searchTerm: str = '', maxTerms: int = 8):
    base_url = 'https://www.lowes.com'
    path = 'LowesSearchServices/resources/autocomplete/v2_0'
    parameters = f'searchTerm={searchTerm}&maxTerms={maxTerms}'
    full_url = f'{base_url}/{path}?{parameters}'
    print(full_url)
    response = requests.get(full_url, timeout=5)
    print(response.status_code)
    response_text = response.text
    return response_text

def convertAmazonResponseToGeneric(input_dict):
    autocomplete_term_list: list[AutocompleteTerm] = []
    for suggestion in input_dict['suggestions']:
        if suggestion['type'] != 'KEYWORD':
            continue
        autocomplete_term = AutocompleteTerm()
        autocomplete_term.name = suggestion['value']
        autocomplete_term_list.append(autocomplete_term)
    generic = GenericResponse()
    generic.data = autocomplete_term_list
    return generic

@app.get("/amazon")
async def amazon(searchTerm: str = '', maxTerms: int = 8):
    base_url = 'https://origin-completion.amazon.in'
    path = 'api/2017/suggestions'
    default_paramters = 'limit=11&suggestion-type=WIDGET&suggestion-type=KEYWORD&page-type=Gateway&alias=aps&site-variant=desktop&version=3&event=onkeypress&wc=&lop=en_IN&last-prefix=re&avg-ks-time=29966&fb=1&session-id=257-9914362-9137250&request-id=HW69TAMQWTEFNHE269NZ&mid=A21TJRUUN4KGV&plain-mid=44571&client-info=amazon-search-ui'
    parameters = f'{default_paramters}&prefix={searchTerm}'
    full_url = f'{base_url}/{path}?{parameters}'
    response = requests.get(full_url, timeout=5)
    logger.debug(f'response.status_code: {response.status_code}')
    response_dict = response.json()
    generic_response = convertAmazonResponseToGeneric(response_dict)
    return generic_response
