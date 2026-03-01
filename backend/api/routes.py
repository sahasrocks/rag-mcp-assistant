from rag.llm import generate_response
from flask import Blueprint, request, jsonify
from rag.store import vector_store, ingest_text
from rag.llm import generate_response
from agent.orchestrator import Agent

api_bp = Blueprint("api", __name__)
agent = Agent()



@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

@api_bp.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    chunk_count = ingest_text(text)

    return jsonify({
        "message": "Document ingested successfully",
        "chunks_added": chunk_count
    })
@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    session_id = data.get("session_id", "default")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    answer = agent.handle_query(query, session_id)

    return jsonify({"answer": answer})
