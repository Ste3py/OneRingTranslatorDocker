FROM python:3.11-slim

WORKDIR /app

COPY . /app/

ENV HOST=0.0.0.0
ENV PORT=4990
ENV CORE_CONFIG=""
ENV OFFLINE_MODE=false

ENV BLOOMZ_CONFIG=""
ENV CUSTOM_LIBRE_TRANSLATE_CONFIG=""
ENV DEEPL_CONFIG=""
ENV FB_MBART50_CONFIG=""
ENV FB_NLLB_CTRANSLATE2_CONFIG=""
ENV FB_NLLB_TRANSLATE_CONFIG=""
ENV GEMINI_CHAT_CONFIG=""
ENV GOOGLE_TRANSLATE_CONFIG=""
ENV KOBOLDAPI_TRANSLATE_CONFIG=""
ENV LIBRE_TRANSLATE_CONFIG=""
ENV LINGVANEX_CONFIG=""
ENV MULTI_SOURCES_CONFIG=""
ENV NO_TRANSLATE_CONFIG=""
ENV NO_TRANSLATE2_CONFIG=""
ENV OPENAI_CHAT_CONFIG=""
ENV OPUS_MT_CONFIG=""
ENV T5_MT_CONFIG=""
ENV USE_MID_LANG_CONFIG=""
ENV VSEGPT_CHAT_CONFIG=""

ENV PIP_CACHE_DIR=/cache/pip

EXPOSE ${PORT}


CMD echo "Installation des dépendances requirements.txt..."; \
    pip install -r requirements.txt; \
    if [ "$OFFLINE_MODE" = "true" ]; then \
      if [ -f "requirements-offline.txt" ]; then \
        echo "Mode offline activé, installation des dépendances offline..."; \
        pip install -r requirements-offline.txt; \
      else \
        echo "Mode offline activé mais requirements-offline.txt introuvable."; \
      fi; \
    fi && \
    python run_webapi.py

