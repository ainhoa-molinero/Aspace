from django.shortcuts import render
from usuarios.models import Usuario, UsuariosTable, Sesion, SesionTable, Juego
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Sum, Avg
from datetime import date, datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models.functions import Concat
from django.db.models import F, Value

COLORS = ['#f7a35c', '#7cb5ec', "#f15c80", "#90ed7d", "#434348", "#8085e9", "#e4d354", "#2b908f", "#f45b5b", "#91e8e1"]

def random_colors(colors=COLORS):
    from random import shuffle
    shuffle(colors)
    return(colors)

def json_example(request):
    return render(request, 'graficas/ver_grafica.html')

def filter_usuario(obj, id_usuario):
    # Filtrado de usuario
    if id_usuario and type(id_usuario) is list:
        # Lista de usuarios
        obj = obj.filter(id_usuario__in=id_usuario)
    elif id_usuario and type(id_usuario) is str:
        # Un único usuario
        obj = obj.filter(id_usuario=id_usuario)
    else:
        # Todos los usuarios
        obj = obj

    return(obj)


def get_pie_graph(request, id_usuario=None):
    obj = Sesion.objects.all()
    obj = filter_usuario(obj, id_usuario)

    obj = obj.values('id_juego','aciertos','fallos')

    res = obj.aggregate(Aciertos=Sum('aciertos'), Fallos=Sum('fallos'))
    data = [{'name':k, 'y':v} for k,v in res.items()]
    #data = [{'name':k, 'data':v} for k,v in res.items()]

    chart = {
        'chart': {
            'plotBackgroundColor': None,
            'plotBorderWidth': None,
            'plotShadow': False,
            'type': 'pie'
        },
        'colors': COLORS,
        'title': {
            'text': 'Aciertos vs. fallos totales'
        },
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'accessibility': {
            'point': {
                'valueSuffix': '%'
            }
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        'series': [{
            'name': 'Aciertos vs. fallos',
            'colorByPoint': True,
            'data': data
        }]
    }
    return JsonResponse(chart)


def get_time_graph(request):
    '''Gráfica con tiempo medio para cada usuario a lo largo de un periodo'''
    fecha_inicial = '2021-07-01'
    fecha_final = '2021-12-30'

    data = Sesion.objects.values('id_usuario__nombre','id_usuario__apellido','fecha', 'tiempo_medio')\
        .annotate(trunc_fecha=TruncDate('fecha'))\
        .values('id_usuario__nombre','id_usuario__apellido','trunc_fecha', 'tiempo_medio')\
        .filter(trunc_fecha__range=[fecha_inicial, fecha_final])\
        .order_by('trunc_fecha')

    # --- Crear lista con el rango de fechas ----
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
    end_dt = datetime.strptime(fecha_final, '%Y-%m-%d').date()
    dias_dicc = {}
    for dt in daterange(start_dt, end_dt):
        dias_dicc[dt.strftime("%d/%m/%Y")] = None

    series_dicc = {}
    for i in data:
        usuario = i['id_usuario__nombre']+' '+i['id_usuario__apellido']
        fecha = i['trunc_fecha'].strftime("%d/%m/%Y")
        cuenta = i['tiempo_medio']
        if usuario not in series_dicc.keys():
            series_dicc[usuario] = {
                'name':usuario,
                'data':dias_dicc.copy()
            }
            series_dicc[usuario]['data'][fecha] = cuenta
        else:
            if series_dicc[usuario]['data'][fecha] is not None:
                series_dicc[usuario]['data'][fecha] += cuenta
            else:
                series_dicc[usuario]['data'][fecha] = cuenta


    series_dicc_final = {}
    for k in series_dicc.keys():
        series_dicc_final[k] = {
            'name':series_dicc[k]['name'],
            'data':list(series_dicc[k]['data'].values())
        }



    chart = {
        'chart': {
            'type':'line',
            # 'height': 600,
            'zoomType':'x',
            # 'spacingRight':20
        },
        'colors': COLORS,
        'title': {
            'text': f'Proporción de variantes ({fecha_inicial}|{fecha_final})'
        },
        'subtitle': {
            'text': f'Haz click y arrastra para hacer zoom sobre una zona.'
        },
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        'xAxis': {
            'categories': list(dias_dicc.keys())
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:10px"><strong>{point.key}</strong></span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{series.name}:</strong> </td>' +
                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> ({point.percentage:.0f}%) </td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'backgroundColor':'#FFFFFF',
            'useHTML': True
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True
                }
            },
            'series': {
                'animation': False,
                'connectNulls':True
            }
        },
        'credits':'JEJEJEJE',
        'series': list(series_dicc_final.values())
    }

    return JsonResponse(chart)


