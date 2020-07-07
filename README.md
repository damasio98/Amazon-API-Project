# <center>Projeto Final</center> 
### <center>Eletrónica Digital e Microprocessadores</center>
#### <center>José Damásio Tavares</center>
**<center>up201603301</center>** 
***
## Indice
1. [Objetivos](#Objetivos)
2. [Introdução](#Introdução)
3. [Desenvolvimento do Projeto](#Desenvolvimento)
    1. [Visão Geral](#Overview)
    2. [Escolha do API](#API)
    3. [Código](#Codigo)
4. [Conclusão](#Conclusão)
5. [Webgrafia](#Webgrafia)
***

## Objetivos <a name="Objetivos"></a>

* Utilizar a funcionalidade de wifi do ESP32 para criar uma ligação com um servidor do serviço REST. O API escolhido irá-nos indicar o preço atual de um produto na Amazon.

* A partir da informação obtida, interagir com os leds e botões da placa.

## Introdução <a name=Introdução></a>

A Amazon é considerada o maior armazém e _retailer_ do mundo. O seu catálogo é composto pelos mais variados produtos, desde decoração da casa, livros, roupa e o maior de todos, tecnologia. A tecnologia é o seu foco e o facto de a vender a um preço muitas vezes mais acessível do que as lojas físicas do próprio país tornou a Amazon numa das empresas mais valiosas do mundo. Assim sendo e falando por experência pessoal, é algo comum esperar por uma promoção e ir acompanhando o preço de um produto que se deseja obter.  
Na Europa, a Amazon possui 5 lojas virtuais (agora 4, devido ao _Brexit_). No entanto, é possível comprar em qualquer destas lojas e enviar para Portugal, algo que acontece frequentemente visto existir muito mais oferta e os preços serem mais acessíveis quando comparados aos praticados nas lojas portuguesas.
Um dos principais objetivos deste projeto é estabelecer uma ligação bem sucedida com um API. Para isso, é necessário primeiro escolher um que esteja de acordo com o que queremos desenvolver.  
Devido a isto, o meu projeto consiste num API que fornece o preço atual de um produto e conforme o mesmo, a placa oferece uma resposta fazendo uso dos LEDs.

***
## Desenvolvimento do Projeto <a name="Desenvolvimento"></a>

### Visão Geral <a name="Overview"></a>

A finalidade do projeto é ser um _tracker_ do preço de determinado produto da Amazon. O utilizador estabelece um valor mínimo que está disposto a pagar pelo produto e  em qual loja virtual deseja pesquisar o preço. Também insere qual o preço habitual do produto.  
Como já foi referido acima, o objetivo do API é obter o preço atual de determinado produto. Após isso, o código analisa o preço atual e caso esteja abaixo ou igual ao preço minimo, acende o LED verde. No caso de estar acima, acende o LED vermelho.
O LED amarelo também tem uma função. É estabelecido um intervalo acima do preço mínimo para o qual este acende. É mais intuitivo se explicar usando um exemplo.  
Vamos imaginar que o preço habitual do produto (inserido pelo utilizador) é de 100€.  
O preço minimo que o utilizador quer pagar é 80€. O intervalo estabelico é 20% da diferença entre estes dois preços. Então neste caso, os LEDs funcionariam da seguinte forma:

* LED Verde acende se preço <= 80€.
* LED Amarelo acende se  80€ < preço <=84€
* LED Vermelho acende se preço > 84€ 

Estabeleci este intervalo de forma a existir uma margem de tolerância (quem está disposto a pagar 80€, também estará disposto a pagar 81€).

Além destas funçoes, outras funções esperadas da placa seria o uso dos butões. O botão esquerdo serviria para executar o API enquanto o direito serviria para alterar entre lojas virtuais (mudar da loja Espanhola para a Italiana, como exemplo).

### Escolha do API <a name="API"> </a>

Incialmente tentei encontrar um API oficial da Amazon, mas depois de alguma pesquisa percebi que é necessário uma conta de vendedor na amazon para ter acesso ao mesmo. Após isso, procurei por APi's de terceiros. O primeiro que encontrei foi o [Rainforest API](https://rainforestapi.com/). A conta _free_ dava acesso a 100 pedidos e returnava toda a informação do produto, o que se tornou num problema. O ficheiro json recebido continha tanta informação (mais de 100 linhas de resposta) que recebia a seguinte mensagem como erro:
_<center>memory allocation failed, allocating 19184 bytes</center>_  
A memória flash do ESP32 não era suficiente para tanta informação e apesar de eu inserir alguns comandos _gc.collect_ (comando que liberta memória que contém dados desnecessários) ao longo do código, este só funcionava 1 em cada 5 vezes e por isso decidi abandonar este API.    
Ao procurar outro API, tentei-me focar num que só retornasse o preço e não outra informação que não me era útil.
Após alguma pesquisa consegui encontrar o [Amazon Price](https://rapidapi.com/ajmorenodelarosa/api/amazon-price1) que oferece 150 pedidos gratuitos por mês. Este API apenas retorna informação relacionado com o preço, o que é ideal visto que só preciso do valor do preço atual.
O API recebe os seguintes parâmetros: 

&nbsp; 1. Loja virtual a aceder ('ES','DE','IT', entre outras)  
&nbsp; 2. ASIN do produto (que é comum a todas as lojas e encontra-se no link)  
![Onde encontrar o ASIN](https://raw.githubusercontent.com/damasio98/edm_proj_final/master/ASIN.PNG?token=APT2DNIPAOYKONYDIADMLNC7ASCYK)
&nbsp; 3. Chave do API  

### Código <a name="Codigo"></a>

O código exclusivo para o API revelou-se um desafio, pois não era oferecido um URL completo, mas sim um código em python que teve de ser adaptado para Micropython (_urequests_ apresenta diferenças quando comparado com o seu fundador _requests_). Após acertar todos os pormenores, consegui obter o ficheiro json. No código final, abstive-me de atribuir um print ao ficheiro já que não é necessário termos todas as informações fornecidas.

Após construir o código para os LEDS, que já foi explicado na [Visão Geral](#Overview) e verificar que funcionava decidi testar uma nova função no código. O API só fornece o preço numa loja virtual, mas é possível que o utilizador queira comparar com várias lojas virtuais. Então o objetivo seria o código correr 5 vezes, por 5 lojas virtuais e retornar os seus valores. Os LEDs funcionariam conforme o preço mais baixo. Criei uma função que corria 5 ciclos, alterando apenas o parâmetro _'ES','IT',etc..._ O preço de cada loja seria _append_ a uma lista e no final o microcontrolador apresentava todos os valores.
No entanto, após criar o código necessário deparei-me com um novo erro:
_<center>wifi: bcn_timout,ap_probe_send_start</center>_

Resumidamente, o esp32 desligava-se da internet o que fazia com o API falhase. Falarei mais a fundo deste erro à frente, visto que o mesmo volta a aparecer.

Após isto, decidi focar-me nos botões de forma a incorporar ao máximo todos os componentes que tinha comigo.
Utilizando o que foi aprendido no trabalho do "Semáforo", criei o seguinte para os 2 botões:

    paises = ['ES','IT','DE','FR','GB']
    j=paises.index(país)
    if button_right.value()==0:
        sleep_ms(11)
    if país == 'GB':  
        país = 'ES'
    else:
        país = paises[j+1] 

    if button_left.value()==0:
        sleep.ms(11)
        Amazon()

Na primeira parte, podemos verificar que sempre que carregamos no botão direito, muda o domínio da loja virtual.
Já no segundo, toda o API e os respetivos comandos encontram-se dentro de uma função que denominei Amazon(). Ao carregar no botão esquerdo, a função percorre o seu ciclo e retorna os resultados. O código apesar de aparentar estar correto, apresenta o mesmo problema:

_<center>wifi: bcn_timout,ap_probe_send_start</center>_

Após várias pesquisas sobre este erro e o que significa, cheguei a várias conclusões:
 
&nbsp; 1. Devido ao elevado número de _threads_ já existentes sobre este problema, é um erro comum do ESP32 e que ainda não tem solução fornecida pela _ESPRESSIF_.

&nbsp; 2. O erro origina de 2 situações: a primeira é uma falha de memória flash quando o microcontrolador se encontra a realizar várias operações. A segunda situação é que ao realizar várias _"flash write"_ o esp32 "tranca-se" e suspende todas as outras tarefas, incluindo o Wi-fi. Isto leva a que perca a conecção e por isso o código do API seja interrompido ([explicação fornecida por um representante da ESPRESSIF](https://www.esp32.com/viewtopic.php?t=6800&p=29472)).

&nbsp; 3. Uma possível solução seria acrescentar um taskdelay ou sleepms() de 11 milisegundos. Isto faria com que o microcontrolador tivesse tempo de fazer todas as suas tarefas. Infelizmente, embora esta solução ajudasse e me permitisse obter resultados ocasionalmente, não chegava a ser nem 50% fiável.

Infelizmente, até à data de entrega do projeto não consegui encontrar uma solução para estes 2 problemas. Devido a isso, decidi manter o meu código mais simples só trabalhando com o API e com os LEDS. No entanto, acrescentei estes 2 códigos ao _github_ numa pasta à parte visto estarem a nivel técnico corretos. O código que percorria as 5 lojas encontra-se fora do _"src"_ com o nome "Codigo Extra - 5 Lojas" e o que interagia com os botões tem o nome "Codigo Extra - Botoes".
***
## Conclusão <a name="Conclusão"></a>

Os objetivos principais do projeto foram cumpridos. Consegui de forma bem sucedida trabalhar com um API e integrá-lo com alguns componentes da placa. 

Infelizmente não consegui usar o número de componentes que pretendia. Além disso, o facto de não conseguir aceder a todas as lojas em um só _compile_ também acabou por tornar o projeto em algo mais simples do que inicialmente ambicionado.

Apesar de considerar que o resultado final é positivo e que me permitiu perceber muito melhor o comportamento de um ESP32, deixa um sabor amargo não ter conseguido elevar o projeto ao nível pretendido.



