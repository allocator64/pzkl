#include "mystem.h"

#include <unistd.h>
#include <stdexcept>
#include <stdio.h>
#include <sys/wait.h>
#include <iostream>
#include <sstream>
#include "json11/json11.hpp"
#include "util.h"
#include <vector>
#include <deque>
#include "build/messages.pb.h"

// namespace {
std::vector<json11::Json> RunMystem(const string &text) {
  int stdin_pipe[2], stdout_pipe[2];
  if (pipe(stdin_pipe) != 0 || pipe(stdout_pipe) != 0) {
    perror("pipe()");
    throw std::runtime_error("Unix error");
  }
  pid_t pid = fork();
  if (pid < 0) {
    perror("fork()");
    throw std::runtime_error("Unix error");
  } else if (pid == 0) {
    close(stdin_pipe[1]);
    close(stdout_pipe[0]);
    close(0);
    close(1);
    dup2(stdin_pipe[0], 0);
    dup2(stdout_pipe[1], 1);
    execl("mystem/mystem", "mystem", "-cgin", "--format", "json", NULL);
    perror("execl()");
    _exit(1);
  } else {
    close(stdin_pipe[0]);
    close(stdout_pipe[1]);
    FILE *stdin_file = fdopen(stdin_pipe[1], "w");
    FILE *stdout_file = fdopen(stdout_pipe[0], "r");
    if (fwrite(text.data(), 1, text.size(), stdin_file) != text.size()) {
      perror("fwrite()");
      throw std::runtime_error("Unix error");
    }
    fclose(stdin_file);
    string output;
    char buf[4096];
    std::vector<json11::Json> ret;
    string err;
    while (fgets(buf, sizeof(buf), stdout_file)) {
      ret.emplace_back(json11::Json::parse(buf, err));
      if (!err.empty()) {
        std::cerr << err << std::endl;
        throw std::runtime_error("Bad json!");
      }
    }
    fclose(stdout_file);
    wait(NULL);
    return ret;
  }
}

template<typename T>
void MayBeSetGender(const string &attr, T *dest) {
  if (attr == "муж") {
    dest->set_gender(Gender::MALE);
  } else if (attr == "жен") {
    dest->set_gender(Gender::FEMALE);
  }
}

Tokens GetTokens(const std::vector<json11::Json> &words) {
  Tokens tokens;
  for (const auto &line : words) {
    Token token;
    if (!line.is_object()) {
      throw std::logic_error("not map");
    }
    if (!line["text"].is_string()) {
      throw std::logic_error("text is not string");
    }
    const auto &analysis = line["analysis"];
    if (analysis.is_null()) {
      continue;
    }
    for (const auto &kv : analysis.array_items()) {
      if (!kv["gr"].is_string()) {
        continue;
      }
      if (!kv["lex"].is_string()) {
        continue;
      }
      const auto &encoded = kv["gr"].string_value();
      const string &first = encoded.substr(0, encoded.find("="));
      std::istringstream ss(first);
      string attr;      
      std::deque<string> attributes;
      while (std::getline(ss, attr, ',')) {
        attributes.push_back(attr);
      }
      assert(!attributes.empty());
      string part_of_speech = attributes[0];
      attributes.pop_front();
      if (part_of_speech == "SPRO") {
        token.set_part_of_speech(Token::PRONOUN);
        PronounAnalysis *analysis = token.mutable_pronoun_analysis();

        for (const string &attr : attributes) {
          if (attr == "ед") {
            analysis->set_is_plural(false);
          } else if (attr == "мн") {
            analysis->set_is_plural(true);
          } else if (attr == "1-л") {
            analysis->set_person(PronounAnalysis::FIRST);
          } else if (attr == "2-л") {
            analysis->set_person(PronounAnalysis::SECOND);
          } else if (attr == "3-л") {
            analysis->set_person(PronounAnalysis::THIRD);
          } else {
            MayBeSetGender(attr, analysis);
          }
        }
      } else if (part_of_speech == "S") {
        token.set_part_of_speech(Token::NOUN);
        NounAnalysis *analysis = token.mutable_noun_analysis();

        for (const string &attr : attributes) {
          if (attr == "имя" || attr == "фам" || attr == "отч") {
            analysis->set_type(NounAnalysis::NAME);
          } else if (attr == "гео") {
            analysis->set_type(NounAnalysis::GEO);
          } else if (attr == "неод") {
            analysis->set_is_animal(false);
          } else if (attr == "од") {
            analysis->set_is_animal(true);            
          } else {
            MayBeSetGender(attr, analysis);
          }
        }
      } else if (part_of_speech == "V") {
        token.set_part_of_speech(Token::VERB);

      } else if (part_of_speech == "PART") {
        token.set_part_of_speech(Token::PART);                
      }
      if (token.has_part_of_speech()) {
        token.set_lexem(kv["lex"].string_value());
      }
      break;
    }
    if (token.has_part_of_speech()) {
      token.set_original(line["text"].string_value());
      *tokens.add_token() = token;
    }
  }
  return tokens;
}

//}  // namespace
