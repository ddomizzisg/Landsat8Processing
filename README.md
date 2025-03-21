# Dagon* Landsat 8 corrections

Flujo de trabajo que corrije y obtiene productos derivados de imagenes satelitales Landsat8.

Etapas del flujo: descompresión, correcciones+productos derivados, parsing+indexing

Descargar imagenes satelitales ```Landsat8``` de https://earthexplorer.usgs.gov/

### Services

Available services are in the ```stages``` directory. The most relevant are the following:

*  ```uncompres```: a simple container with TAR installed to uncompress the images.
*  ```atmospheric```: contains an application to perform atmospheric corrections over scenes.
* ```radiometric```: performs radiometric corrections over the scenes.
* ```derivatives```: produces NDWI and NDVI indexes from the bands of a image.
* ```crop```: crop the bands of a image to an specific region specified by min and max coordinates.
* ```parser```: parses the metadata and get human-readeable information from the coordinates of the images.


### Example of a flow

```mermaid
flowchart TD
    subgraph Endpoint_1
    uncompress-->atmospheric
    atmospheric-->crop
    end
    subgraph Endpoint_2
    crop-->derivatives
    derivatives-->summary
    end
    subgraph Endpoint_3
    summary-->A
    A@{ shape: lin-cyl, label: "Database" }
    A-->Geoportal
    end
    subgraph Endpoint_4
    uncompress-->parser
    parser --> A
    end
```

* Uncompress:
    - **Execution command**: ```mkdir -p out_dir && tar -xf image.tar.gz -C out_dir```
    - **Inputs**: An image in tar.gz format
    - **Outputs**: The file uncompressed.
* Atmospheric:
    - **Execution command**: ```python /app/main.py /path/to/image image_name -o out_dir```
    - **Inputs**: Bands of the image
    - **Outputs**: Corrected bands
* Crop:
    - **Execution command**: ```python /app/crop.py /path/to/image image_name longitud1 latitud1 longitud2 latitud2 -o out_dir```
    - **Inputs**: Bands of the image, coordinates
    - **Outputs**: Cropped Bands
* Derivatives:
    - **Execution command**: ```python /app/main.py/path/to/image image_name -o @D```
    - **Inputs**:  Bands of the image
    - **Outputs**:  Corrected bands
* Summary:
    - **Execution command**: ```python /app/main.py @I -o @D```
    - **Inputs**: Derivate products
    - **Outputs**: Plots
* Parser:
    - **Execution command**: ```python /app/test.py METADATA IMAGE_NAME MONGO_DATABASE > OUT.json```
    - **Inputs**:  Metadata of the image
    - **Outputs**: A json file with the metadata, which already is indexed in a DB.

### Construcción de las imagenes de  contenedores

```bash
cd stages/correcciones
docker build -t landsat:corrections .
cd stages/parser
docker build -t parser:landsat .
```
### Levantar base de datos

```bash
cd database
docker-compose up -d
```

### Ejecución Makeflow

```bash
cd makeflow
bash build.sh PATH_TO_IMAGES PATH_TO_OUTPUTS
docker exec -it landsattests bash
python build.py /inputs > workflow.jx
makeflow --jx --max-local=1 workflow.jx
```

## Ejecución Parsl

```
📦parsl
 ┣ 📂mongodbdata
 ┣ 📂parsl
 ┃ ┣ 📂apps <- Application source code and requirements
 ┃ ┃ ┣ 📂corrections
 ┃ ┃ ┣ 📂crop
 ┃ ┃ ┣ 📂derivatives
 ┃ ┃ ┣ 📂parser
 ┃ ┃ ┣ 📂summary
 ┃ ┃ ┗ 📜requirements.txt
 ┃ ┣ 📂indexing <- Results of the indexing stage
 ┃ ┣ 📜Parsl.Dockerfile
 ┃ ┣ 📜Globus.Dockerfile
 ┃ ┗ 📜parslflow.py
 ┃ ┗ 📜distributed_parsl.py
 ┗ 📜docker-compose.yml
```

1. Dirigirse a la carpeta parsl y modificar las lineas 10 y 20 del archivo ```docker-compose.yml``` .

2. Levantar los servicios con ```docker compose```.

    ```bash
    docker compose build
    docker compose up -d
    docker compose exec parsltest bash
    ```


2. Ingresar a los contenedores ```globusendpoint```, ```globusendpoint_corrections```, y ```globusendpoint_derivatives```.

3. Ejecutar los siguientes comandos en cada contenedor:

    ```bash
    globus-compute-endpoint configure endpointname
    globus-compute-endpoint start endpointname

    ```

    Reemplazar ```endpointname``` con el nombre del endpoint deseado. Seguir las instrucciones de autenticación. Guardar el token del endpoint. 

