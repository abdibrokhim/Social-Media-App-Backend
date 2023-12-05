import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_title_and_description(image_url):

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant designed to output JSON object. You are helping a user generate a title and description for an image. You should always keep the title 120 characters or less and description 500 characters or less. And return the title and description as a JSON object: {'title': '...', 'description': '...'}."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Generate title and description for this image. Strictly keep title 120 characters or less and description 500 characters or less. Return only the title and description as a JSON object: {'title': '...', 'description': '...'}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0])

    return response.choices[0]
