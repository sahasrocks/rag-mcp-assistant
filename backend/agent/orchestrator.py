from rag.store import vector_store
from rag.llm import generate_response
from mcp.server import MCPServer
from tools.code_tool import generate_code
from tools.architecture_tool import explain_architecture
from memory.service import save_message, get_conversation_history

class Agent:

    def __init__(self):
        self.mcp = MCPServer()

        # Register tools
        self.mcp.register_tool(
            "code_tool",
            "Generate backend production code",
            generate_code
        )

        self.mcp.register_tool(
            "architecture_tool",
            "Provide detailed system design explanation",
            explain_architecture
        )

    def decide(self, query):
        lower_q = query.lower()

        if "write" in lower_q or "code" in lower_q or "example" in lower_q:
            return "code_tool"

        if "design" in lower_q or "architecture" in lower_q:
            return "architecture_tool"

        if "explain" in lower_q or "what is" in lower_q:
            return "rag_tool"

        # fallback to LLM
        tools = self.mcp.list_tools()

        tool_descriptions = "\n".join(
            [f"{name}: {desc}" for name, desc in tools.items()]
        )

        prompt = f"""
    Available tools:
    {tool_descriptions}

    User query:
    {query}

    Respond ONLY with:
    CALL:<tool_name>
    or DIRECT
    """

        decision = generate_response(prompt).strip()

        if decision.startswith("CALL:"):
            return decision.replace("CALL:", "").strip()

        return "direct"
    def handle_query(self, query, session_id="default"):

        # Save user message
        save_message(session_id, "user", query)

        # Load memory
        history = get_conversation_history(session_id)

        history_text = ""
        for msg in history:
            history_text += f"{msg.role.upper()}: {msg.message}\n"

        # 🔥 Step 1: Try RAG first
        retrieval_results = vector_store.search(query)

        if retrieval_results:
            best_score = retrieval_results[0]["score"]

            # Lower distance = more relevant
            RAG_THRESHOLD = 0.8  # you may tune this

            if best_score < RAG_THRESHOLD:
                context = "\n\n".join(
                    [r["text"] for r in retrieval_results]
                )

                prompt = f"""
            Conversation History:
            {history_text}

            You are an intelligent assistant.

            Use the retrieved context below to answer the user's question.
            Adapt your response to the domain of the context.
            If the context is insufficient, say that clearly.

            Retrieved Context:
            {context}

            User Question:
            {query}

            Answer:
            """
                response = generate_response(prompt)

                save_message(session_id, "assistant", response)
                return response

        # 🔥 Step 2: If RAG not confident → use MCP tools
        decision = self.decide(query)

        if decision == "direct":
            response = self.handle_direct(query, history_text)

        elif decision in self.mcp.tools:
            tool_result = self.mcp.call_tool(decision, query)

            final_prompt = f"""
    Conversation History:
    {history_text}

    Tool Result:
    {tool_result}

    Provide final answer:
    """
            response = generate_response(final_prompt)

        else:
            response = self.handle_direct(query, history_text)

        save_message(session_id, "assistant", response)
        return response
    

    def handle_direct(self, query, history_text=""):
        prompt = f"""
    Conversation History:
    {history_text}

    User Question:
    {query}

    Answer clearly and concisely.
    """
        return generate_response(prompt)

    def handle_rag(self, query):
        relevant_chunks = vector_store.search(query)
        context = "\n\n".join(relevant_chunks)

        prompt = f"""
    You are a senior system design expert.

    Use the provided context to answer clearly and technically.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
        return generate_response(prompt)
