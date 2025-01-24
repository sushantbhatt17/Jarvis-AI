import os
import openai
from config import apikey

# Set OpenAI API key
openai.api_key = apikey


def generate_resignation_email():
    """
    Generates a resignation email using OpenAI's GPT model.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Write an email to my boss for resignation?",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract and print the response text
        email_text = response['choices'][0]['text'].strip()
        print("Generated Email:\n")
        print(email_text)

        # Save the response to a file for record
        if not os.path.exists("GeneratedEmails"):
            os.mkdir("GeneratedEmails")
        with open("GeneratedEmails/resignation_email.txt", "w") as file:
            file.write(email_text)

        print("\nThe email has been saved to 'GeneratedEmails/resignation_email.txt'.")

    except openai.error.OpenAIError as e:
        print(f"Error occurred with OpenAI API: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    generate_resignation_email()
