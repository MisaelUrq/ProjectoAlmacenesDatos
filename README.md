# Generador de mapas

Un generador de mapas donde se muestran las zonas con más escuelas en la zona metropolitana de guadalajara.

Abarcada por estos municipos:  GUADALAJARA, ZAPOPAN, SAN PEDRO TLAQUEPAQUE, TLAJOMULCO DE ZÚÑIGA, TONALÁ, EL SALTO, ZAPOTLANEJO, IXTLAHUACÁN DE LOS MEMBRILLOS, JUANACATLÁN, ACATLÁN DE JUAREZ.

## Integrantes

- Urquieta Estrada, José Misael

## Requerimentos

- Es necesario tener instalado python 3.7 o mayor
- Es necesario hacer pip install con la librería folium y mysql-connector-python (tkinter, webbrowser, json y minidom deberían venir incluidas)
- No mover de lugar los archivos CP\_14Jal\_v2.kml, este archivo contiene las coordenadas y estructura de las zonas según https://datos.gob.mx/busca/dataset/codigos-postales-coordenadas-y-colonias
   - NOTA: tengo dudas respecto a las zonas... pero es lo que hay oficial.

## Como correr
- Desde la consola irse hasta la raíz de la carpeta del projecto 'project'
- Correr _python main.py_
- Aquí aparecera la ventana del programa, donde podremos selecionar el top de zonas que queremos que nos muestre por nivel.

## Notas
- Muchos códigos postales cubren más de una zona nosotros solo tomamos la zona más grande y mostramos esta, aunque esta puede ser un poco más grande (a lo visto por una zona de unas cuadras más en otro lugar)
- Otros códigos postales no muestran toda la extención, un ejemplo sería en 45430, que según puedo ver cubre zapotlanejo, pero las cordenadas solo cubren la calle central.
- Las escuelas cubren varios turnos, por lo que un edificio puede llegar a contar más de una vez, dependiendo de los turnos o modalidades que maneje.
- El mouse puede confudirse al pasar sobre las zonas, ya que en varios niveles puede estar marcada la misma zona, para estar seguros de la información mostrada apague todas las capas que no sea el nivel al que deseé ver.
