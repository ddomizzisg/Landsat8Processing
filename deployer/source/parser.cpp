#include "parser.h"
#include <typeinfo>

unordered_map<string, Single *> ConfigParser::searchSingles(vector<string> lines)
{
    bool found;
    unordered_map<string, Single *> singles;
    string name, command, image;
    vector<string> inputs, outputs, ports;

    found = false;

    for (auto &i : lines)
    {
        if (found)
        {
            if (i.compare("[END]") == 0)
            {
                found = !found;
                singles[name] = new Single(name, command, inputs, outputs, image, ports);
                this->bbs[name] = singles[name];
                Logger("PARSER: Configured single " + name, true);
                inputs = {};
                outputs = {};
                ports = {};
            }
            else
            {
                vector<string> v{explode(i, '=')};
                if (v.size() == 2)
                {

                    v[0] = trim(v[0]);

                    if (v[0].compare("name") == 0)
                    {
                        name = trim(v[1]);
                    }
                    else if (v[0].compare("command") == 0)
                    {
                        command = trim(v[1]);
                    }
                    else if (v[0].compare("source") == 0)
                    {
                        inputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("sink") == 0)
                    {
                        outputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("image") == 0)
                    {
                        image = trim(v[1]);
                    }
                    else if (v[0].compare("port") == 0)
                    {
                        ports = explode(trim(v[1]), ' ');
                        cout << v[1] << endl;
                    }
                }
                else
                {
                    cerr << i << "Bad configuration" << endl;
                    exit(1); // call system to stop
                }

            }
        }
        else if (i.compare("[BB]") == 0) //New BB found, next lines are the BB metadata
        {
            found = !found;
        }
    }
    return singles;
}

unordered_map<string, Pattern *> ConfigParser::searchPatterns(vector<string> lines,
        unordered_map<string, Single *> singles)
{
    bool found;
    unordered_map<string, Pattern *> patterns;
    string name, pattern, lb, workerName, lbmode;
    vector<string> inputs, outputs;
    int nWorkers;

    found = false;

    for (auto &i : lines)
    {
        if (found)
        {
            if (i.compare("[END]") == 0)
            {
                found = !found;
                //cout << singles[workerName]->getName()  << endl;
                patterns[name] = new Pattern(name, nWorkers, lb, lbmode, pattern,
                                            singles[workerName], inputs, outputs);
                this->bbs[name] = patterns[name];
                Logger("PARSER: Configured pattern " + name, true);
            }
            else
            {
                vector<string> v{explode(i, '=')};
                if (v.size() == 2)
                {
                    v[0] = trim(v[0]);
                    //cout << v[0] << " " << v[0].compare("command") << endl;
                    if (v[0].compare("name") == 0)
                    {
                        name = trim(v[1]);
                    }
                    else if (v[0].compare("task") == 0)
                    {
                        workerName = trim(v[1]);
                    }
                    else if (v[0].compare("source") == 0)
                    {
                        inputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("pattern") == 0)
                    {
                        pattern = trim(v[1]);
                    }
                    else if (v[0].compare("workers") == 0)
                    {
                        nWorkers = stoi(trim(v[1]));
                    }
                    else if (v[0].compare("loadbalancer") == 0)
                    {
                       vector<string> v2{explode(trim(v[1]), ':')};
                       lb = v2[0];
                       lbmode = v2[1];
                    }
                    else if (v[0].compare("sink") == 0)
                    {
                       outputs = explode(trim(v[1]), ' ');
                    }
                }
                else
                {
                    cerr << i << "Bad configuration" << endl;
                    exit(1); // call system to stop
                }

            }
        }
        else if (i.compare("[PATTERN]") == 0) //New Pattern found, next lines are the Pattern metadata
        {
            found = !found;
        }
    }
    return patterns;
}


