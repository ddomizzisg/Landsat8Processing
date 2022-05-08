#ifndef STAGE_H
#define STAGE_H

#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <sstream>
#include <nlohmann/json.hpp>
#include <unordered_map>
#include <boost/algorithm/string/replace.hpp>
#include <dirent.h>

#include "files.h"
#include "buildingblock.h"
#include "pattern.h"
#include "single.h"
#include "logs.h"
#include "ordered_map.h"
#include "ordered_set.h"

using namespace std;
using json = nlohmann::json;

class Stage : public BuildingBlock
{
private:
    vector<Stage*> previous;
    vector<Stage*> next;
    tsl::ordered_map<string, BuildingBlock *> bbs;
    vector<string> bbsStr;
public:
    Stage():BuildingBlock(STAGE){};
    Stage(string name):BuildingBlock(name, STAGE){}

    Stage(string name, vector<string> sourcesStr, vector<string> sinksStr, vector<string> bbsStr)
    :BuildingBlock(name, STAGE, sourcesStr, sinksStr)
    {
      this->bbsStr = bbsStr;
    }

    Stage(string name, vector<Stage*> previous, vector<Stage*> next,
          tsl::ordered_map<string, BuildingBlock *> bbs, vector<string> sourcesStr,
          vector<string> sinksStr, vector<string> bbsStr)
    :BuildingBlock(name, STAGE, sourcesStr, sinksStr)
    {
        this->previous = previous;
        this->next = next;
        this->bbs = bbs;
        this->bbsStr = bbsStr;
    }

    void setPrevious(vector<Stage *> previous);
    void setNext(vector<Stage *> next);
    void setBBs(tsl::ordered_map<string, BuildingBlock *> bb);
    tsl::ordered_map<string, BuildingBlock *> getBBs();
    BuildingBlock* getBB(string name);
    void setBB(BuildingBlock* bb);
    void addPrevious(Stage *previous);
    void addNext(Stage *next);
    vector<Stage *> getNext();
    vector<Stage *> getPrevious();
    vector<string> getBBsStr();
    bool execute(string,  vector<string> sourcesPaths, string compose_command);
    bool hasBB(string name);
    string getDependencieDir(BuildingBlock* bb, string basedir);
};
#endif
