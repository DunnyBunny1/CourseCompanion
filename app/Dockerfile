# Use Python 3.11 as our base image
FROM python:3.11-slim

# Create /appcode as the CWD in the container - al subsequent
# commands will be relative to this path
WORKDIR /appcode

# Install sys-level dependencies 
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  software-properties-common \
  git \
  # Clean up the apt cache to reduce img size
  && rm -rf /var/lib/apt/lists/*

# RUN mkdir /requirements
# COPY ./src/requirements.txt /requirements/requirements.txt

# Copy reqs.txt from host to container's cwd (/appcode)
COPY ./src/requirements.txt .

# Install all python deps into our container from our reqs
RUN pip3 install -r requirements.txt

# Debugging: list contents of CWD
RUN ls

# Listen on port 8501 at runtime (default streamlit port)
EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"] 

# Command to run at run-time - run the streamlit app from home.py
# Run on port 8501 and make the server accessible on all network interfaces
# (0.0.0.0), ensuring srever accessible from outside container
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
