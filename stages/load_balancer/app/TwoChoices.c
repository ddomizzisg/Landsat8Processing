#include "TwoChoices.h"

/**
 * @brief Function that allows to obtain size of the file.
 */
long fileSize(char *fname)
{
    long ftam = -1;
    struct stat fdata;
    int error;

    ftam = -1;
    // printf("%s", fname);
    error = stat(fname, &fdata);
    if (error >= 0)
        ftam = fdata.st_size;
    else
        printf("FileName: %s ERRNO: %d - %s\n", fname, errno, strerror(errno));
    return ftam;
}

long getFilesRecursive(char *path, int niv, node_t **list)
{
    DIR *dir;           //< Pointer to open the directory.
    struct dirent *ent; //< Contain information abut the file to open
    long numfiles;      //< Files in the actual path.
    unsigned char type; //< File type.
    char *fullName, *posstr, *parent;
    long sizef; //< File size.

    dir = opendir(path);
    numfiles = 0;

    if (dir == NULL) //< Check for errors.
        error("The directory can't be opened.");

    while ((ent = readdir(dir)) != NULL)
    {
        if ((strcmp(ent->d_name, ".") != 0) && (strcmp(ent->d_name, "..") != 0))
        {
            fullName = getFullName(path, ent);
            sizef = fileSize(fullName);
            type = getFileType(fullName, ent);

            parent = path;
            if (type == DT_REG)
            {
                if (sizef > 0)
                {
                    ++numfiles;
                    push(list, fullName, path, sizef);
                }
                posstr = generaPosStr(niv);
                free(posstr);
            }
            else if (type == DT_DIR)
            {
                posstr = generaPosStr(niv);
                numfiles += getFilesRecursive(fullName, niv + 1, list);
                free(posstr);
            }
            free(fullName);
        }
    }
    closedir(dir);
    return numfiles;
}

int countfiles(char *path)
{
    DIR *dir_ptr = NULL;
    struct dirent *direntp;
    char *npath;
    if (!path)
        return 0;
    if ((dir_ptr = opendir(path)) == NULL)
        return 0;

    int count = 0;
    while ((direntp = readdir(dir_ptr)))
    {
        if (strcmp(direntp->d_name, ".") == 0 ||
            strcmp(direntp->d_name, "..") == 0)
            continue;
        switch (direntp->d_type)
        {
        case DT_REG:
            ++count;
            break;
        }
    }
    closedir(dir_ptr);
    return count;
}

long getDirectoriesWithFiles(char *path, int niv, node_t **list)
{
    DIR *dir;           //< Pointer to open the directory.
    struct dirent *ent; //< Contain information abut the file to open
    long numfiles;      //< Files in the actual path.
    unsigned char type; //< File type.
    char *fullName, *posstr, *parent;
    long sizef; //< File size.

    dir = opendir(path);
    numfiles = 0;

    if (dir == NULL) //< Check for errors.
        error("The directory can't be opened.");

    while ((ent = readdir(dir)) != NULL)
    {
        if ((strcmp(ent->d_name, ".") != 0) && (strcmp(ent->d_name, "..") != 0))
        {
            fullName = getFullName(path, ent);
            sizef = fileSize(fullName);
            type = getFileType(fullName, ent);

            parent = path;

            if (type == DT_DIR)
            {

                if (sizef > 0 && countfiles(fullName) > 0)
                {
                    ++numfiles;
                    push(list, fullName, path, sizef);
                }

                posstr = generaPosStr(niv);
                numfiles += getDirectoriesWithFiles(fullName, niv + 1, list);
                free(posstr);
            }

            free(fullName);
        }
    }
    closedir(dir);
    return numfiles;
}

