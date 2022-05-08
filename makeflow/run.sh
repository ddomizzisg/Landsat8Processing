python build.py /inputs > landsat8.jx

echo "Ejecutando"

rm  -r -f /outputs/*
rm *.makeflowlog
ts=$(date +%s%N)
makeflow --jx --max-local=1 landsat8.jx > logs/DS_1.txt
echo  DS,1,$((($(date +%s%N) - $ts)/1000000))
#rm /home/Volume/*/*

rm  -r -f /outputs/*
rm *.makeflowlog
ts=$(date +%s%N)
makeflow --jx --max-local=2 landsat8.jx > logs/DS_3.txt
echo  DS,3,$((($(date +%s%N) - $ts)/1000000))
#rm /home/Volume/*/*

rm  -r -f /outputs/*
rm *.makeflowlog
ts=$(date +%s%N)
makeflow --jx --max-local=4 landsat8.jx > logs/DS_6.txt
echo  DS,6,$((($(date +%s%N) - $ts)/1000000))
#rm /home/Volume/*/*

rm  -r -f /outputs/*
rm *.makeflowlog
ts=$(date +%s%N)
makeflow --jx --max-local=8 landsat8.jx > logs/DS_12.txt
echo  DS,12,$((($(date +%s%N) - $ts)/1000000))
#rm /home/Volume/*/*
