#include "util.h"
#include "mystem.h"
#include "json11/json11.hpp"
#include <iostream>
#include <vector>
#include "build/messages.pb.h"
#include <fstream>

using namespace std;
vector<json11::Json> RunMystem(const string &text);
Tokens GetTokens(const vector<json11::Json> &words);
int main(int ac, char **av) {
  string input = ReadFile("texts/input.txt");
  auto result = RunMystem(input);
  {
    std::ofstream inter("texts/inter.json", std::ios_base::out | std::ios_base::trunc);
    for (const auto &line : result) {
      inter << line.dump() << endl;
    }
  }

  Tokens tokens = GetTokens(result);
  WriteFile("texts/output.asciipb", ProtoToString(tokens));
  // cout << tokens.Utf8DebugString();
}