long getFiles(char *path, int niv, node_t **list)
{
    DIR *dir;           //< Pointer to open the directory.
    struct dirent *ent; //< Contain information abut the file to open
    long numfiles;      //< Files in the actual path.
    unsigned char type; //< File type.
    char *fullName, *posstr, *parent;
    long sizef; //< File size.

    dir = opendir(path);
    numfiles = 0;

    if (dir == NULL) //< Check for errors.
        error("The directory can't be opened.");
    // printf("%s", path);
    while ((ent = readdir(dir)) != NULL)
    {
        if ((strcmp(ent->d_name, ".") != 0) && (strcmp(ent->d_name, "..") != 0))
        {
            fullName = getFullName(path, ent);
            sizef = fileSize(fullName);
            type = getFileType(fullName, ent);
            parent = path;
            if (type == DT_REG)
            {
                // printf("%s %ld\n", ent -> d_name, sizef);
                if (sizef > 0)
                {
                    // printf("%ld", numfiles);
                    ++numfiles;
                    push(list, fullName, path, sizef);
                }
                posstr = generaPosStr(niv);
                free(posstr);
            }
            free(fullName);
        }
    }
    closedir(dir);
    return numfiles;
}

long getDirs(char *path, int niv, node_t **list)
{
    DIR *dir;           //< Pointer to open the directory.
    struct dirent *ent; //< Contain information abut the file to open
    long numfiles;      //< Files in the actual path.
    unsigned char type; //< File type.
    char *fullName, *posstr, *parent;
    long sizef; //< File size.

    dir = opendir(path);
    numfiles = 0;

    if (dir == NULL) //< Check for errors.
        error("The directory can't be opened.");

    while ((ent = readdir(dir)) != NULL)
    {
        if ((strcmp(ent->d_name, ".") != 0) && (strcmp(ent->d_name, "..") != 0))
        {
            fullName = getFullName(path, ent);
            sizef = fileSize(fullName);
            type = getFileType(fullName, ent);

            parent = path;

            if (type == DT_DIR)
            {

                if (sizef > 0)
                {
                    ++numfiles;
                    push(list, fullName, path, sizef);
                }

                posstr = generaPosStr(niv);
                free(posstr);
            }

            free(fullName);
        }
    }
    closedir(dir);
    return numfiles;
}

/**
 * @brief Function that count the files in the file system.
 */
long readDir(char *path, int niv, node_t **list, char *mode)
{

    if (strcmp(mode, "D") == 0)
    {
        return getDirs(path, 0, list);
    }
    else if (strcmp(mode, "F") == 0)
    {
        return getFiles(path, 0, list);
    }
    else if (strcmp(mode, "FR") == 0)
    {
        return getFilesRecursive(path, 0, list);
    }
    else if (strcmp(mode, "DL") == 0)
    {
        node_t **list2;
        list2 = malloc(sizeof(node_t));
        long files = getFiles(path, 0, list2);
        int found = getDirectoriesWithFiles(path, 0, list);
        if (files > 0)
        {
            push(list, path, path, 10);
            found += 1;
        }

        return found;
    }else if (strcmp(mode, "W") == 0)
    {
        push(list, path, path, 10);
        return 1;
    }
}

/**
 * @brief Function that allows print the data in the workers.
 */
void print_list_worker(struct worker *my_data, int workers)
{
    int i, j;

    printf("{\"result\": [");
    for (i = 0; i < workers; i++)
    {
        printf("[");
        for (j = 0; j < my_data[i].sizeWorker; ++j)
        {
            printf(
                "\"%s\"",
                my_data[i].v[j].fileName);
            if (j < my_data[i].sizeWorker - 1)
            {
                printf(",");
            }
        }
        printf("]");
        if (i < workers - 1)
        {
            printf(",");
        }
    }
    printf("]}");
}

/**
 * @brief Function returns error in the case to occur.
 */
void error(const char *s)
{
    perror(s); //< perror() returns the S string and the error that found in errno.
    exit(EXIT_FAILURE);
}

/**
 * @brief Function that allows add data file in the node structure.
 */
void push(node_t **head, char *fileName, char *path, long fileSize)
{
    node_t *new_node;
    new_node = malloc(sizeof(node_t));
    new_node->fileName = malloc(strlen(fileName) + 2);
    new_node->parent = malloc(strlen(path) + 2);

    strcpy(new_node->fileName, fileName);
    strcpy(new_node->parent, path);
    new_node->fileSize = fileSize;
    new_node->next = *head;
    *head = new_node;
}

