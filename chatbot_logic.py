from transformers import AutoTokenizer, AutoModelForCausalLM
import re

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
model.resize_token_embeddings(len(tokenizer))

# Greeting function
def greet_user():
    return "Hello! I'm your hiring assistant. Let's get started!"

# Validate and filter generated questions
def validate_questions(questions):
    valid_questions = [
        q.strip(" -") for q in questions  # Remove leading hyphens or spaces
        if q.strip().endswith("?") and len(q.split()) > 3  # Ends with "?" and has >3 words
    ]
    # Filter out lines that resemble code or commands
    filtered_questions = [
        q for q in valid_questions 
        if not re.match(r'^\s*python\s+-m\s+', q, re.IGNORECASE)
    ]
    return list(set(filtered_questions))[:5]  # Unique and up to 5 questions

# Fallback questions for common tech stacks
fallback_questions = {
    "Python": [
        "What are Python decorators, and how are they used?",
        "Explain the difference between shallow and deep copying in Python.",
        "How does Python manage memory allocation?",
        "Write a Python function to reverse a string.",
        "What is the Global Interpreter Lock (GIL) in Python?"
    ],
    "SQL": [
        "What is the difference between INNER JOIN and OUTER JOIN?",
        "How would you optimize a slow SQL query?",
        "What are indexes, and how do they improve database performance?",
        "Explain the concept of database normalization.",
        "Write a query to find the second highest salary from a table."
    ]
}

# Generate technical questions
def generate_technical_questions(tech_stack):
    prompt = f"""
    You are an expert technical interviewer specializing in {tech_stack}. Generate exactly 3-5 specific, concise, and unique technical interview questions for a candidate skilled in {tech_stack}. 
    The questions must:
    1. Be directly related to {tech_stack}.
    2. End with a question mark.
    3. Avoid including any code, commands, or unrelated content.
    Examples of valid questions:
    - What are Python decorators, and how are they used?
    - How does Python manage memory, and what is garbage collection?
    Now generate the questions:
    """
    
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=200,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1,
        do_sample=True
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    questions = generated_text.split("\n")
    filtered_questions = validate_questions(questions)
    
    if not filtered_questions:
        filtered_questions = fallback_questions.get(tech_stack, ["No questions available for this tech stack."])
    
    return filtered_questions

# Global variables to store conversation state
conversation_stage = "initial"
user_responses = {}
questions = [
    "Please enter your full name:",
    "What is your email address?",
    "Can you share your phone number?",
    "How many years of experience do you have?",
    "What position(s) are you looking for?",
    "Where are you currently located?",
    "Please list your tech stack (e.g., Python, Django, SQL):"
]
current_question_index = 0  # Track the current question

def chatbot_interface(user_input=None):
    global conversation_stage, user_responses, current_question_index

    if conversation_stage == "initial":
        conversation_stage = "gathering_info"
        return greet_user()  # Return greeting

    elif conversation_stage == "gathering_info":
        # Check if this is the first question
        if user_input is None and current_question_index == 0:
            return questions[current_question_index]

        # Save the user's response to the current question
        if current_question_index < len(questions):
            current_question = questions[current_question_index].rstrip(":")
            user_responses[current_question] = user_input
            current_question_index += 1

        # Check if we've reached the end of the questions
        if current_question_index >= len(questions):
            conversation_stage = "generating_questions"
            return "Thank you! Generating technical questions based on your tech stack..."

        # Ask the next question
        return questions[current_question_index]

    elif conversation_stage == "generating_questions":
        tech_stack = user_responses.get("Please list your tech stack (e.g., Python, Django, SQL)")
        if not tech_stack:
            return "No tech stack provided. Please restart the conversation."

        questions = generate_technical_questions(tech_stack)
        if questions:
            conversation_stage = "answering_questions"
            return "\n".join([f"Q{i + 1}: {q}" for i, q in enumerate(questions)])
        else:
            return "Sorry, I couldn't generate technical questions for the provided tech stack."

    elif conversation_stage == "answering_questions":
        return "Thank you for your answers! We'll review them and get back to you shortly."

    else:
        return "Unexpected error. Please restart the conversation."

# Run the chatbot
if __name__ == "__main__":
    print(chatbot_interface())  # Start the chatbot
