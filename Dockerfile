FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Zig
RUN wget https://ziglang.org/download/0.10.0/zig-linux-x86_64-0.10.0.tar.xz && \
    tar -xf zig-linux-x86_64-0.10.0.tar.xz && \
    mv zig-linux-x86_64-0.10.0 /usr/local/zig && \
    ln -s /usr/local/zig/zig /usr/local/bin/zig

# Copy the Zig source code
COPY performance_module.zig /app/performance_module.zig

# Compile the Zig code into a shared library
RUN zig build-lib -fPIC -dynamic /app/performance_module.zig -o /app/libperformance_module.so

# Install Python dependencies
RUN pip install --no-cache-dir flask pandas pyarrow

# Copy the Python server code
COPY server_2.py /app/server_2.py

# # Copy the Python server code
# COPY server.py /app/server.py

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "server_2.py"]

# # Command to run the application
# CMD ["python", "server.py"]