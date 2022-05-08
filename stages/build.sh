docker build -t corrections:landsat correcciones
docker build -t parser:landsat parser
docker build -t corrections:parallel parallel_corrections

docker-compose -p database -f database/docker-compose.yml up -d 
