import gradio as gr
from huggingface_hub import InferenceClient

# Load a lightweight model, you can change this to a better model if you have access
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token="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"
)


# Customize system prompt for a farming assistant
system_prompt = (
    "You are a helpful assistant for Indian farmers. "
    "Provide advice on agriculture, crop care, fertilizers, weather impact, and pest control. "
    "Use simple and clear language in English."
)

# Function to get bot response
def get_response(message, history):
    full_prompt = system_prompt + "\n"
    for user, bot in history:
        full_prompt += f"Farmer: {user}\nAssistant: {bot}\n"
    full_prompt += f"Farmer: {message}\nAssistant:"

    try:
        response = client.text_generation(
            prompt=full_prompt,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
        )
        return response.strip()
    except Exception as e:
        return f"❌ Error from Hugging Face: {str(e)}"


# Gradio Chat Interface
chat = gr.ChatInterface(fn=get_response,
                        chatbot=gr.Chatbot(label="Farmer's Assistant"),
                        title="🌾 Farmer's Assistant Bot",
                        description="Ask questions about crops, fertilizers, pests, and more.",
                        theme="default")

# Launch app
chat.launch()
