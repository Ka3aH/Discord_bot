import json
import os

KNOWLEDGE_BASE_FILE = 'SF_GPT_Library.json'

def load_knowledge_base():
    """Загрузка базы знаний из файла JSON."""
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        raise FileNotFoundError(f"Knowledge base file {KNOWLEDGE_BASE_FILE} does not exist.")
    with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_knowledge_response(query):
    """Получение ответа из базы знаний на основе запроса."""
    knowledge_base = load_knowledge_base()
    for item in knowledge_base:
        if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
            return item['content']
    return "Извините, я не могу ответить на этот вопрос, так как я создан для помощи по SoftField."
