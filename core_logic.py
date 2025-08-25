import ollama

def get_ai_response(character_prompt: str, user_message: str, conversation_history: list) -> str:
    """
    Sends a message to the AI with a specific character prompt and conversation history,
    then gets a response.
    """
    messages = [
        {
            'role': 'system',
            'content': character_prompt,
        }
    ]

    # Add the conversation history to the messages
    messages.extend(conversation_history)

    # Add the new user message
    messages.append({'role': 'user', 'content': user_message})

    try:
        response = ollama.chat(
            model='phi3:mini',
            messages=messages
        )
        ai_response_text = response['message']['content']

        # Return the AI response to be added to the history
        return ai_response_text

    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        return "Sorry, there was an error communicating with the AI. Please check if Ollama is running."

if __name__ == '__main__':
    # Example usage:
    pirate_character = "You are a cheerful pirate captain named Red. You love to say 'Ahoy!' and talk about treasure. Keep your responses brief and in character."

    # Initialize conversation history
    history = []

    print("Talking to Captain Red. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Fair winds to ye!")
            break

        # Get AI response
        ai_output = get_ai_response(pirate_character, user_input, history)

        # Print the response
        print(f"Captain Red: {ai_output}")

        # Update history
        history.append({'role': 'user', 'content': user_input})
        history.append({'role': 'assistant', 'content': ai_output})
