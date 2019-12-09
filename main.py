import mysql.connector
from xml.dom import minidom
import json   # Pre install in python 3.7
import folium # Install
import webbrowser # Pre install in python3.7
import tkinter

class ZipCodeCounter:
    def __init__(self, name, count):
        self.name = name
        self.count  = count

class GeoData:
    def __init__(self, cp, coordinates, count):
        self.cp  = cp
        self.coordinates = coordinates
        self.count = count

connection = mysql.connector.connect(host='37.59.55.185', user='WCqgiEsLy3', passwd='I9yyxDyDIJ', database='WCqgiEsLy3')
zmg_query = """ WHERE municipio = 'GUADALAJARA' or municipio = 'ZAPOPAN' or municipio = 'SAN PEDRO TLAQUEPAQUE' or municipio = 'TLAJOMULCO DE ZÚÑIGA' or municipio = 'TONALÁ' or municipio = 'EL SALTO' or municipio = 'ZAPOTLANEJO' or municipio = 'IXTLAHUACÁN DE LOS MEMBRILLOS' or municipio = 'JUANACATLÁN' or municipio = 'ACATLÁN DE JUAREZ' """

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getCP(marker):
    return getText(marker.getElementsByTagName('ExtendedData')[0].getElementsByTagName('SchemaData')[0].getElementsByTagName('SimpleData')[0].childNodes)

def GetGeoJsonData(data):
    number = int(data.cp)%255*1231236%99999
    color = ''
    switch = number % 4
    if switch == 0:
        color = '#f{:05d}'.format(number)
    elif switch == 1:
        color = '#0{:05d}'.format(number)
    elif switch == 2:
        color = '#{:05d}0'.format(number)
    else:
        color = '#{:05d}f'.format(number)
    return {'type': 'Feature', 'properties': {'title':data.cp, 'color': color, 'count':str(data.count)}, 'geometry': {'type':'Polygon', 'coordinates':[data.coordinates]}}

def GenerateGeoJson(geo_list):
    return json.dumps({'type': 'FeatureCollection', 'features':  list(map(GetGeoJsonData, geo_list))}, indent=4)


# This needs to be split by ' ' to get the alt,lng and then create something for that...
def getCoordinates(marker):
    polygons = marker.getElementsByTagName('MultiGeometry')[0].getElementsByTagName('Polygon')
    largest = getText(polygons[0].getElementsByTagName('outerBoundaryIs')[0].getElementsByTagName('LinearRing')[0].getElementsByTagName('coordinates')[0].childNodes)
    largest_x = len(largest)

    for polygon in polygons:
        element = getText(polygon.getElementsByTagName('outerBoundaryIs')[0].getElementsByTagName('LinearRing')[0].getElementsByTagName('coordinates')[0].childNodes)
        x = len(element)
        if largest_x < x:
            largest = element
            largest_x = x

    return list(map(lambda x: [float(x.split(',')[0]),float(x.split(',')[1])],largest.split(' ')))


def CrearMap(limit):
    cursor = connection.cursor()

    cursor.execute("show tables")
    table_names = cursor.fetchall()
    zip_locations = minidom.parse('CP_14Jal_v2.kml')
    placemarkers = zip_locations.getElementsByTagName('Placemark')
    m = folium.Map(location=[20.666667,-103.333333], zoom_start=13)

    for table in table_names:
        zip_codes = {}
        if table[0] == 'primaria':
            cursor.execute("""SELECT cp, Count(cp) c FROM {0} {1} GROUP BY cp order by c desc LIMIT {2}""".format(table[0], zmg_query, limit))
        elif table[0] == 'secundaria' or table[0] == 'preparatoria':
            cursor.execute("""SELECT codigo_postal, Count(codigo_postal) c FROM {0} {1} GROUP BY codigo_postal order by c desc LIMIT {2}""".format(table[0], zmg_query, limit))
        else:
            continue
        table_info = cursor.fetchall();

        for info in table_info:
            if zip_codes.get(info[0]) == None:
                zip_codes[info[0]] = info[1]
            else:
                zip_codes[info[0]] += info[1]

        sorted_codes = []
        def IsCPInPlacemarker(marker):
            cp = getCP(marker)
            for code in sorted_codes:
                if code.name == cp:
                    return GeoData(cp, getCoordinates(marker), code.count)

        for item in zip_codes.items():
            sorted_codes.append(ZipCodeCounter(item[0], item[1]))
        sorted_codes = sorted(sorted_codes, key=lambda x: x.count, reverse=True)

        geo_list = list(map(IsCPInPlacemarker, placemarkers))
        geo_list = [x for x in geo_list if x is not None]

        f = open('{}.json'.format(table[0]), 'w')
        f.write(GenerateGeoJson(geo_list))
        f.close()

        style_function = lambda x: {'fillColor': x['properties']['color'] }
        geo = folium.GeoJson('{}.json'.format(table[0]),
                             name=table[0],
                             style_function=style_function,
                             tooltip=folium.GeoJsonTooltip(fields=['title', 'count'],
                                                           aliases=['Codigo postal', 'Número de escuelas']))
        sorted_codes.clear()
        geo.add_to(m)

    folium.LayerControl().add_to(m)
    m.save(outfile='datamap.html')
    webbrowser.open('datamap.html')

if __name__=='__main__':
    window = tkinter.Tk()
    window.title('Zona de escuelas')
    window.geometry('390x200')

    title_label = tkinter.Label(window, text='Marcador de zonas de escuela')
    title_label.grid(column=1,row=0)

    schools_label = tkinter.Label(window, text='Número de escuelas por nivel: ')
    schools_label.grid(column=0,row=1)
    schools_count = tkinter.Entry(window, width=10)
    schools_count.grid(column=1,row=1)

    error_label = tkinter.Label(window, text='N/A')

    def ClickEvent():
        limit = 10
        try:
            limit = int(schools_count.get())
            CrearMap(limit)
        except:
            error_label.configure(text='La entrada tiene \nque ser un número')

    button = tkinter.Button(window, text='Crear mapa', command=ClickEvent)
    button.grid(column=1,row=3)
    info_label = tkinter.Label(window, text='*Este programa cuenta cuantas escuelas\n existen por zona de código postal\n y marca las zonas con \nmayor número de escuelas\nen un mapa en html')
    info_label.grid(column=0,row=3)

    info_label2 = tkinter.Label(window, text='**Muchas dependencias cuentan turnos\n como diferentes escuelas')
    info_label2.grid(column=0,row=4)
    error_label.grid(column=1,row=4)

    window.mainloop()
