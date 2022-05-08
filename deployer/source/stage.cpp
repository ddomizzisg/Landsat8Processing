#include "stage.h"


void Stage::setPrevious(vector<Stage *> previous)
{
    this->previous = previous;
}

void Stage::setNext(vector<Stage *> next)
{
    this->next = next;
}

void Stage::setBBs(tsl::ordered_map<string, BuildingBlock *> bb)
{
  this->bbs = bb;
}

tsl::ordered_map<string, BuildingBlock *> Stage::getBBs()
{
  return this->bbs;
}

bool Stage::hasBB(string name)
{
  return bbs.find(name) != bbs.end();
}

void Stage::addPrevious(Stage *previous)
{
    this->previous.push_back(previous);
}

void Stage::addNext(Stage *next)
{
    this->next.push_back(next);
}


void Stage::setBB(BuildingBlock *bb)
{
    Logger(this->name + ": Added building block " + bb->getName(), true);
    this->bbs[bb->getName()] = bb;
}

BuildingBlock* Stage::getBB(string name)
{
  return this->bbs.find(name) != this->bbs.end() ? this->bbs[name] : NULL;
}

vector<string> Stage::getBBsStr()
{
  return this->bbsStr;
}

string Stage::getDependencieDir(BuildingBlock* bb, string basedir)
{
  switch (bb->getType()) {
    case SINGLE:
    {
      return basedir + "/" + bb->getWorkdir();
    }
    case PATTERN:
    {
      Pattern* pt = (Pattern*) bb;
      return this->getDependencieDir(pt->getWorker(), basedir + "/" + bb->getWorkdir());
    }
    case STAGE:
    {
      Stage* stg = (Stage *) bb;
      BuildingBlock* last = stg->getBB(stg->getBBsStr()[stg->getBBsStr().size()-1]);
      //cout << last->getName() << endl;
      return this->getDependencieDir(last, basedir + "/" + bb->getWorkdir());
    }
  }
  return "";
}

bool Stage::execute(string workdirbase,  vector<string> sourcesPaths, string compose_command)
{
  vector<string> sourcesStg;
  Logger(this->name + ": waiting", true);
  this->state = WAITING;
  int previousCompleted = 0;

  while ( previousCompleted < this->sources.size() )
  {
    previousCompleted = 0;
    for (auto s : this->sources)
    {
      
      if(s.second->getState() == COMPLETED){
        previousCompleted++;
      }else if(s.second->getState() == FAILED){
        this->state = FAILED;
        Logger(this->name + ": ERROR stage " + s.second->getName() + " failed", true);
        return false;
      }
    }
    //Logger(this->name + ": stage " + ::to_string(previousCompleted) + "\t" + ::to_string(this->sources.size())  + " failed", true);
  }
  auto start_ptr = chrono::steady_clock::now();
  Logger(this->name + ": WORKING", true);
  this->state = WORKING;
  for (auto s : this->sources)
  {
    sourcesStg.push_back(this->getDependencieDir(s.second, workdirbase + "/"));
  }

  for (auto s : this->sourcesStr)
  {
    if (dirExists(s.c_str()) == 1)
    {
      sourcesStg.push_back(s);
    }else{
      Logger( this->name + "WARNING: " + s + "  doesn't exist\n", true);
    }
  }
  //std::cout << "\n" << sourcesStg.size() << "\n" << std::endl;
  Logger(this->name + ":  has " + ::to_string(sourcesStg.size()) + " sources", true);

  if(sourcesStg.size() == 0){
    Logger(this->name + ": ERROR stage does not have sources ", true);
    this->state = FAILED;
  }else{
    std::vector<string> inputs, outputsPaths;
    bool first = true;

    for(auto b : this->bbs)
    {
      inputs = first ? sourcesStg : outputsPaths;
      switch (b.second->getType()) {
        case SINGLE:
          ((Single* ) b.second)->execute( workdirbase + "/" + this->workdir, inputs, compose_command, !first, 0);
          outputsPaths.clear();
          break;
        case PATTERN:
          ((Pattern* ) b.second)->execute( workdirbase + "/" + this->workdir, inputs, compose_command);
          break;
        case STAGE:
          ((Stage* ) b.second)->execute( workdirbase + "/" + this->workdir, inputs, compose_command);
          break;
      }

      outputsPaths.push_back(workdirbase + "/" + this->workdir);
    }
    auto end_ptr = chrono::steady_clock::now();
    this->state = COMPLETED;
    Logger(this->name + ": stage executed in ST = " + ::to_string(chrono::duration_cast<chrono::milliseconds>(end_ptr - start_ptr).count()) + " miliseconds", true);
    
  }
  
  return true;
}
//
// void executeWorker(string commandComp, Single *worker, json contents, int n_worker)
// {
//     int i = 0;
//     //string final_cmd = worker->getCommnad().replace(0, worker->getCommnad().size()-1, "@I","xxx");
//     //std::string output = boost::replace_all_copy(worker->getCommnad(), "@I", "xxx");
//     string command, final_curl, final_path;
//
//     //string params = "[" + worker->source + "," + ss.str() + "]";
//     string curl_command = " curl -s --header \"Content-Type: application/json\" --request POST --data '{\"command\":\"COMMMAND\",\"data\":[]}' http://" + worker->getName() + "_" + ::to_string(n_worker + 1) + ":5000/api/ejecuta";
//     for (i = 0; i < contents.size(); i++)
//     {
//         stringstream aux;
//         aux << contents[i];
//         command = boost::replace_all_copy(worker->getCommnad(), "@I", final_path.c_str());
//         final_curl = boost::replace_all_copy(curl_command, "COMMMAND", command.c_str());
//         string result = exec_cmd((commandComp + " exec -T proxy" + final_curl).c_str());
//         cout << result << endl;
//         aux.clear();
//         final_path.clear();
//         final_curl.clear();
//     }
// }

