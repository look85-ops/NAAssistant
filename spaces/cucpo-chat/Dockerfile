FROM python:3.10-slim

# Install useful OS deps for healthchecks and runtime
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (HF expects uid 1000)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

COPY --chown=user requirements.txt ./

# Upgrade pip and install deps
RUN pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio

COPY --chown=user . /app

EXPOSE 7860
CMD ["python", "app.py"]
