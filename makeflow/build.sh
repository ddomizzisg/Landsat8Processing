 docker build -t makeflow:v1 .
 docker run -id -v /var/run/docker.sock:/var/run/docker.sock -v $1:/inputs -v $2:/outputs -v $PWD:$PWD --name landsattests --net=host makeflow:v1
