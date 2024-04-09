import subprocess

def run_command(command=None):

    command = "ls -l"

    # Run the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Capture the output
    output, error = process.communicate()

    # Decode the output
    output = output.decode()
    error = error.decode()

    # Print the output and error if any
    print("Output:")
    print(output)
    print("Error:")
    print(error)


if __name__=="__main__":
    run_command()
