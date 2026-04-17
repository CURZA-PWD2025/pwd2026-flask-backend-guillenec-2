FROM python:3.14
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Crear usuario no-root y darle propiedad del directorio de trabajo
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["flask", "--app", "run.py", "run", "--debug", "--host=0.0.0.0"]
