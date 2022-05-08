#ifndef PARSER_H
#define PARSER_H

#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <list>
#include <fstream>
#include <unordered_map>

#include "workflow.h"
#include "buildingblock.h"
#include "stringfunctions.h"
#include "single.h"
#include "pattern.h"
#include "stage.h"
#include "logs.h"

using namespace std;

class ConfigParser
{
private:
    unordered_map<string, BuildingBlock *> bbs;
    unordered_map<string, Single *> singles;
    unordered_map<string, Pattern *> patterns;
    unordered_map<string, Stage *> stages;
    Workflow* workflow;
public:
    int readConfig(string filePath);
    unordered_map<string, Single *> searchSingles(vector<string> lines);
    unordered_map<string, Pattern *> searchPatterns(vector<string> lines, unordered_map<string, Single *> singles);
    unordered_map<string, Stage *> searchStages(vector<string> lines, unordered_map<string, Single *> singles, unordered_map<string, Pattern *> patterns);
    unordered_map<string, Single *> getSingles();
    unordered_map<string, Pattern *> getPatterns();
    unordered_map<string, BuildingBlock *> getBBs();
    unordered_map<string, Stage *> getStages();
    Workflow* searchWorkflow(vector<string> lines);
    Workflow * getWorkflow();
};

#endif
