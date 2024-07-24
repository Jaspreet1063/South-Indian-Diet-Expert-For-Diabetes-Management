import gradio as gr
import fitz  # PyMuPDF
import os
import re

# Function to load PDF documents
def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Load and process the PDF document
pdf_content = load_pdf("South-Indian-Diet-Plan.pdf")

# Define key topics and their related content
topics = {
    "meal_plan": {
        "keywords": ["meal plan", "breakfast", "lunch", "dinner", "snack"],
        "content": re.search(r"Sample South Indian Meal Plan.*?Snack\s+•\s+1 fresh fruit", pdf_content, re.DOTALL)
    },
    "foods_to_eat": {
        "keywords": ["foods to eat", "eat often", "vegetables", "fruits"],
        "content": re.search(r"Foods to eat often.*?Liquids to drink often", pdf_content, re.DOTALL)
    },
    "foods_to_avoid": {
        "keywords": ["avoid", "foods rich in sugars", "foods rich in fats"],
        "content": re.search(r"Always Avoid!.*?Additional Tips", pdf_content, re.DOTALL)
    },
    "dietary_tips": {
        "keywords": ["tips", "recommendations", "prefer", "avoid"],
        "content": re.search(r"Additional Tips.*?Take-Home Messages", pdf_content, re.DOTALL)
    },
    "diabetes_management": {
        "keywords": ["diabetes", "blood sugar", "dietary restriction"],
        "content": re.search(r"Does diabetes mean going without foods you enjoy\?.*?What types of foods should you eat\?", pdf_content, re.DOTALL)
    }
}

def generate_response(message, history):
    lower_message = message.lower()
    
    # Check which topic the message relates to
    relevant_topic = None
    for topic, data in topics.items():
        if any(keyword in lower_message for keyword in data["keywords"]):
            relevant_topic = topic
            break
    
    if relevant_topic and topics[relevant_topic]["content"]:
        response = topics[relevant_topic]["content"].group().strip()
        # Truncate the response if it's too long
        if len(response) > 500:
            response = response[:500] + "... (truncated for brevity)"
    else:
        response = "I'm sorry, I don't have specific information about that in my knowledge base. Could you try asking about meal plans, foods to eat or avoid, dietary tips, or diabetes management?"

    return response

iface = gr.ChatInterface(
    generate_response,
    title="South Indian Diet Expert for Diabetes Management",
    description="Ask me about South Indian cuisine, diet plans, and nutritional advice for diabetes management!",
    examples=[
        "What's a typical South Indian meal plan for diabetics?",
        "What foods should I eat often in a South Indian diet for diabetes?",
        "What foods should I avoid if I have diabetes?",
        "Can you give me some dietary tips for managing diabetes with South Indian food?",
        "How does diet affect diabetes management?"
    ],
)

iface.launch()