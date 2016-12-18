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

Text GetText(const Tokens &tokens) {
  Sentence current_sentence;
  Text text;
  bool previous_token_was_a_name = false;
  for (const auto &token : tokens.token()) {
    bool current_token_is_a_name = false;
    if (token.part_of_speech() == Token::SENTENCE_BOUND) {
      if (current_sentence.span_size() > 0) {
        current_sentence.Swap(text.add_sentence());
      }
    } else if (token.part_of_speech() == Token::VERB) {
      auto *span = current_sentence.add_span();
      span->set_type(Span::VERB);
      *span->add_token() = token;
    } else if (token.part_of_speech() == Token::NOUN) {
      current_token_is_a_name = token.noun_analysis().type() == NounAnalysis::NAME;
      if (current_token_is_a_name) {
        if (previous_token_was_a_name) {
          *current_sentence.mutable_span(current_sentence.span_size() - 1)->add_token() = token;
        } else {
          auto *span = current_sentence.add_span();
          span->set_type(Span::NAME);
          *span->add_token() = token;
        }
      }
    }
    previous_token_was_a_name = current_token_is_a_name;
  }
  return text;
}

string SpanText(const Span &span) {
  string text;
  for (const auto &token : span.token()) {
    if (!text.empty()) {
      text.push_back(' ');
    }
    text.append(token.original());
  }
  return text;
}

void SampleOutputMeetingFacts(const Text &text) {
  for (const auto &sentence : text.sentence()) {
    std::vector<string> names;
    bool good = false;
    for (const auto &span : sentence.span()) {
      if (span.type() == Span::NAME) {
        names.push_back(SpanText(span));
      } else if (span.type() == Span::VERB) {
        if (span.token(0).lexem() == "встречать") {
          good = true;
        }
      }
    }
    if (good) {
      std::cout << "Meeting fact:" << std::endl;
      for (const auto &name : names) {
        std::cout << name << std::endl;
      }
      std::cout << std::endl << std::endl;
    }
  }
} 

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
  Text text = GetText(tokens);
  WriteFile("texts/tokens.asciipb", ProtoToString(tokens));
  WriteFile("texts/text.asciipb", ProtoToString(text));
  SampleOutputMeetingFacts(text);
  // cout << tokens.Utf8DebugString();
}
