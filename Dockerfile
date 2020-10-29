# Use the official image as a parent image.
FROM python:3

# Set the working directory.
WORKDIR /usr/src/labs/shopping-site

# Copy all the files to the container
COPY . .

# Install dependencies.
RUN pip3 install --no-cache-dir -r requirements.txt

# The port number that container should expose.
EXPOSE 8080

# Run the specified command within the container.
CMD [ "python3", "./shoppingsite.py" ]