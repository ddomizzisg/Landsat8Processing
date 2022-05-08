CC=g++
CFLAGS=-std=c++17 -I  -lboost_filesystem -lboost_system -lcurl -pthread -Os -Wall -pedantic

all: main main_execution

main: main.cpp files.o curl_functions.o buildingblock.o single.o pattern.o stage.o  workflow.o parser.o logs.o stringfunctions.o launcher.o pipeline.o
	$(CC) $(CFLAGS)  -o main main.cpp  buildingblock.o single.o  pattern.o stage.o workflow.o parser.o logs.o stringfunctions.o launcher.o  files.o curl_functions.o pipeline.o

main_execution: main_execution.cpp files.o curl_functions.o buildingblock.o single.o pattern.o stage.o  workflow.o parser.o logs.o stringfunctions.o launcher.o pipeline.o
	$(CC) $(CFLAGS)  -o main_execution main_execution.cpp  buildingblock.o single.o  pattern.o stage.o workflow.o parser.o logs.o stringfunctions.o launcher.o  files.o curl_functions.o pipeline.o


clean:
	rm -f *.o
	rm -f main main_execution
