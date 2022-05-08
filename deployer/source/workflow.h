#ifndef WORKFLOW_H
#define WORKFLOW_H

#include <string>
#include <vector>

#include "stage.h"
#include "logs.h"

class Workflow : public BuildingBlock
{
private:
    vector<Stage*> stages;
    vector<string> stagesStr;
    Stage start;
    Stage last;

public:
    Workflow():BuildingBlock(WORKFLOW){};
    Workflow(string name):BuildingBlock(name, WORKFLOW){}
    Workflow(string name, vector<string> sourcesStr, vector<string> sinksStr)
    :BuildingBlock(name, WORKFLOW, sourcesStr, sinksStr){}
    Workflow(string name, vector<string> sourcesStr, vector<string> sinksStr, vector<string> stagesStr)
    :BuildingBlock(name, WORKFLOW, sourcesStr, sinksStr)
    {
      this->stagesStr = stagesStr;
    }

    void setStages(vector<Stage*> stages);
    void addStage(Stage *stg);
    vector<string> getStagesSrt();
    void setStart(Stage stg);
    void setLast(Stage stg);
    vector<Stage*> getStages();
    Stage* getStage(int idx);
    Stage getStart();
    Stage getLast();
    void execute(string workdirbase, string compose_command);
};

#endif
