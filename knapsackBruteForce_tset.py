from contextlib import redirect_stdout
import matplotlib.pyplot as plt
import itertools
import argparse
import time


def time_knapsack(type: str, total: int, coins: list[int]) -> tuple[bool, float]: 

    start_time = time.time()

    print(f"Solving knapsack for Type: {type}, Total: {total}, Coins: {coins}")

    # Bruteforce method: attempt every possible combination 
    for r in range(1, total + 1):
        for combination in itertools.combinations_with_replacement(coins, r):
            if sum(combination) == total:
                print(f"Solution found: {combination}")
                return (True, time.time() - start_time)

    print("No solution")

    return (False, time.time() - start_time)

def main():
    # Handle arguments
    parser = argparse.ArgumentParser(
        prog='read_knapsack_test_cases',
        description='Reads the test cases generated for the knapsack problem and prints them.'
    )

    # Add argument to specify the file to read
    parser.add_argument("--test_file", "-tf", required=True, type=argparse.FileType('r'), help="File containing the test cases to read.")
    parser.add_argument("--fail_file", "-ff", required=True, type=argparse.FileType('r'), help="File containing the guaranteed fails to read.")
    parser.add_argument("--log_file", "-lf", required=True, type=str, help="File to log the output.")

    args = parser.parse_args()

    # If something went wrong and the file cannot be opened, exit with error
    if (not args.file):
        print("Error opening file.")
        return

    # Lists to store data for plotting
    total_values_success   = []
    total_values_failure   = []
    elapsed_times_success  = []
    elapsed_times_failures = []

    # Redirect output to the log file
    with open(args.log_file, 'w') as log:
        with redirect_stdout(log):

            # Process the regular test cases
            with args.test_file as file:
                for line in file:
                    line         = line.strip().split(',')
                    result       = time_knapsack(line[0], int(line[1]), [int(x) for x in line[2:]])
                    elapsed_time = result[1]
                    print(f"Time taken for test case: {elapsed_time:.6f}\n")

                    # Store the total and elapsed time 
                    if result[0]:
                        total_values_success.append(int(line[1]))
                        elapsed_times_success.append(elapsed_time)
                    else:
                        total_values_failure.append(int(line[1]))
                        elapsed_times_failures.append(elapsed_time)

            # Process the guaranteed fails
            with args.fail_file as file:
                for line in file:
                    line         = line.strip().split(',')
                    result       = time_knapsack(line[0], int(line[1]), [int(x) for x in line[2:]])
                    elapsed_time = result[1]
                    print(f"Time taken for guaranteed fail case: {elapsed_time:.6f}\n")

                    # Store the total and elapsed time
                    total_values_failure.append(int(line[1]))
                    elapsed_times_failures.append(elapsed_time)

            # Plot the results
            plt.figure(figsize=(10, 6))
            
            # Plot successes in green
            plt.plot(sorted(total_values_success), sorted(elapsed_times_success), marker='o', linestyle='-', color='g', label='Successes')
            
            # Plot failures in red (both from test cases and guaranteed fails)
            plt.plot(sorted(total_values_failure), sorted(elapsed_times_failures), marker='x', linestyle='--', color='r', label='Failures')

            plt.title('Elapsed Time vs Total Amount for Knapsack Problem')
            plt.xlabel('Total Amount')
            plt.ylabel('Elapsed Time (seconds)')
            plt.grid()
            plt.legend()
            plt.show()

    args.file.close()

    return 0

if __name__ == '__main__':
    main()