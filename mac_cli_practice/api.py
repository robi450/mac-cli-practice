from flask import Flask, request, jsonify

from .core import (
    generate_summary,
    list_summaries,
    configure_defaults,
    load_config,
)

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/summaries")
    def summaries():
        files = list_summaries()
        data = [
            {
                "name": f.name,
                "path": str(f.resolve()),
            }
            for f in files
        ]
        return jsonify({"count": len(data), "summaries": data}), 200

    @app.post("/generate")
    def generate():
        body = request.get_json(silent=True) or {}
        config = load_config()

        name = body.get("name") or config.get("default_name") or "Example User"
        topic = body.get("topic") or config.get("default_topic") or "General"

        path = generate_summary(name, topic)
        return jsonify(
            {
                "message": "summary created",
                "name": name,
                "topic": topic,
                "path": str(path.resolve()),
            }
        ), 201

    @app.post("/config")
    def config():
        body = request.get_json(silent=True) or {}
        name = body.get("name")
        topic = body.get("topic")

        if not name and not topic:
            return jsonify({"error": "Nothing to configure. Provide 'name' and/or 'topic'."}), 400

        data = configure_defaults(name, topic)
        return jsonify({"message": "configuration saved", "config": data}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    # Dev mode: debug=True so you see changes live
    app.run(host="127.0.0.1", port=5000, debug=True)
