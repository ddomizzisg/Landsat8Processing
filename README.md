# Dagon* Landsat 8 corrections

Flujo de trabajo que corrije y obtiene productos derivados de imagenes satelitales Landsat8.

Etapas del flujo: descompresión, correcciones+productos derivados, parsing+indexing

Descargar imagenes satelitales ```Landsat8``` de https://earthexplorer.usgs.gov/

### Construcción de las imagenes de  contenedore

```bash
cd dagon/correcciones
docker build -t landsat:corrections .
cd dagon/parser
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