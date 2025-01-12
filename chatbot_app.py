import gradio as gr

# Initialize global variables
conversation_stage = 0
user_responses = []
current_question_index = 0

# Define the questions
questions = [
    "What is your name?",
    "What is your age?",
    "What is your profession?",
    "What skills do you have?",
    "What are your career goals?"
]

# Chatbot logic
def chatbot_interface(user_input):
    global conversation_stage, user_responses, current_question_index

    # Handle first interaction
    if user_input is None or user_input.strip() == "":
        return "Hello! I'm your hiring assistant. Let's get started!"

    # Process user input
    if current_question_index < len(questions):
        # Save the user's response
        user_responses.append(user_input)

        # Move to the next question
        current_question_index += 1

        # If there are more questions, ask the next one
        if current_question_index < len(questions):
            return questions[current_question_index]
        else:
            # All questions are answered
            return f"Thank you for your responses! Here's what you shared:\n\n" + "\n".join(
                [f"{questions[i]} {response}" for i, response in enumerate(user_responses)]
            )
    else:
        # Restart or provide feedback
        return "You've completed the interview. Type 'restart' to start over or 'exit' to end."

# Reset functionality
def reset_chatbot():
    global conversation_stage, user_responses, current_question_index
    conversation_stage = 0
    user_responses = []
    current_question_index = 0
    return "The chatbot has been reset. Let's start over!"

# Gradio app
with gr.Blocks() as demo:
    gr.Markdown("# Hiring Assistant Chatbot")
    gr.Markdown("Interact with the AI-powered hiring assistant.")
    
    user_input = gr.Textbox(label="Your Input", placeholder="Type your response here...")
    output = gr.Textbox(label="Chatbot Response")
    submit_button = gr.Button("Submit")
    clear_button = gr.Button("Reset")

    submit_button.click(chatbot_interface, inputs=user_input, outputs=output)
    clear_button.click(reset_chatbot, outputs=output)

# Launch the app
demo.launch()