def get_game_time_graph(request, id_usuario=None):
    '''Gráfica con tiempo medio para cada juego a lo largo de un periodo'''
    fecha_inicial = '2021-07-01'
    fecha_final = '2021-12-30'

    obj = Sesion.objects.all()
    obj = filter_usuario(obj, id_usuario)

    data = obj.values('id_juego__nombre_juego','fecha', 'tiempo_medio')\
        .annotate(trunc_fecha=TruncDate('fecha'))\
        .values('id_juego__nombre_juego','trunc_fecha', 'tiempo_medio')\
        .filter(trunc_fecha__range=[fecha_inicial, fecha_final])\
        .order_by('trunc_fecha')

    # --- Crear lista con el rango de fechas ----
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
    end_dt = datetime.strptime(fecha_final, '%Y-%m-%d').date()
    dias_dicc = {}
    for dt in daterange(start_dt, end_dt):
        dias_dicc[dt.strftime("%d/%m/%Y")] = None

    series_dicc = {}
    for i in data:
        juego = i['id_juego__nombre_juego']
        fecha = i['trunc_fecha'].strftime("%d/%m/%Y")
        cuenta = i['tiempo_medio']
        if juego not in series_dicc.keys():
            series_dicc[juego] = {
                'name':juego,
                'data':dias_dicc.copy()
            }
            series_dicc[juego]['data'][fecha] = cuenta
        else:
            if series_dicc[juego]['data'][fecha] is not None:
                series_dicc[juego]['data'][fecha] += cuenta
            else:
                series_dicc[juego]['data'][fecha] = cuenta


    series_dicc_final = {}
    for k in series_dicc.keys():
        series_dicc_final[k] = {
            'name':series_dicc[k]['name'],
            'data':list(series_dicc[k]['data'].values())
        }



    chart = {
        'chart': {
            'type':'line',
            # 'height': 600,
            'zoomType':'x',
            # 'spacingRight':20
        },
        'colors': COLORS,
        'title': {
            'text': f'Gráfica con tiempo medio para cada juego'
        },
        'subtitle': {
            'text': f'Subtitulo'
        },
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        'xAxis': {
            'categories': list(dias_dicc.keys())
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:10px"><strong>{point.key}</strong></span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{series.name}:</strong> </td>' +
                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> ({point.percentage:.0f}%) </td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'backgroundColor':'#FFFFFF',
            'useHTML': True
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True
                }
            },
            'series': {
                'animation': False,
                'connectNulls':True
            }
        },
        'credits':'JEJEJEJE',
        'series': list(series_dicc_final.values())
    }

    return JsonResponse(chart)


