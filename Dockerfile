# Use a minimal base image
FROM python:3.9-alpine

# Set working directory
WORKDIR /home/data

# Copy files
COPY scripts.py /home/data/
COPY home/data/ /home/data/

# Install dependencies and create the output directory in a single layer
RUN apk add --no-cache python3 py3-pip && mkdir -p /home/data/output

# Define the command to run the script
CMD ["sh", "-c", "python /home/data/scripts.py && cat /home/data/output/result.txt"]
