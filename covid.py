#!/usr/bin/env python3

import json, matplotlib.pyplot, numpy


def save_plot_img(array, title, img_file, average=None):
    matplotlib.pyplot.figure(figsize=(14, 8), dpi=100)
    matplotlib.pyplot.plot(array)
    if not average is None:
        matplotlib.pyplot.plot(average)
    matplotlib.pyplot.title(title)
    matplotlib.pyplot.savefig(img_file)


def moving_average(x, w):
    return numpy.convolve(x, numpy.ones(w), 'valid') / w

#with open("COVID-19/dati-json/dpc-covid19-ita-regioni.json") as fd:
with open("COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json") as fd:
    covid_data = json.load(fd)

data = [i['data'] for i in covid_data]
tamponi = [i['tamponi'] for i in covid_data]
tamponi_giorno = [i-j for i,j in zip(tamponi,[0] + tamponi[:-1])]
nuovi_positivi = [i['nuovi_positivi'] for i in covid_data]
tasso_positivita = [i/j*100 for i,j in zip(nuovi_positivi, tamponi_giorno)]
ricoverati_con_sintomi = [i['ricoverati_con_sintomi'] for i in covid_data]
terapia_intensiva = [i['terapia_intensiva'] for i in covid_data]
deceduti = [i['deceduti'] for i in covid_data]
deceduti_giorno = [i-j for i,j in zip(deceduti,[0] + deceduti[:-1])]

for i in range(len(covid_data)):
    print(f'{i:5} {data[i]:15}'
            f'{tamponi_giorno[i]:10}'
            f'{nuovi_positivi[i]:10}'
            f'{tasso_positivita[i]:8.2f}'
            f'{ricoverati_con_sintomi[i]:7}'
            f'{terapia_intensiva[i]:7}'
            f'{deceduti_giorno[i]:7}')

last_days = 90

save_plot_img(nuovi_positivi, 'Nuovi Positivi Giornalieri',
        'nuovi_positivi.png')
save_plot_img(tamponi_giorno, 'Tamponi Giornalieri', 'tamponi_giorno.png')
save_plot_img(tasso_positivita, 'Tasso Positivita\'', 'tasso_positivita.png')
save_plot_img(deceduti_giorno, 'Deceduti Giornalieri', 'deceduti_giorno.png')
save_plot_img(nuovi_positivi[-last_days:],
        f'Nuovi Positivi Giornalieri Ultimi {last_days} Giorni',
        'nuovi_positivi_last.png',
        moving_average(nuovi_positivi, 7)[-last_days:]) 
save_plot_img(tamponi_giorno[-last_days:], 
        f'Tamponi Giornalieri Ultimi {last_days} Giorni',
        'tamponi_giorno_last.png',
        moving_average(tamponi_giorno, 7)[-last_days:]) 
save_plot_img(tasso_positivita[-last_days:], 
        f'Tasso Positivita\' Ultimi {last_days} Giorni',
        'tasso_positivita_last.png',
        moving_average(tasso_positivita, 7)[-last_days:]) 
save_plot_img(deceduti_giorno[-last_days:], 
        f'Deceduti Giornalieri Ultimi {last_days} Giorni',
        'deceduti_giorno_last.png',
        moving_average(deceduti_giorno, 7)[-last_days:]) 

with open('covid.html', 'w') as html_file:
    html_file.write('''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>COVID</title>
  </head>
  <body>
    <div>
        <img src='nuovi_positivi.png'>
    </div>
    <div>
        <img src='tamponi_giorno.png'>
    </div>
    <div>
        <img src='tasso_positivita.png'>
    </div>
    <div>
        <img src='deceduti_giorno.png'>
    </div>
    <div>
        <img src='nuovi_positivi_last.png'>
    </div>
    <div>
        <img src='tamponi_giorno_last.png'>
    </div>
    <div>
        <img src='tasso_positivita_last.png'>
    </div>
    <div>
        <img src='deceduti_giorno_last.png'>
    </div>
  </body>
</html>
''')
