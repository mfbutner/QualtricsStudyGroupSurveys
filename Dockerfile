FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN groupadd -g 1001 appgroup && \
    useradd -m -u 1001 -g appgroup appuser
COPY --chown=appuser:appgroup . ./
USER appuser:appgroup
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]