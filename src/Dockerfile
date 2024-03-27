# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

ENV APIVERSION=1.1.0

EXPOSE 8080

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY gallery_api_impl gallery_api_impl

# RUN uvicorn gallery_api_impl.main:app --host 0.0.0.0 --port 8080
CMD ["uvicorn", "gallery_api_impl.main:app", "--host", "0.0.0.0", "--port", "8080"]
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "gallery_api_impl.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]