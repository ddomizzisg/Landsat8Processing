#include "workflow.h"

void Workflow::setStages(vector<Stage*> stages)
{
    this->stages = stages;
}

void Workflow::addStage(Stage *stg)
{
    Logger(this->name + ": Stage " + stg->getName() + " added", true);
    this->stages.push_back(stg);
}

void Workflow::setStart(Stage start)
{
    this->start = start;
}

void Workflow::setLast(Stage last)
{
    this->last = last;
}

vector<Stage*> Workflow::getStages()
{
    return this->stages;
}

Stage* Workflow::getStage(int idx)
{
    return this->stages.at(idx);
}


Stage Workflow::getStart()
{
    return this->start;
}

Stage Workflow::getLast()
{
    return this->last;
}

vector<string> Workflow::getStagesSrt()
{
  return this->stagesStr;
}

void Workflow::execute(string workdirbase, string compose_command)
{
  Logger(this->name + ": executing ", true);
  vector<thread> threadsvec;
  vector<string> auxStrs;

  for(auto s : this->stages)
  {
    threadsvec.push_back(thread(&Stage::execute, s, workdirbase + "/" + this->workdir, auxStrs, compose_command));
  }

  for (auto &t : threadsvec)
  {
      t.join();
  }
}
