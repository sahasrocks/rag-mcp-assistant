from flask import Flask
from api.routes import api_bp
from memory.models import init_db
from rag.store import ingest_folder

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    init_db()
    chunk_count = ingest_folder()
    print(f"Loaded {chunk_count} chunks from documents folder.")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)