#Baseado em dados da covid19 do ano de 2020
#Formação gráfica em destaques a cidades, geração de gráficos visuais e um qr


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)

raw_data = resp.json()
raw_data[0]

final_data = []
for obs in raw_data:
    final_data.append(obs['Confirmed'], obs['Recovered'], obs['Active'], obs['Date'])

final_data.insert(0, ['confirmados', 'obitos', 'recuperados', 'ativos', 'data'])
final_data

CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]
    final_data

import datetime as dt

print(dt.time(12, 6, 21, 7), 'Hora:minuto:segundo.microsegundo')
print('_ _ _ _')
print(dt.date(2020, 4, 25), 'Ano-mês-dia')
print('_ _ _ _')
print(dt.datetime(2020, 4, 25,12, 6, 21, 7), 'Ano-mês-dia Hora:minuto:segundo.microsegundo')

natal = dt.date(2020, 12, 25)
reveillon = dt.date(2021, 1, 1)

print(reveillon - natal)
print((reveillon -natal).days)
print((reveillon - natal).seconds)
print((reveillon - natal).microseconds)

import csv

with open ('brasil-covid.csv', 'w') as file:
    write = csv.writer(file)
    write.writerows(final_data)

for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y')

def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label' : labels[i],
                'data' : y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]

def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {

        'title': title,
        'display' : display
    }

def create_chart(x, y, labels, kind='bar', title=''):

 datasets = get_datasets(y, labels)
 option = set_title(title)

chart = {
    'type': kind,
    'data': {
       'labels': x,
       'datasets': datasets 
    },
    'options': Options
}



def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    rep = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)

from PIL import Image
from IPython.display import display

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)

y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']
x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data1, y_data_2], labels, title='Gráfico confirmados vs recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeir-grafico.png', chart_content)
display_image('meu-primeiro-grafico.png')

from urllib.parse import quote

def get_api_qrcode(link):
    text = quote(link) #parsing do link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content

url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')
