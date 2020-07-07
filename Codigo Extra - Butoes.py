import gc       #recolhe e elimina dados desnecessários da memória flash
gc.collect()
import urequests as requests
gc.collect()
from parametros import ASIN, país, preço_ideal, preço_atual #condições estabelecidas pelo utilizador
gc.collect()
from secrets import api_key
from ujson import dumps #só irá ser usado no caso de fazermos print do ficheiro json
gc.collect()
from machine import Pin
from formatar import formatar
from sleep import sleep_ms

led_red = Pin(21, Pin.OUT)
led_red.value(False)
led_green = Pin(19, Pin.OUT)
led_green.value(False)
led_yellow = Pin(22, Pin.OUT)
led_yellow.value(False)
button_left = Pin(23, Pin.IN, Pin.PULL_UP)
button_right = Pin(18, Pin.IN, Pin.PULL_UP)

gc.collect()

paises = ['ES','IT','DE','FR','GB']
j=paises.index(país)

while True:
    sleep_ms(11)
    if button_right.value()==0:
        sleep_ms(11)
    if país == 'GB':
        país = 'ES'
    else:
        país = paises[j+1]

    def Amazon():

        url = "https://amazon-price1.p.rapidapi.com/priceReport?asin={0}&marketplace={1}" \
        .format(ASIN, país)

        headers = {
            'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
            'x-rapidapi-key': api_key
        }

        resposta = requests.get(url, headers=headers).json()
        #print(formatar(dumps(resposta))) #visto não ser necessário ao programa imprimir o ficheiro

        preço = resposta['prices']['priceAmazon']/100 #o preço é dado em cêntimos e por isso converto para euros
        gc.collect()

        diferença = (preço_atual - preço_ideal)/5

        if preço > preço_ideal+diferença:
            led_red.value(True)

        elif preço <= preço_ideal+diferença and preço > preço_ideal:
            led_yellow.value(True)

        elif preço <= preço_ideal:
            led_green.value(True)

        url_tp = 'https://tropicalprice.com/product/{0}'\
        .format(ASIN)

        gc.collect()

        print('')
        print('Amazon {0}'\
        .format(país))
        print('{0}:'\
        .format(resposta['title']))
        print('{0}€'\
        .format(resposta['prices']['priceAmazon']/100))
        print('Compara aqui o preco da Amazon {0} com as outras lojas europeias:'\
        .format(país))
        print(url_tp)
        print('')
        sleep_ms(11)

    if button_left.value()==0:
        sleep.ms(11)
        Amazon()