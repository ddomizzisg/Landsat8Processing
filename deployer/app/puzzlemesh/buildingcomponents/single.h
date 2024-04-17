#ifndef single_H
#define single_H

#include <iostream>
#include <string>
#include <list>
#include <nlohmann/json.hpp>
#include <chrono>
#include <unistd.h>
#include <boost/algorithm/string/replace.hpp>

#include "../io/filesystem/files.h"
#include "../io/filesystem/files.h"
#include "buildingblock.h"

using namespace std;
using json = nlohmann::json;

struct results {
  float st;
  double th;
  long size;
};

class Single : public BuildingBlock
{
private:
    string command;
    list<string> inputs;
    string image;
    vector<string> ports;
    string node;

public:
    Single():BuildingBlock(SINGLE){};
    Single(string name, string command, string image)
    :BuildingBlock(name, SINGLE)
    {
        this->command = command;
        this->image = image;
    };

    Single(string name, string command, vector<string> sourcesStr,
          vector<string> sinksStr, string image, vector<string> ports)
    :BuildingBlock(name, SINGLE, sourcesStr, sinksStr)
    {
        this->command = command;
        this->image = image;
        this->ports = ports;
    };

    Single(string name, string command, tsl::ordered_map<string, BuildingBlock *> sources,
          tsl::ordered_map<string, BuildingBlock *> sinks, string image, vector<string> ports)
    :BuildingBlock(name, SINGLE, sources, sinks)
    {
        this->command = command;
        this->image = image;
        this->ports = ports;
    };

    // Single(string name, string command, tsl::ordered_map<string, BuildingBlock *> sources,
    //       tsl::ordered_map<string, BuildingBlock *> sinks, string image, vector<string> ports)
    // :BuildingBlock(name, SINGLE, sources, sinks)
    // {
    //     this->command = command;
    //     this->image = image;
    //     this->ports = ports;
    // };

    void setCommand(string command);
    void setInputs(list<string> inputs);
    void setImage(string image);
    string getCommnad();
    list<string> getInputs();
    string getImage();
    results execute(string workdirbase, vector<string> contents, string compose_command, bool readFromDir, int id_worker);
    json processFile(string workdirbase, string content, string compose_command, int id_worker);
    vector<string> getPorts();
    void setPorts(vector<string> ports);
    void setNode(string node);
    string getNode();
    //void execute(string workdirbase, json contents, string compose_command);
};
#endif