def get_user_results_time_graph(request, id_usuario=None):
    '''Gráfica con aciertos y fallos a lo largo de un período'''
    fecha_inicial = '2021-07-01'
    fecha_final = '2021-12-30'

    obj = Sesion.objects.all()
    obj = filter_usuario(obj, id_usuario)

    data = obj.values('id_usuario','fecha','aciertos','fallos')\
        .annotate(trunc_fecha=TruncDate('fecha'))\
        .values('id_usuario','trunc_fecha','aciertos','fallos')\
        .filter(trunc_fecha__range=[fecha_inicial, fecha_final])\
        .order_by('trunc_fecha')

    # --- Crear lista con el rango de fechas ----
    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
    end_dt = datetime.strptime(fecha_final, '%Y-%m-%d').date()
    dias_dicc = {}
    for dt in daterange(start_dt, end_dt):
        dias_dicc[dt.strftime("%d/%m/%Y")] = None

    series_dicc = {}
    for i in data:
        for name, atribute in {'Aciertos':'aciertos','Fallos':'fallos'}.items():
            name = name
            fecha = i['trunc_fecha'].strftime("%d/%m/%Y")
            cuenta = i[atribute]
            if name not in series_dicc.keys():
                series_dicc[name] = {
                    'name':name,
                    'data':dias_dicc.copy()
                }
                series_dicc[name]['data'][fecha] = cuenta
            else:
                if series_dicc[name]['data'][fecha] is not None:
                    series_dicc[name]['data'][fecha] += cuenta
                else:
                    series_dicc[name]['data'][fecha] = cuenta

    series_dicc_final = {}
    for k in series_dicc.keys():
        series_dicc_final[k] = {
            'name':series_dicc[k]['name'],
            'data':list(series_dicc[k]['data'].values())
        }

    chart = {
        'chart': {
            'type':'line',
            # 'height': 600,
            'zoomType':'x',
            # 'spacingRight':20
        },
        'colors': COLORS,
        'title': {
            'text': f'Aciertos vs. fallos por día' # ({fecha_inicial}|{fecha_final})
        },
        'subtitle': {
            # 'text': f'Haz click y arrastra para hacer zoom sobre una zona.'
        },
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        'xAxis': {
            'categories': list(dias_dicc.keys())
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:10px"><strong>{point.key}</strong></span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{series.name}:</strong> </td>' +
                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> ({point.percentage:.0f}%) </td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'backgroundColor':'#FFFFFF',
            'useHTML': True
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True
                }
            },
            'series': {
                'animation': False,
                'connectNulls':True
            }
        },
        'credits':'JEJEJEJE',
        'series': list(series_dicc_final.values())
    }

    return JsonResponse(chart)




def get_col_graph(request, id_usuario=None):
    '''Gráfica con proporción de aciertos en cada juego'''
    fecha_inicial = '2021-07-01'
    fecha_final = '2021-12-30'

    # Filtrar por usuario/s
    obj = Sesion.objects.all()
    obj = filter_usuario(obj, id_usuario)

    data = obj.values('id_usuario','id_juego__nombre_juego','aciertos','fallos','fecha','rondas')\
        .filter(fecha__range=[fecha_inicial, fecha_final])\
        .values('id_usuario','id_juego__nombre_juego','aciertos','fallos','rondas')

    juegos = list(data.values_list('id_juego__nombre_juego',flat=True).distinct())

    # Diccionario objetivo
    dicc_objetivo = {
        'Aciertos':{
            'name': 'Aciertos',
            'data': []
        },
        'Fallos':{
            'name': 'Fallos',
            'data': []
        }
    }
    # Para cada juego, se hace el sumatorio de aciertos, fallos y rondas y se game_time_graph
    # en la lista 'data' de dicc_objetivo en el mismo orden que aparezcan los nombres de juegos en xAxis
    for j in juegos:
        d = data.filter(id_juego__nombre_juego=j)
        d = d.aggregate(Aciertos=Sum('aciertos'), Fallos=Sum('fallos'), Rondas=Sum('rondas'))
        dicc_objetivo['Aciertos']['data'].append(round(d['Aciertos']/d['Rondas'], 2))
        dicc_objetivo['Fallos']['data'].append(round(d['Fallos']/d['Rondas'], 2))

    chart = {
        'chart': {
            'type': 'column'
        },
        'colors': COLORS,
        'title': {
            'text': 'Proporción de aciertos y fallos por ronda'
        },
        'xAxis': {
            'categories': list(juegos)
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Proporción'
            },
            'stackLabels': {
                'enabled': True,
            }
        },
        'tooltip': {
            'headerFormat': '<b>{point.x}</b><br/>',
            'pointFormat': '{series.name}: {point.y}'
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True
                }
            }
        },
        'series': list(dicc_objetivo.values())
    }
    return JsonResponse(chart)
