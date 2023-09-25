import re
import sys 

if len(sys.argv) != 2:
    print("Usage: python script.py logpath")
    sys.exit(1)
FILE_PATH = sys.argv[1]     # log.txt file


def retrieve_iterations_average(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regular expressions to find all numbers after "Number of iterations: "
    pattern = r'Number of iterations           : (\d+)'
    matches = re.findall(pattern, content)

    # Convert the matched numbers to integers and compute the average
    iterations = [int(match) for match in matches]
    average = sum(iterations) / len(iterations)
    averagelast = sum(iterations[-1000:]) / len(iterations[-1000:])

    return average,averagelast

# Usage 
average_iterations = retrieve_iterations_average(FILE_PATH)
print(f"Average number of iterations: {average_iterations[0]}")
print(f"Average last 1000 iterations: {average_iterations[1]}")