
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


# Used to securely store your API key
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key='AIzaSyCcc0sqTtwa42Dp6QVuBLlWJeewfh0fx-w')
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
response = model.generate_content(
    'Tell me a story about a magic backpack.',
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=20,
        temperature=1.0)
)
text = response.text
print(text)

if response.candidates[0].finish_reason.name == "MAX_TOKENS":
    text += '...'

# print(to_markdown(text))