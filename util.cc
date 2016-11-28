#include "util.h"

#include <fstream>
#include <google/protobuf/message.h>
#include <google/protobuf/text_format.h>
#include <stdexcept>
#include <streambuf>
#include <string>

string ReadFile(const string &path) {
  std::ifstream file(path.c_str());
  if (!file.is_open()) {
    throw std::runtime_error("Input file not found!");
  }
  return string(std::istreambuf_iterator<char>(file),
                std::istreambuf_iterator<char>());
}

void WriteFile(const string &path, const string &content) {
  std::ofstream file(path.c_str(), std::ios_base::out | std::ios_base::trunc);
  if (!file.is_open()) {
    throw std::runtime_error("Output file cannot be open!");
  }
  file << content;
}

string ProtoToString(const google::protobuf::Message &message) {
  string ret;
  google::protobuf::TextFormat::Printer printer;
  printer.SetUseUtf8StringEscaping(true);
  if (!printer.PrintToString(message, &ret)) {
    throw std::runtime_error("TextFormat::PrintToString() failed.");
  }
  return ret;
}

void StringToProto(const string &text, google::protobuf::Message *message) {
  if (!google::protobuf::TextFormat::ParseFromString(text, message)) {
    throw std::runtime_error("TextFormat::ParseFromString() failed.");
  }
}
