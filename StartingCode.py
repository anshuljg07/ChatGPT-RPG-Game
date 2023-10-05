import requests
import os
import openai

openai.api_key = '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'
clipdrop_api_key = 'e3f4231072fa4e6cc7e351871d3d22463672b782581b9cf76b46d2f17b50d1504037b878ea44e62c0710f049f0f8ff71'

# Initialize global variables
user_input = "begin"
game_running = True

#initialized to environment creating query
chatgpt_rpg_messages = [
            {
                "role": "system",
                "content": "I want you to act as the game master of a classic text adventure game set in a lord of the rings like world. Assume the role of the narrator and never break character. Avoid referring to yourself or the outside world. If I need to give you instructions outside the context of the game, I will use curly brackets {like this}. Otherwise, you must maintain the game's setting and narrative. Each location or room should have a detailed description of at least three sentences, and you should always provide me with options to choose from or actions to take. Ensure consistency in the game world, so characters, locations, and items remain as previously described. If I type '{hint}', provide a subtle hint to guide me. Let’s embark on this journey: display the initial setting of the game and await my first command."
            }
        ]

chatgpt_imageprompt_messages = [
        {
          "role": "system",
          "content": "As I play a text-based RPG, I will provide you with excerpts from the game. Your task is to distill these excerpts into A SINGLE, concise text-to-image prompt suitable for DALLE. This prompt should capture the essence of the environment or scene described in the game. Exclude references to my personal interactions, past verbs, or speculations about the story's progression. Imagine you're describing the scene to someone who's observing from a distance, without any personal involvement. Keep track of the context as we proceed, but remember that not every excerpt will introduce a new environment. Please format the prompt following a [PREFIX], [SCENE], [SUFFIX] format where PREFIX defines the image medium, style, perspective; SCENE defines the scene, subject, or context of the image; and SUFFIX defines the overall vibes, adjectives, aesthetic descriptors, lighting, etc. Please provide the prompt as a single plain-text comma separated string with your generated PREFIX, SCENE, and SUFFIX appended together. Provide the prompt without any embellishments like quotes or \"prompt: \"."
        }
    ]
# Define functions for API calls (implement these functions with actual API calls)
def send_user_input_to_chatgpt_instance_1(user_input):
    # Make API call to ChatGPT Instance 1 and return the response
    # Implement the API call here
    chatgpt_rpg_messages.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chatgpt_rpg_messages,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = response['choices'][0]['message']
    chatgpt_rpg_messages.append(message) #append GPT's message to the conversation history
    message_content = message['content']

    return message_content

def send_chatgpt_response_to_chatgpt_instance_2(chatgpt_response):
    # Make API call to ChatGPT Instance 2 and return the image prompt
    # Implement the API call here
    chatgpt_imageprompt_messages.append(
        {
            "role" : "user",
            "content" : chatgpt_response
        }
    )

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages= chatgpt_imageprompt_messages,
      temperature=1,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    message = response['choices'][0]['message']
    chatgpt_imageprompt_messages.append(message)  # append GPT's message to the conversation history
    message_content = message['content']

    return message_content

def generate_image(image_prompt):
    # Make API call to the image generator (e.g., DALL·E 2) and return the generated image
    # Implement the API call here
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                      files={
                          'prompt': (None, image_prompt, 'text/plain')
                      },
                      headers={'x-api-key': clipdrop_api_key}
                      )
    if (r.ok):
        image_bytes = r.content
        return image_bytes
    # r.content contains the bytes of the returned image
    else:
        r.raise_for_status()

def display_image(image):
    # Display the image in the game interface
    # Implement the display logic here


# Main loop for the game
while game_running:
    # Step 1: Send User Input to ChatGPT API (Instance 1) for story creation
    chatgpt_response = send_user_input_to_chatgpt_instance_1(user_input)
    print(chatgpt_response)

    # Step 2: Send ChatGPT Response to ChatGPT API (Instance 2) for story-to-image-prompt
    image_prompt = send_chatgpt_response_to_chatgpt_instance_2(chatgpt_response)
    print(image_prompt)

    # Step 3: Send Image Prompt to Image Generator (e.g., DALL·E 2)
    generated_image = generate_image(image_prompt)

    # Step 4: Display the generated image
    display_image(generated_image)

    # Step 5: Wait for User Input (continue game)
    user_input = input("User: ")

    # Optionally, you can add game-ending conditions and logic here
    if user_input.lower() == "exit":
        game_running = False

# Game loop ends
print("Game over. Thanks for playing!")
