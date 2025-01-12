import gradio as gr
from chatbot_logic import chatbot_interface  # Import the modified function

iface = gr.Interface(
    fn=chatbot_interface,
    inputs="text",  # Now accepting text input
    outputs="text",
    title="Hiring Assistant Chatbot",
    description="Interact with the AI-powered hiring assistant.",
)

iface.launch()
