docker build -t ddomizzi/corrections:landsat correcciones
docker build -t ddomizzi/parser:landsat parser
docker build -t ddomizzi/uncompress:landsat uncompress
docker build -t ddomizzi/atmospheric:landsat atmospheric
docker build -t ddomizzi/radiometric:landsat radiometric
docker build -t ddomizzi/derivatives:landsat derivatives
docker build -t ddomizzi/crop:landsat crop
docker build -t ddomizzi/summary:landsat summary
docker build -t ddomizzi/tc:balancer load_balancer

#docker compose -p database -f database/docker-compose.yml up -d 
