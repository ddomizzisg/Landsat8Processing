#usage: bash up_container.sh imgs_path output

docker run -id -v $1:/inputs -v $2:/outputs --name correcciones corrections:landsat
docker run -id -v $1:/inputs -v $2:/outputs --name parser parser:landsat
