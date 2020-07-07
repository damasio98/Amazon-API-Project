#Este código seria para percorrer as 5 lojas virtuais europeias de uma só vez
import gc
gc.collect()
import urequests as requests
gc.collect()
from parametros import ASIN, preço_ideal, preço_atual
gc.collect()
from ujson import dumps
from secrets import api_key
gc.collect()
from machine import Pin

led_red = Pin(21, Pin.OUT)
led_red.value(False)
led_green = Pin(19, Pin.OUT)
led_green.value(False)   
led_yellow = Pin(22, Pin.OUT)
led_yellow.value(False)

gc.collect()

preços = []
produto = []

def Amazon():
  i = 0
  if i == 0:
    país = 'ES'
  elif i == 1:
    país = 'FR'
  elif i == 2:
    país = 'IT'
  elif i == 3:
    país = 'DE'
  elif i == 4:
    país = 'GB'

  url = "https://amazon-price1.p.rapidapi.com/priceReport?asin={0}&marketplace={1}" \
    .format(ASIN, país)

  headers = {
      'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
      'x-rapidapi-key': api_key
  }
  resposta = requests.get(url, headers=headers).json()
  i += 1

  preços.append(resposta['prices']['priceAmazon']/100)
  produto.append(resposta['title'])


while len(preços) != 5: #obriga a função a correr 5 vezes, cada vez com um dominio diferente
  Amazon()
  gc.collect()

preços[4] = preços[4]*1.1 #transformar o pound inglês em euros

print(produto[0])
print('Espanha\tFrança\tItália\tAlemanha\tReino Unido')
print(preços[0], '€\t', preços[1], '€\t', preços[2], '€\t', preços[3], '€\t', preços[4])


preços.sort() #necessário para acender os leds de forma correta

diferença = (preço_atual - preço_ideal)/5

if preços[0] > preço_ideal+diferença:
  led_red.value(True)

elif preços[0] <= preço_ideal+diferença and preços[0] > preço_ideal:
  led_yellow.value(True)

elif preços[0] <= preço_ideal:
  led_green.value(True)