/**
 * @brief Function that allows to obtain full name of the file.
 */
char *getFullName(char *path, struct dirent *ent)
{
    char *fullName;
    int tmp;

    tmp = strlen(path);
    fullName = malloc(tmp + strlen(ent->d_name) + 2); //< Add 2, because of 0 and the address bar (/)
    if (path[tmp - 1] == '/')
        sprintf(fullName, "%s%s", path, ent->d_name);
    else
        sprintf(fullName, "%s/%s", path, ent->d_name);
    return fullName;
}

/**
 * @brief Function to obtain type of file.
 */
unsigned char getFileType(char *nombre, struct dirent *ent)
{
    unsigned char tipo;

    tipo = ent->d_type;
    if (tipo == DT_UNKNOWN)
    {
        tipo = statFileType(nombre);
    }
    return tipo;
}

/**
 * @brief Function to obtain status of the file.
 */
unsigned char statFileType(char *fname)
{
    struct stat sdata;

    if (stat(fname, &sdata) == -1)
    { //< In the case not found, return unknown file.
        return DT_UNKNOWN;
    }

    switch (sdata.st_mode & S_IFMT)
    {
    case S_IFBLK:
        return DT_BLK;
    case S_IFCHR:
        return DT_CHR;
    case S_IFDIR:
        return DT_DIR;
    case S_IFIFO:
        return DT_FIFO;
    case S_IFLNK:
        return DT_LNK;
    case S_IFREG:
        return DT_REG;
    case S_IFSOCK:
        return DT_SOCK;
    default:
        return DT_UNKNOWN;
    }
}

/**
 * @brief Function that indentation generate.
 */
char *generaPosStr(int niv)
{
    int i;
    char *tmp;

    tmp = malloc(niv * 2 + 1); /* Add two spaces to the indentation level*/
    for (i = 0; i < niv * 2; ++i)
        tmp[i] = ' ';
    tmp[niv * 2] = '\0';
    return tmp;
}

long count_elements(node_t **head)
{
    node_t *current;
    long count;

    current = malloc(sizeof(node_t));
    current = *head;
    count = 0;

    while (current != NULL)
    {
        count++;
        current = current->next;
    }
    return count;
}

/**
 * @brief Function to load balanced.
 */
struct worker *twoChoices(node_t **list, long count, int workers, char *path_root)
{
    struct worker *arrayWorkers;
    node_t *current;
    int contar[workers], i, c, position, position1, position2;

    current = malloc(sizeof(node_t));
    arrayWorkers = (struct worker *)malloc(workers * sizeof(struct worker));

    i = 0;

    for (i = 0; i < workers; ++i)
    {
        arrayWorkers[i].v = (node_t *)malloc(count * sizeof(node_t));
        contar[i] = 0;
        arrayWorkers[i].id = i;
        arrayWorkers[i].sizeWorker = 0;
        arrayWorkers[i].sizeStorage = 0;
        arrayWorkers[i].path_root = malloc((255) * sizeof(char));
        strcpy(arrayWorkers[i].path_root, path_root);
    }

    c = 0;
    position = 0;
    position1 = 0;
    position2 = 0;
    srand(time(NULL)); //< Initialization, should only be called once.

    current = *list;
    i = 0;
    while (i < count)
    {
        position1 = rand() % workers; //< Returns a pseudo-random integer between 0 and RAND_MAX.
        position2 = rand() % workers;

        if (workers == 1)
        {
            position = position1;
        }
        else
        {
            while (position1 == position2)
            {
                position2 = rand() % workers;
            }

            if (arrayWorkers[position1].sizeStorage > arrayWorkers[position2].sizeStorage)
            {
                position = position2;
            }
            else
            {
                position = position1;
            }
        }

        arrayWorkers[position].sizeStorage += current->fileSize;
        arrayWorkers[position].sizeWorker++;
        arrayWorkers[position].v[contar[position]] = *current;
        contar[position]++;
        i++;
        current = current->next;
    }
    return arrayWorkers;
}