unordered_map<string, Stage *> ConfigParser::searchStages(vector<string> lines,
                                                          unordered_map<string, Single *> singles,
                                                          unordered_map<string, Pattern *> patterns)
{
    bool found;
    unordered_map<string, Stage *> stages;
    string name;
    vector<string> inputs, outputs,  transformationNames;
    found = false;

    for (auto &i : lines)
    {
        if (found)
        {
            if (i.compare("[END]") == 0)
            {
                found = !found;
                //cout << name << command << input << outputs << endl;
                stages[name] = new Stage(name, inputs, outputs, transformationNames);
                this->bbs[name] = stages[name];
                Logger("PARSER: Configured stage " + name, true);
            }
            else
            {
                vector<string> v{explode(i, '=')};
                if (v.size() == 2)
                {
                    v[0] = trim(v[0]);
                    //cout << v[0] << " " << v[0].compare("command") << endl;
                    if (v[0].compare("name") == 0)
                    {
                        name = trim(v[1]);
                    }
                    else if (v[0].compare("source") == 0)
                    {
                        inputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("sink") == 0)
                    {
                        outputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("transformation") == 0)
                    {
                        transformationNames = explode(trim(v[1]), ' ');
                    }
                }
                else
                {
                    cerr << i << "Bad configuration" << endl;
                    exit(1); // call system to stop
                }
            }
        }
        else if (i.compare("[STAGE]") == 0) //New Pattern found, next lines are the Pattern metadata
        {
            found = !found;
        }
    }
    return stages;
}

Workflow* ConfigParser::searchWorkflow(vector<string> lines)
{
    bool found;
    string name;
    vector<string> inputs, outputs, transformationNames;
    Workflow *workflow;

    found = false;
    //cout << "ENTRO" << endl;
    for (auto &i : lines)
    {
        if (found)
        {
            if (i.compare("[END]") == 0)
            {
                found = !found;
                workflow = new Workflow(name, inputs, outputs, transformationNames);
                Logger("PARSER: Configured workflow " + name, true);
            }
            else
            {
                vector<string> v{explode(i, '=')};
                if (v.size() == 2)
                {
                    v[0] = trim(v[0]);
                    
                    if (v[0].compare("name") == 0)
                    {
                        name = trim(v[1]);
                    }
                    else if (v[0].compare("stages") == 0)
                    {
                        transformationNames = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("source") == 0)
                    {
                        inputs = explode(trim(v[1]), ' ');
                    }
                    else if (v[0].compare("sink") == 0)
                    {
                        outputs = explode(trim(v[1]), ' ');
                    }
                }
                else
                {
                    cerr << i << "Bad configuration" << endl;
                    exit(1); // call system to stop
                }
            }
        }
        else if (i.compare("[WORKFLOW]") == 0) //New Pattern found, next lines are the Pattern metadata
        {
            found = !found;
        }
    }
    return workflow;
}

int ConfigParser::readConfig(string filepath)
{
    ifstream inFile;
    string line;
    vector<string> lines;

    inFile.open(filepath);

    if (!inFile)
    {
        cerr << "Unable to open file configuration.cfg";
        exit(1); // call system to stop
    }

    while (getline(inFile, line))
    {
        //cout << line << endl;
        lines.push_back(trim(line));
    }

    inFile.close();

    //Search for singles
    this->singles = this->searchSingles(lines);
    this->patterns = this->searchPatterns(lines, singles);
    this->stages = this->searchStages(lines, singles, patterns);
    this->workflow = this->searchWorkflow(lines);

    return 0;
}

unordered_map<string, Single *> ConfigParser::getSingles()
{
    return this->singles;
}

unordered_map<string, Pattern *> ConfigParser::getPatterns()
{
    return this->patterns;
}

unordered_map<string, Stage *> ConfigParser::getStages()
{
    return this->stages;
}

Workflow * ConfigParser::getWorkflow()
{
    return this->workflow;
}

unordered_map<string, BuildingBlock*> ConfigParser::getBBs()
{
    return this->bbs;
}
