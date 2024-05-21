docker build -t corrections:landsat correcciones
docker build -t parser:landsat parser
docker build -t uncompress:landsat uncompress
docker build -t atmospheric:landsat atmospheric
docker build -t radiometric:landsat radiometric
docker build -t derivatives:landsat derivatives
docker build -t crop:landsat crop
docker build -t summary:landsat summary
docker build -t tc:balancer load_balancer

#docker compose -p database -f database/docker-compose.yml up -d 
