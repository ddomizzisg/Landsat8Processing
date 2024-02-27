docker build -t corrections:landsat correcciones
docker build -t parser:landsat parser
docker build -t uncompress:landsat uncompress
docker build -t atmospheric:landsat atmospheric
docker build -t radiometric:landsat radiometric
docker build -t derivatives:landsat derivatives

#docker compose -p database -f database/docker-compose.yml up -d 
