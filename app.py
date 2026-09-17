import os

from flask import Flask, request, send_file, jsonify
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

API_KEY = os.environ.get("PDF_SERVICE_API_KEY", "")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/generate")
def generate():
    if API_KEY:
        provided = request.headers.get("X-Api-Key", "")
        if provided != API_KEY:
            return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    html = data.get("html")
    filename = data.get("filename", "reporte.pdf")

    if not html:
        return jsonify({"error": "missing 'html' field"}), 400

    pdf_bytes = HTML(string=html).write_pdf()

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
