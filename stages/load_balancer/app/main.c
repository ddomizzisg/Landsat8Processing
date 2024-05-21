
/**
 * @file main.c
 * @mainpage Preparation and retrieval service
 * @author Diana E. Carrizales-Espinoza
 * @date September 2019
 */



#include <stdlib.h>
#include <stdio.h>
#include "TwoChoices.h"



int main(int argc, char *argv[]) {
  node_t **                   list;
  struct worker               *arrayWorkers;
  FILE                        *f;
  int                         workers, i;
  long                        count;
  char *                      path, *mode;


  list = malloc(sizeof(node_t));
  i = 0;
  count = 0;
  workers = atoi(argv[1]);
  mode = argv[2];
  path = argv[3];

  if (argc < 3)
      error("ERROR!\nThe correct way to execute the program is:\n ./leer\n");

  for(i=3;i<argc;i++)
  {
      count += readDir(argv[i], 1,list,mode);
      //break;
  }
  
  arrayWorkers = (struct worker*) malloc(workers* sizeof (struct worker));
  arrayWorkers = twoChoices(list,count,workers,path);
  print_list_worker(arrayWorkers, workers);

  return EXIT_SUCCESS;
}
