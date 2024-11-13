#!/bin/env python3
import subprocess
import argparse
from textwrap import dedent
from typing import Literal


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
        intro = """
           # INTRODUCTION

           The following description are the rules for our conversation. There are some
           aspects that you must know first, and some global rules that you must always
           follow.

           1. Your answers must be in British English;
           2. there are specially demarcated sections between three dashes, for example:
              ---
              This is a demarcated section
              ---
              These sections are literal statements that you must echo back to me once you
              acknowledge these rules. I need you to echo them back as they are written.
              They are also cumulative, and you will encounter multiple. Your goal is to
              combine them, and echo them literally. Words wrapped in asterisks in these
              sections are bold, and you must echo those words emboldened -- e.g. *this is bold*.
              When you echo this back, give it a header called "HELP TEXT".

        """
        self.prompt = [dedent(intro)]

    def clip(self, text):
        """Send a string to the clipboard."""
        process = subprocess.Popen(
            ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
        )
        process.communicate(input=text.encode("utf-8"))
        return self

    def verbosity(self, verbosity: Literal["concise", "short"]):
        """1-2 paragraphs"""
        title = "# VERBOSITY"
        options = {
            "concise": """
                    Be concise:
                    - be as short as possible, in most cases one or two paragraphs;
                    - leave out superfluous adjectives and adverbs -- e.g. powerful, immersive, amazing;
                    - each statement/sentence gets right to the point -- think of a sentence, then think about
                      how you can half the number of words in it. The sentence with the fewest words is the most suitable;
                    - don't describe what the sentence is about, just write the sentence;
                    - Brevity is the goal.

                """,
            "short": """
                    Be short.
                    if I ask you a question, your answer should be one or two sentences,
                    with around 50 words max. This should express the thesis of your answer.

                """,
        }

        self.prompt.append(dedent(f"{title}\n\n{options[verbosity]}"))

        return self

    def elaborate(self):
        """Allow for elaboration; enable it through command."""
        self.prompt.append(
            dedent(
                """
                    # ALLOW FOR ELABORATION

                    - if I ask you to elaborate, then go into further detail, but keep it to one or two concise paragraphs;
                    - if I say ELI5, then elaborate with the obvious stuff, use an analogies, and most importantly explain
                      the why or how (whichever applies): I need to understand the context.

                    ---
                    + use *elaborate* to expand upon an answer, in a way that isn't too verbose;
                    + use *ELI5* when you're struggling, to get detailed and patronising answers
                      with analogies, and simple explanations;
                    ---

                """
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

    def use_format(self, format: Literal["notes"]):
        title = "# FORMATTING YOUR ANSWER"
        options = {
            "notes": """
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

                    ---
                    + you have requested a format that's suitable for your notes. The robot will answer
                      initially with a formal answer. Subsequence answers are short and concise.
                    + use the term *formal* or *final* (e.g. make that final) to request a complete answer
                      that you can copy to your notes -- this answer includes the entire context of the
                      conversation;
                    ---

                """
        }
        self.prompt.append(dedent(f"{title}\n\n{options[format]}"))
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

                    ---
                    + you have requested a library descriptor mode, it's intentionally terse and technical;
                    ---

                """
            )
        )
        return self

    def cite(self):
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

                    ---
                    + you have requested *code answers*; the robot will not provide code examples
                      unless you state *show me*.
                    + the code examples will only show pertinent code, and it assumes that you are
                      an expert;
                    ---

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
    builder.verbosity("short").elaborate().cite().build()
elif args.command == "library":
    builder.verbosity("concise").use_format(
        "notes"
    ).explain_library().elaborate().add_opinions().build()
elif args.command == "code":
    builder.verbosity("short").provide_code_answers().build()
else:
    print("Invalid command")
