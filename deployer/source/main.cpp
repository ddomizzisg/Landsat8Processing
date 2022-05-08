#include "parser.h"
#include "launcher.h"

class InputParser{
    public:
        InputParser (int &argc, char const **argv){
            for (int i=1; i < argc; ++i)
                this->tokens.push_back(std::string(argv[i]));
        }
        /// @author iain
        const std::string& getCmdOption(const std::string &option) const{
            std::vector<std::string>::const_iterator itr;
            itr =  std::find(this->tokens.begin(), this->tokens.end(), option);
            if (itr != this->tokens.end() && ++itr != this->tokens.end()){
                return *itr;
            }
            static const std::string empty_string("");
            return empty_string;
        }
        /// @author iain
        bool cmdOptionExists(const std::string &option) const{
            return std::find(this->tokens.begin(), this->tokens.end(), option)
                   != this->tokens.end();
        }
    private:
        std::vector <std::string> tokens;
};

void usage(){
  cout << "Execution: ./main -c /path/to/conf/file -m {swarm || single}" << endl;
}

int parseCDM(int argc, char const *argv[])
{
    InputParser input(argc, argv);

    if(input.cmdOptionExists("-h")){
        usage();
        return 0;
    }

    const std::string &filename = input.getCmdOption("-c");
    const std::string &mode = input.getCmdOption("-m");

    if (!filename.empty() && !mode.empty()){
        // Do interesting things ...
        ConfigParser *parser;
        Launcher *launcher;

        parser = new ConfigParser;
        parser->readConfig(filename);

        launcher = new Launcher(parser->getWorkflow(),parser->getSingles(),
                                parser->getPatterns(),parser->getStages(),
                                parser->getBBs());

        launcher->start(mode);
        return 0;
    }else
    {
        usage();
    }

    return 1;
}

int main(int argc, char const *argv[])
{
    //launcher->buildYML();
    return parseCDM(argc, argv);
}
