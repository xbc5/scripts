#!/bin/env python3
import sys
import subprocess  # Import subprocess for shell commands
import argparse  # Import argparse for argument parsing


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
        self.prompt = []

    def clip(self, text):
        """Send a string to the clipboard."""
        process = subprocess.Popen(
            ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
        )  # For Linux
        process.communicate(input=text.encode("utf-8"))  # Send text to clipboard

        return self  # Return self for method chaining

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
            " ".join(
                [
                    "Your answer must be informational, and it should be one or two paragraphs explaining the the core concepts of the subject matter.",
                    "The formal answer is the first answer and last answer that you make. The intermediate answers are to address inquiries",
                    "from me, to which you will respond with one or two sentences to simply gather information from me.",
                    "I will ask you to make it formal or final, when I do that, then you must make your final answer",
                    "include all of the context that we've discussed on that subject matter",
                ]
            )
        )
        return self

    def explain_library(self):
        self.prompt.append(
            " ".join(
                [
                    "You will describe a programming library to a programmer. Just cut the waffle, and stick to the technical details:",
                    "purpose (4-5 words); features (1 sentence, comma separated single words);",
                    "Write a sentence about why developers use this option over others; list the primary use cases in one or two sentences",
                    "If it's a framework, and there are other common components or libraries frequently used with it, then you must list them.",
                    "If it's a framework, then you must mention the languages that it supports, and what testing frameworks are available for it.",
                    "if it's not already obvious: what fundamental technologies does it rely upon? E.g. HTML canvas, WebGL, WebAssembly, etc.",
                    "Do NOT mention obvious things like 'a web browser' or 'HTML5', 'JavaScript', 'CSS', etc. unless it's part of the initial description.",
                    "Mention it's maturity: version number, and first release date.",
                    "Mention what license it uses, and if it's a framework, what license that my written code can use -- can it be used commercially, and",
                    "can I use a proprietary license for my code?",
                ]
            )
        )
        return self

    def provide_citations(self):
        self.prompt.append(
            "Provide sources for every claim that you make: citations, and sometimes quotes"
        )
        return self

    def add_opinions(self):
        self.prompt.append(
            "Include additional opinions from social media: both positive and negative. Keep this short.",
        )
        return self

    def provide_code_answers(self):
        self.prompt.append(
            " ".join(
                [
                    "I will ask you about code questions, you must answer in English.",
                    "if I ask you to 'show me...' how to write code, follow these rules:",
                    "a. don't explain the code; just provide the code;",
                    "b. only show me the pertinent information -- skip the boilerplate, setup code, and unrelated",
                    "concepts (I only want to see the code that relates to my question);",
                    "c. assume that I have good grasp of the language;",
                    "d. exclude all comments;",
                ]
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
