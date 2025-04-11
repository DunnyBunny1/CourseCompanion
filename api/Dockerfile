# Use python as our base image
FROM python:3.11-slim

# Set /apicode as our CWD
WORKDIR /apicode

# Copy over our requirements file into the img (w/o caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from our api folder into our image's cWD
COPY . .

# Expose port 4k
EXPOSE 4000

# Run the backend_app.py file at runtime
CMD [ "python", "backend_app.py"]

