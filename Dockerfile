# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /DATAFUSION

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port the API will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:test_api", "--host", "0.0.0.0", "--port", "8000"]
