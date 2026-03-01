from rag.llm import generate_response

def generate_code(query):
    prompt = f"""
Generate clean production-ready code relevant to the query domain.

Request:
{query}

Return only code.
"""
    return generate_response(prompt)