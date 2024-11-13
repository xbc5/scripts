#!/bin/env python3
import subprocess
import argparse
from textwrap import dedent


def help_text():
    help_info = """Usage: python chat-ctx.py {chat|code|library}

Description:
  This script provides context for chatbot conversations.

Options:
  chat    A general one-to-one chat without all the superfluous nonsense.
          Use 'elaborate' to ask for more detail, and ELI5 when you're struggling.
  code    Answer code questions in a Q&A format. Use 'show me' to ask for code.
  library Describe a programming library and its features."""
    print(help_info)


class PromptBuilder:
    def __init__(self):
        self.prompt = ["Your answers must be in British English."]

    def clip(self, text):
        """Send a string to the clipboard."""
        process = subprocess.Popen(
            ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
        )
        process.communicate(input=text.encode("utf-8"))
        return self

    def be_concise(self):
        """1-2 paragraphs"""
        self.prompt.append(
            " ".join(
                [
                    "Be as short as possible, in most cases one or two paragraphs.",
                    "Leave out superfluous adjectives and adverbs -- e.g. powerful, immersive, amazing.",
                    "Each statement/sentence gets right to the point -- think of a sentence, then think about",
                    "how you can half the number of words in it. The sentence with the fewest words is the most suitable.",
                    "don't describe what the sentence is about, just write the sentence",
                    "Brevity is the goal.",
                ]
            )
        )
        return self

    def allow_elaboration(self):
        """Allow for elaboration; enable it through command."""
        self.prompt.append(
            " ".join(
                [
                    "If I ask you to elaborate, then go into further detail, but keep it to one or two concise paragraphs.",
                    "If I say ELI5, then elaborate with the obvious stuff, use an analogies, and most importantly explain",
                    "the why or how (whichever applies): I need to understand the context.",
                ]
            )
        )
        return self

    def be_short(self):
        """Super short 1-2 sentences"""
        self.prompt.append(
            " ".join(
                [
                    "if I ask you a question, your answer should be one or two sentences,",
                    "with around 50 words max. This should express the thesis of your answer.",
                ]
            )
        )
        return self

    def for_notes(self):
        self.prompt.append(
            dedent(
                """
                    # FORMATTING YOUR ANSWER
                    
                    Your answer must be informational, and it should be one or two paragraphs explaining the
                    the core concepts of the subject matter.

                    There are two types of answers:
                      - formal: this is the answer in its final form, and it includes the entire context of my query;
                      - intermediate: this is an answer to an inquiry, and it's one or two concise sentences that
                        allow provides me with useful information to further interrogate you;

                    How to respond to me:
                    - when I ask you an initial question, you will initially respond with a format answer;
                    - when I ask follow up questions, you will provide intermediate answer;
                    - when I ask you to make it formal, or final, then you will include the entire (relative)
                      context of our conversation as a formal answer;

                """
            )
        )
        return self

    def explain_library(self):
        self.prompt.append(
            dedent(
                """
                    # EXPLAINING A LIBRARY

                    You will describe a programming library to a programmer. Just cut the waffle, and stick to the technical details:
                    Describe the:
                      a. purpose (4-5 words);
                      b. features (1 sentence, comma separated single words);
                      c. why developers use this option over others (1 sentence);
                      d. the primary use cases (1-2 sentences)
                      d. (if it's not already obvious) fundamental technologies does it rely upon (in 1-2 sentences)?:
                         - E.g. HTML canvas, WebGL, WebAssembly, etc.
                         - Do NOT mention obvious things like 'a web browser' or 'HTML5', 'JavaScript',
                           'CSS', etc. unless it's part of the initial description.
                      f. it's maturity: version number, and first release date (1 sentence; 4-5 words);
                      g. licenses (1-2 sentences):
                         - what license does it use?
                         - (if applicable) what license can my written code use? Can it be used commercially, and
                           can I use a proprietary license for my code?
                    
                    If it's a framework:
                      a. and there are other common components or libraries frequently used with it, then you must list them (1-2 sentences);
                      b. list the languages that it supports (1 sentence);
                      c. describe what testing frameworks are commonly used for it (1 sentence);

                """
            )
        )
        return self

    def provide_citations(self):
        self.prompt.append(
            dedent(
                """
                    # PROVIDING CITATIONS

                    Provide sources for every claim that you make: citations, and sometimes quotes.

                """
            )
        )
        return self

    def add_opinions(self):
        self.prompt.append(
            dedent(
                """
                    # PROVIDING OPINIONS

                    Include additional opinions from social media: both positive and negative.
                    Keep this short, and broad. Include specific caveats if necessary; include
                    common problems, criticism, and issues if necessary. You MUST provide a valid
                    citation for every opinion that you include.

                """
            )
        )
        return self

    def provide_code_answers(self):
        self.prompt.append(
            dedent(
                """
                    # PROVIDING ANSWERS TO CODE QUESTIONS

                    I will ask you code questions. Generally you will answer in English, but
                    If I ask you to 'show me...', then write the code and follow these rules:
                      a. don't explain the code; just provide it;
                      b. only show me the pertinent code -- skip the boilerplate, setup code,
                         installation, and other superfluous information. Typically this means
                         one or two lines of code; sometimes it means just a statement. You do
                         not necessarily need to wrap the code in a function, class, or any other
                         construct -- the pertinent statements are enough.
                      c. assume that I have good grasp of the language; assume that I have expert
                         knowledge;
                      d. exclude all comments, unless they are caveats or necessary warnings.

                """
            )
        )
        return self

    def build(self):
        self.prompt = "\n".join(self.prompt)
        self.clip(self.prompt)
        print("Copied to clipboard.")
        return self


# the args parse argument parser to parse args
parser = argparse.ArgumentParser(description="Chatbot context script.")
parser.add_argument(
    "command", choices=["chat", "code", "library"], help="Command to execute"
)
args = parser.parse_args()

print(args.command)

builder = PromptBuilder()

if args.command == "chat":
    builder.be_short().allow_elaboration().provide_citations().build()
elif args.command == "library":
    builder.be_concise().for_notes().explain_library().allow_elaboration().add_opinions().build()
elif args.command == "code":
    builder.be_short().provide_code_answers().build()
else:
    print("Invalid command")
