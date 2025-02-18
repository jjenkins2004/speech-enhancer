# Compiler and flags
CC = gcc
CFLAGS = -O2 -Wall -fPIC -I../rnnoise/include \
         -I$(shell python3 -c "import numpy; print(numpy.get_include())") \
         $(shell python3-config --includes)

LDFLAGS = -shared \
          -L../rnnoise/.libs \
          -Wl,-rpath,@loader_path/../rnnoise/.libs \
          -lrnnoise \
          $(shell python3.11-config --ldflags) \
          -lpython3.11

# Source files
SRCS = noise_reduction.c
OBJS = $(SRCS:.c=.o)

# Output shared library (Python module)
TARGET = noise_reduction.so

# Default rule: compile the shared library
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $(TARGET)

# Clean up compiled files
clean:
	rm -f $(OBJS) $(TARGET)
