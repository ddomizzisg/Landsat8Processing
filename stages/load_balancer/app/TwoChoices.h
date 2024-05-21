
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>
#include <sys/time.h>
#include <fcntl.h>
#include <libgen.h>

/**
 * @brief Node structure.
 *
 * Node structure stores the data of files found in the file system.
 */
typedef struct node {
    char *parent;           /**< Directory path to the file.*/
    char *fileName;         /**< Name of the files in the directory.*/
    long fileSize;          /**< Size of the file in bytes.*/
    struct node * next;     /**< Next element in the linked list.*/
} node_t;


/**
 * @brief Worker structure.
 *
 * Worker structure stores data of the workers in the patterns.
 */
struct worker{
  int id;                          /**< Identifier of worker.*/
  int sizeWorker;                  /**< Number of the processed data in the worker.*/
  long sizeStorage;                /**< Size of the processed data in the worker.*/
  char *path_root;                 /**< Path root of the directory.*/
  node_t *v;                       /**< List of the files to procces.*/
};


/**
 * @brief Function that allows to obtain size of the file.
 * @param fname Name file.
 * @return Return the size of the file.
 */
long fileSize(char *fname);

/**
 * @brief Function that allows to obtain full name of the file.
 * @param path Path of the file in the file system.
 * @return Return the full name of the file.
 */
char *getFullName(char *path, struct dirent *ent);

/**
 * @brief Function that allows print the data in the workers.
 * @param my_data Worker structure that contains file list.
 * @param workers Number of workers in the pattern.
 */
void print_list_worker(struct worker *my_data, int workers);

/**
 * @brief Function returns error in the case to occur.
 * @param s Char string that contains the error.
 * @return Return the error.
 */
void error(const char *s);


/**
 * @brief Function that read files in the path.
 * @param path Files path.
 * @param niv Indentation level.
 * @param list Files list.
 * @return Return indentation in the print of the paths.
 */
long readDir(char *path, int niv, node_t ** list, char* mode);

/**
 * @brief Function that allows add data file in the node structure.
 * @param head Node structure.
 * @param fileName Name of the file to add in the structure.
 * @param path Path of the file.
 * @param fileSize Size of the file.
 * @param hash Hash of the file.
 */
void push(node_t ** head, char *fileName, char *path, long fileSize);


/**
 * @brief Function to obtain type of file.
 * @param path File path.
 * @param ent Contain file data.
 * @return Return type of the file.
 */
unsigned char getFileType(char *path, struct dirent *ent);

/**
 * @brief Function to obtain status of the file.
 * @param fname File name.
 * @return Return status of the file.
 */
unsigned char statFileType(char *fname);

/**
 * @brief Function that indentation generate.
 * @param niv Indentation level.
 * @return Return indentation in the print of the paths.
 */
char *generaPosStr(int niv);

long count_elements(node_t ** head);

/**
 * @brief Function to load balanced.
 * @param list List of files to procces.
 * @param count Number of files to procces.
 * @param workers Number of workers.
 * @param path_root Root path of the directory to analyse.
 * @param configuration Config structure that contains the dato of configuration service.
 * @return Returns worker struct with the list of proccesed files.
 */
struct worker *twoChoices(node_t **list, long count, int workers, char *path_root);


long getDirs(char *path, int niv, node_t ** list);
long getFiles(char *path, int niv, node_t ** list);
long getFilesRecursive(char *path, int niv, node_t ** list);
int countfiles(char *path);
long getDirectoriesWithFiles(char *path, int niv, node_t ** list);
