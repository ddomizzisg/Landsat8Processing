#include <curl/curl.h>
#include <string>
#include <iostream>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

string generateCurlCommand(string service, string command);