4. Ingresar al contenedor ```parsltest```.

    ```bash
    docker compose exec parsltest bash
    ```

5. Modificar el archivo distributed_parsl.py, cambiando los valores de las variables ```endpoint_id``` con los obtenidos anteriormente.

6. Modificar la línea 30 con las coordenadas deseadas.

3. Ejecutar el flujo con:

    ```bash
    python parslflow.py
    ```


## Ejecución Nez

```
📦deployer
 ┣ 📂cfg-files <- Configuration files
 ┃ ┗ 📜configuration.cfg
 ┣ 📂results <- Deployment and execution results
 ┣ 📜Dockerfile
 ┗ 📜docker-compose.yml
```

1. Dirigirse a la carpeta stages y ejecutar el archivo ```build.sh``` para construir las imágenes de contenedor.

    ```bash
    cd stages
    bash build.sh
    ```

1. Dirigirse a la carpeta deployer.
3. Modificar el archivo ```deployer/cfg-files/configuration.cfg``` y cambiar la IP del BB de indexamiento (línea 9) así como la fuente de datos del stage ```uncompressingstage``` (línea 47).

    ```configuration
    [BB]
    name = uncompressing
    command = mkdir -p @D/@N && tar -xzvf @I -C @D/@N
    image = uncompress:landsat
    [END]

    [BB]
    name = indexing
    command = python /app/test.py @I/@N_MTL.txt @N IP_HOST:27018
    image = parser:landsat
    [END]

    [BB]
    name = corrections
    command = python /app/LS.py @I @N
    image = corrections:landsat
    [END]

    [PATTERN]
    name = indexingpattern
    task = indexing
    pattern = MW
    workers = 2
    loadbalancer = TC:D
    [END]

    [PATTERN]
    name = uncompressingpattern
    task = uncompressing
    pattern = MW
    workers = 2
    loadbalancer = TC:FR
    [END]

    [PATTERN]
    name = correctionspattern
    task = corrections
    pattern = MW
    workers = 1
    loadbalancer = TC:D
    [END]


    #Workflow definition
    [STAGE]
    name = uncompressingstage
    source = FUENTE_DATOS
    sink = correctionsstage
    transformation = uncompressingpattern
    [END]



    [STAGE]
    name = correctionsstage
    source = uncompressingstage
    sink = 
    transformation = correctionspattern
    [END]

    [STAGE]
    name = indexingstage
    source = uncompressingstage
    sink = 
    transformation = indexingpattern
    [END]


    #Workflow
    [WORKFLOW]
    name = workflow1
    stages = uncompressingstage correctionsstage indexingstage
    [END]

    ```

2. Modificar el archivo ```docker-compose.yml``` y cambiar las siguientes rutas:
    * ```FUENTE_DATOS``` (línea 11): Ruta absoluta al directorio donde se encuentran las imágenes en formato tar.gz.
    * ```PATH_TO_DEPLOYER``` (línea 14): Ruta absoluta donde se encuentra el directorio ```deployer```.

    ```YAML
    version: '3'
    services:
    deployer:
        image: ddomizzi/deployer:v1
        tty: true
        restart: unless-stopped
        #working_dir: /home/domizzi/Documents/geoprocindexing/deployer/
        volumes:
        - '/var/run/docker.sock:/var/run/docker.sock' #Docker deamon
        - './deployer/results:/home/app/results' #Deployer
        - '/PATH/TO/DATA:/PATH/TO/DATA' #Data source
        - './cfg-files:/cfg-files' #Configuration files
        environment:
        HOST_PATH: /PATH/TO/DEPLOYER
    ```

3. Levantar el servicio de despliegue y acceder al contenedor.

    ```bash
    docker compose up -d
    docker compose exec deployer bash
    ```

4. Despliega los contenedores del flujo con:

    ```bash
    ./puzzlemesh/puzzlemesh -m compose -c /cfg-files/configuration.cfg
    ```

En ```/PATH/TO/DEPLOYER/results``` verás que se crearon un conjunto de directorios, el cual es el espacio de trabajo de cada contenedor. Aquí se escribirán los resultados de la ejecución.

5. Ejecuta los contenedores con: 

    ```bash
    ./puzzlemesh/puzzlemesh -m compose -c /cfg-files/configuration.cfg -exec True
    ```

6. Para detener los contenedores del flujo ejecuta:

    ```bash
    ./puzzlemesh/puzzlemesh -m compose -c /cfg-files/configuration.cfg -stop True
    ```
