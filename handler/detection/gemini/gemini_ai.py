import os
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image
import requests
import io
import re
import json

load_dotenv()

generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


instruction = "You are a helpful assistant designed to output JSON object. You are helping a user generate a title and description for an image. You should always keep the title 120 characters or less and description 500 characters or less. And return the title and description as a JSON object: {'title': '...', 'description': '...'}."
prompt = "Generate title and description for this image. Strictly keep title 120 characters or less and description 500 characters or less. Return only the title and description as a JSON object in string format: \"{'title': '...', 'description': '...'}\""


def generate_title_and_description(image_url):
    img = PIL.Image.open(requests.get(image_url, stream=True).raw)

    response = model.generate_content([prompt, img])

    response_text = response.text
    print("response_text: ", response_text)

    json_string = re.search(r"\{.*\}", response_text, re.DOTALL).group()

    json_string = json_string.replace("'", '"')

    response_dict = json.loads(json_string)
    print("response_dict: ", response_dict)

    return response_dict

