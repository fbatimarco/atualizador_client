import logging
import pickle
import http.client
import json
from datetime import datetime
import urllib.request
import Constants
import sys
sys.path.insert(1, '/home/pi/caixa-magica/')
from sincronismo import req as sincronismo

class HttpConnection():
        
    def __init__(self):
        pass
    
    #Obter os dados da inicialização diária    
    def get_inicializacao_diaria(self, chave_acesso):
        connection = http.client.HTTPSConnection(Constants.URL_BASE_SERVER_INIT_MATRIZ)
        now = datetime.now()
        #URL ENCODE - %20 - Space E %2f para / - Apenas para Data e Hora 
        time_now = urllib.parse.quote(now.strftime('%d/%m/%Y %H:%M:%S'),safe='')
        query = str(Constants.HTTPS)+str(Constants.URL_BASE_SERVER_INIT_MATRIZ) + str(Constants.URL_MIDDLE_API)+ str('/') + str(chave_acesso) + str('/') + str(time_now)
        print('Url completa: ',  query)
        connection.request('GET', query)
        
        response = connection.getresponse()
        text = json.dumps(response.read().decode("utf-8"))
        data = json.loads(text)
        data = json.loads(data)

        return data

    def put_requisicao_instalacao(self, dados_instalacao):
        # connection = http.client.HTTPConnection(Constants.URL_BASE_SERVER_INSTALL)
        
        # values = json.dumps(dados_instalacao.__dict__)
        # json_data = json.dumps(values)
        
        # query = str(Constants.HTTPS) + str(Constants.URL_BASE_SERVER_INSTALL) + str(Constants.URL_MIDDLE_API)
        # print('Url completa: ',  query)
        # headers = {'content-type': 'application/json-patch+json'}
        # connection.request("PUT", query, json_data, headers=headers)
        # print(json_data)
        # response = connection.getresponse()
        # print(response.read())
        # text = json.dumps(response.read().decode("utf-8"))
        # data = json.loads(text)
        # data = json.loads(data)

        req = sincronismo.instalacao(dados_instalacao.num_serie, dados_instalacao.veiculo)
        print(req)
        print(req.json())
        return req.json()


