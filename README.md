# HiringAssistant-TalentScout-

URL: https://huggingface.co/spaces/Nsain25/TalentScout

This project involves building a Technical Interview Chatbot powered by OpenAI's gpt-neo-1.3B model. The chatbot generates technical interview questions based on a specified tech stack, collects user answers, and supports features like question validation, fallback mechanisms, and debugging. The chatbot also ensures robust filtering of irrelevant or command-like content from the model's output.

**Features**
Dynamic Question Generation:
- Generates 3-5 concise, unique, and practical technical interview questions for a specified tech stack.
- Ensures questions focus on real-world applications.

User Interaction:
- Collects candidate information (name, email, experience, position, etc.).
- Displays questions and allows users to provide answers.

Question Validation:
- Retains only valid questions ending with a question mark (?) and containing more than three words.
- Filters out irrelevant content, including command-like lines or incomplete outputs.

Fallback Mechanism:
- Predefined questions for popular tech stacks (e.g., Python, SQL) are used if the model fails to generate valid questions.

Debugging and Logging:
- Logs raw model output for troubleshooting and refinement.

Configurable Model Behavior:
- Uses sampling (do_sample=True) with temperature and nucleus sampling (top_p) for creative and varied outputs.

**Flow of Execution**
- Candidate Information Collection:
Prompts the user to enter details like name, email, experience, and preferred tech stack.

Question Generation:
- Generates questions using gpt-neo-1.3B based on the provided tech stack.
- Validates and filters the output, ensuring only meaningful and relevant questions are presented.

Fallback Handling:
- If no valid questions are generated, predefined fallback questions for the tech stack are displayed.

User Answers:
- Allows users to provide answers to the generated or fallback questions.
- Displays a summary of the user's responses.

End Conversation: 
- Concludes with a polite message, thanking the user for their time.

**Code Highlights**
Prompt Design: The model is instructed explicitly to avoid including commands, code snippets, or unrelated content in the output.
Question Validation: Ensures questions meet specific criteria (e.g., end with ? and have more than three words).
Fallback Questions: Predefined questions are displayed for common tech stacks (e.g., Python, SQL) if the model fails to generate valid ones.
Debugging and Logs: Logs raw model output for analysis
Diverse Output Generation: Uses do_sample=True, temperature=0.7, and top_p=0.9 for varied and creative question generation.

**Dependencies**
Python Libraries:
- transformers: For the OpenAI gpt-neo model and tokenizer.
- re: For regex-based filtering of irrelevant content.
Model:
- EleutherAI/gpt-neo-1.3B: A lightweight language model for generating questions.

**Future Improvements**
Support for Multilingual Questions: Expand the chatbot to generate questions in multiple languages.
Integration with a Web Interface: Use tools like Streamlit for a user-friendly interface.
Enhanced Question Generation: Use a more advanced model, such as gpt-neo-2.7B, for improved output quality.
Answer Validation: Incorporate logic to validate user answers against predefined solutions.
Data Persistence: Save candidate information and responses to a database or CSV for future reference.
