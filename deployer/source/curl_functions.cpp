#include "curl_functions.h"

// string generateCurlCommand(string service, json data, string command)
// {
//   string data_str, curl_command;
//
//   data_str = data.is_null() ? "[]" : data.dump();
//   curl_command = "curl -s --header \"Content-Type: application/json\" --request POST --data '{\"command\":\""+command+"\",\"data\":" + data_str + "}' http://" + service + ":5000/api/ejecuta";
//
//   return curl_command;
// }


string generateCurlCommand(string service, string command)
{
  string data_str, curl_command;
  cout << command << endl;
  // data_str = data.is_null() ? "[]" : data.dump();
  curl_command = "sh -c \""+command+"\"";

  return curl_command;
}
