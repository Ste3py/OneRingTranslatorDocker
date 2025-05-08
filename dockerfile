FROM python:3.11-slim

WORKDIR /app

COPY . /app/

ENV HOST=0.0.0.0
ENV PORT=4990
ENV CORE_CONFIG=""
ENV REQUIREMENTS_FILE=requirements.txt

EXPOSE ${PORT}


CMD if [ -f "$REQUIREMENTS_FILE" ]; then \
      echo "Installation des dépendances depuis $REQUIREMENTS_FILE..."; \
      pip install --no-cache-dir -r "$REQUIREMENTS_FILE"; \
    else \
      echo "Aucun fichier $REQUIREMENTS_FILE trouvé. Skip install."; \
    fi && \
    python run_webapi.py