void executeBB(string commandComp, Single *worker)
{
    // int i = 0;
    // //string final_cmd = worker->getCommnad().replace(0, worker->getCommnad().size()-1, "@I","xxx");
    // //std::string output = boost::replace_all_copy(worker->getCommnad(), "@I", "xxx");
    // string command, final_curl, final_path;
    //
    // //string params = "[" + worker->source + "," + ss.str() + "]";
    // string curl_command = " curl -s --header \"Content-Type: application/json\" --request POST --data '{\"command\":\"COMMMAND\",\"data\":[]}' http://" + worker->getName() + ":5000/api/ejecuta";
    //
    // DIR *dir;
    // struct dirent *ent;
    //
    // if ((dir = opendir(worker->getSource().c_str())) != NULL)
    // {
    //     /* print all the files and directories within directory */
    //     while ((ent = readdir(dir)) != NULL)
    //     {
    //         //printf("%s\n", ent->d_name);
    //     }
    //     closedir(dir);
    // }
    // else
    // {
    //     /* could not open directory */
    //     perror("");
    // }

    // for (i = 0; i < contents.size(); i++)
    // {
    //     stringstream aux;
    //     aux << contents[i];
    //     final_path = boost::replace_all_copy(aux.str(), "\"", "");
    //     //cout << final_path << endl;
    //     command = boost::replace_all_copy(worker->getCommnad(), "@I", final_path.c_str());
    //     final_curl = boost::replace_all_copy(curl_command, "COMMMAND", command.c_str());

    //     //cout << commandComp + " exec -T proxy" + final_curl << endl;

    //     string result = exec_cmd((commandComp + " exec -T proxy" + final_curl).c_str());
    //     //cout << result << endl;
    //     aux.clear();
    //     final_path.clear();
    //     final_curl.clear();
    // }
}

// void executeNext(Stage *stg, string commandComp)
// {
//
//
//     stg->execute(commandComp);
// }
//
// void Stage::execute(string commandComp)
// {
//     // stringstream ss;
//     // bool complete_previous = false;
//     // int aux = 0;
//     // Logger(this->name+": waiting....", this->workdir, true);
//     // while (aux != this->previous.size())
//     // {
//     //     for (auto &s : this->previous)
//     //     {
//     //         if (s->status == 2)
//     //         {
//     //             aux += 1;
//     //         }
//     //     }
//     //     cout << this->previous.size() << " " << aux << endl;
//     // }
//     // Logger(this->name + ": on execution", this->workdir, true);
//     //
//     // status = 1;
//     // if (this->bb->getType().compare("SINGLE") == 0)
//     // {
//     //     Single *single = (Single *)bb;
//     //     executeBB(commandComp, single);
//     // }
//     // else if (this->bb->getType().compare("PATTERN") == 0)
//     // {
//     //     Pattern *pt = (Pattern *)bb;
//     //     vector<thread> threadsvec;
//     //
//     //     int i = 0;
//     //     json j;
//     //     ss << pt->getNWorkers();
//     //     //string params = "[" + this->source + "," + ss.str() + "]";
//     //     if (this->previous.size() == 0)
//     //     {
//     //         j.push_back(std::to_string(pt->getNWorkers()));
//     //         //j.push_back(std::to_string(pt->getNWorkers()));
//     //         //.push_back(this->source[0]);
//     //     }
//     //     // string curl_command = " curl -s --header \"Content-Type: application/json\" --request POST --data '{\"command\":\"/home/app/main\",\"data\":[\"" + pt->getSource() + "\",\"" + std::to_string(pt->getNWorkers()) + "\"]}' http://lb" + pt->getName() + ":5000/api/ejecuta";
//     //     //
//     //     // string lbcommand = commandComp + " exec -T lb" + pt->getName() + curl_command;
//     //     // Logger(this->name+": querying load-balancer", this->workdir, true);
//     //     // string result = exec_cmd(lbcommand.c_str());
//     //     // auto json_result = json::parse(result);
//     //     // string output = json_result["stdout"];
//     //     // output.substr(1, output.size() - 1);
//     //     // auto elements = json::parse(output);
//     //     //
//     //     // for (i = 0; i < pt->getNWorkers(); i++)
//     //     // {
//     //     //     threadsvec.push_back(thread(executeWorker, commandComp, pt->getWorker(), elements[i], i));
//     //     // }
//     //     //
//     //     // for (auto &t : threadsvec)
//     //     // {
//     //     //     t.join();
//     //     // }
//     // }
//     //
//     // this->status = 2;
//     // Logger(this->name+": Completed", this->workdir, true);
//     //
//     // vector<thread> threadsvec;
//     // for (auto &x : this->next)
//     // {
//     //     if (x->status == 0)
//     //     {
//     //         threadsvec.push_back(thread(executeNext, x, commandComp));
//     //     }
//     // }
//     //
//     // for (auto &t : threadsvec)
//     // {
//     //     t.join();
//     // }
// }
