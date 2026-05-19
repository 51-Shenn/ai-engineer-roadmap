import os

os.system("clear")

file_path = "files/file.txt"

# read
with open(file_path, "r") as f:
    # content = f.read() # reads all content
    # content = f.readline() # only read the first line of the file
    content = f.readlines() # returns a list of lines in the file
    print(content)

# overwrite
with open(file_path, "w") as f:
    f.write("Hello python, wassup!\n")

# append
with open(file_path, "a") as f:
    f.write("This is after append!\n")

# read + write
with open(file_path, "r+") as f:
    content = f.read()
    print(content.strip())
    f.write("This is inserted using r+\n")

    f.seek(0) # this will let the pointer to go back to the start
    new = f.readlines()
    print(new)

with open("files/file-create.txt", "w+") as f:
    pass

# r+ (read + write, no overwrite)
# - File must exist
# - Pointer starts at beginning
# - Does not delete content
# - Writing overwrites from current position
# - Good for modifying existing content

# w+ (write + read, overwrite)
# - File will be created if not exist
# - Deletes all existing content immediately
# - Pointer starts at beginning
# - Good when you want a fresh file

# a+ (append + read)
# - File will be created if not exist
# - Pointer starts at end for writing
# - Writing always adds to the end
# - You can read, but may need `seek(0)`
# - Good for logging / adding data without touching old content

# Modify existing file => r+
# Start fresh => w+
# Never lose data => a+
