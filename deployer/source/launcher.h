#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <unordered_map>
#include <string>
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <thread>
#include <algorithm>
#include <set>

#include "stringfunctions.h"

#include "workflow.h"
#include "buildingblock.h"
#include "single.h"
#include "pattern.h"
#include "stage.h"
#include "logs.h"

using namespace std;

class Launcher
{
private:
    unordered_map<string, Single *> singles;
    unordered_map<string, Pattern *> patterns;
    unordered_map<string, Stage *> stages;
    unordered_map<string, BuildingBlock *> bbs;
    Workflow *workflow;
public:
    Launcher(){};
    Launcher(Workflow *workflow, unordered_map<string, Single *> singles,
            unordered_map<string, Pattern *> patterns,
            unordered_map<string, Stage *> stages,
            unordered_map<string, BuildingBlock *> bbs)
    {
        this->singles = singles;
        this->patterns = patterns;
        this->stages = stages;
        this->workflow = workflow;
        this->bbs = bbs;
    };

    Workflow* coupleWorkflow();
    void start(string mode);
    void buildYML(string mode);
    void coupling();
    void startExecution(string s);
    void prepareBB(BuildingBlock* bb, string basedir);
    void getVolumes(BuildingBlock* b, string target, set<vector<string>> &volumes);
    void execute(string mode);
    void printJSON();
};

#endif
