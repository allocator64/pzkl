#ifndef UTIL_H_
#define UTIL_H_

#include <string>
#include <google/protobuf/message.h>

using std::string;

string ReadFile(const string &path);
void WriteFile(const string &path, const string &content);
string ProtoToString(const google::protobuf::Message &message);
void StringToProto(const string &text, google::protobuf::Message *message);

#endif  // UTIL_H_
