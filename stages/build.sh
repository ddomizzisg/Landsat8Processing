docker build -t corrections:landsat correcciones
docker build -t parser:landsat parser
docker build -t uncompress:landsat uncompress

docker compose -p database -f database/docker-compose.yml up -d 
