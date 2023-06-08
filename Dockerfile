FROM python:3.9

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

# Set the host and port for Streamlit to bind to
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_BROWSER_SERVER_ADDRESS=0.0.0.0

# Expose the port
EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "energy_data.py"]
