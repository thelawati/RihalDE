FROM python:3.10-slim

WORKDIR /etl

# System dependencies for OCR & PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ETL scripts and data
COPY etl/ .

# Run the renamed etl.py script
CMD ["python", "etl.py"]