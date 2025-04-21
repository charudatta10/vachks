import ollama  # Ensure you have installed the Ollama SDK

def generate_response(model_name, prompt):
    """Helper function to generate a response using the Ollama API."""
    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt
        )

        # Check if the response is a dictionary and extract the 'response' key
        if isinstance(response, dict):
            if "response" in response:
                return response["response"].strip()
            else:
                # Log the unexpected response format for debugging
                print("DEBUG: Missing 'response' key in response:", response)
                raise ValueError("Missing 'response' key in Ollama API response")
        elif hasattr(response, "response"):  # Handle custom object with 'response' attribute
            return getattr(response, "response").strip()
        else:
            # Log the unexpected response format for debugging
            print("DEBUG: Response is not a dictionary or does not have 'response' attribute:", response)
            raise ValueError("Unexpected response format from Ollama API")
    except Exception as e:
        # Log the exception for debugging purposes
        print("DEBUG: Exception occurred while generating response:", e)
        raise ValueError(f"Failed to generate response: {e}")

def generate_haiku_and_commentary(input_text):
    try:
        # Initialize Ollama Deep Seek model
        model_name = "llama3.2:3b"  # Corrected model name
        
        # Prompt for generating haiku in a sutra-like style
        haiku_prompt = f"""Write a haiku summarizing the following input in a sutra-like philosophical style.
The haiku should follow the traditional 5-7-5 syllable structure.
Keep it concise and profound.

Input:
{input_text}"""
        
        haiku = generate_response(model_name, haiku_prompt)

        # Prompt for commentary on the haiku
        commentary_prompt = f"""Provide a short philosophical commentary (2-3 sentences) 
on the following haiku. Explain its deeper meaning and connection to the original input.

Haiku:
{haiku}

Original input:
{input_text}"""
        
        commentary = generate_response(model_name, commentary_prompt)

        return haiku, commentary

    except Exception as e:
        return None, f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    # User input for summarization
    user_input = "Meditation leads to inner peace and harmony, guiding one to enlightenment."

    # Generate haiku and commentary
    haiku, commentary = generate_haiku_and_commentary(user_input)

    # Display the results
    if haiku is None:
        print("Error:")
        print(commentary)  # commentary contains the error message
    else:
        print("Generated Haiku:")
        print(haiku)
        print("\nCommentary:")
        print(commentary)