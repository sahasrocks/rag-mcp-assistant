from rag.llm import generate_response

def explain_architecture(query):
    prompt = f"""
You are a senior technical architect.

Provide structured explanation relevant to the query domain.

Question:
{query}
"""
    return generate_response(prompt)