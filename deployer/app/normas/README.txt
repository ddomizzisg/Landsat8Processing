Requerimientos:
	- python 3.9.4
	- pip 21.3

Bibliotecas:
	- networkx (pip install networkx)
	- matplotlib (pip install matplotlib)
	- request (pip install requests, python -m pip install requests)
	- pyyaml (pip install pyyaml)
	- texttable (pip install texttable)
	- plotly.graph_objects (pip install plotly==5.3.1 and pip install -U kaleido)

************************************************************************
				Comando de ejecución del programa
************************************************************************
python main.py _input_path _output_path
************************************************************************

Donde:
	_input_path: es el directorio donde se toman las entradas del programa. Cada directorio dentro de _input_path es interpretado como un sistema de eSalud que debe contener únicamente los archivos .cfg .json y .yml
	_output_path: es el directorio en donde se genera la salida del programa (genera un reporte, el DAG del flujo trabajo descubierto y un gráfico tipo velocímetro con el porcentaje de cumplimiento por cada norma. Todo lo anterior dentro de un directorio (un directorio de salida por cada sistema de eSalud detectado en el directorio _input_path))


Ejemplo de comando de ejecución:
python main.py input output

