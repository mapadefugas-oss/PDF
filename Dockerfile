FROM python:3.13-slim-bookworm

# System libraries WeasyPrint needs (Pango, Cairo, HarfBuzz, fonts).
# Pinned to Debian 12 "bookworm" specifically because these exact package
# names (e.g. libgdk-pixbuf2.0-0) were renamed in Debian 13 "trixie", which
# is what the untagged python:3.13-slim image moved to.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=8000
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "60", "app:app"]
