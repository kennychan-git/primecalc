import math
import time
from multiprocessing import Pool, freeze_support


def is_prime(num):
    # Check if number is less than 2
    if num < 2:
        return False

    # Check if number is divisible by 2
    if num == 2:
        return True

    # Check if number is divisible by any odd integer between 3 and the square root of the number
    if num % 2 == 0:
        return False

    for i in range(3, int(math.isqrt(num)) + 1, 2):
        if num % i == 0:
            return False

    # If number is not divisible by any integer, it is prime
    return True


def factorize_chunk(args):
    num, start, end = args
    factors = []
    for i in range(start, end):
        if num % i == 0:
            factors.append(i)
            factors.append(num // i)
    return factors


def factorize(num):
    factors = []
    with Pool() as pool:
        sqrt_num = int(math.isqrt(num)) + 1
        chunk_size = sqrt_num // pool._processes
        # Ensure chunk size is at least 1
        chunk_size = max(1, chunk_size)
        chunks = [(num, i, i + chunk_size) for i in range(1, sqrt_num, chunk_size)]
        results = pool.map(factorize_chunk, chunks)
        pool.close()
        pool.join()
        factors = [factor for sublist in results for factor in sublist]
    factors = list(set(factors))  # Remove duplicates
    factors.sort()
    return factors


if __name__ == "__main__":
    while True:
        # Prompt user for input
        num = int(input("Enter a positive integer to check if it is a prime number: "))

        # Start the timer
        start_time = time.time()

        # Check if input number is prime
        if is_prime(num):
            print(f"{num} is a prime number.")
        else:
            factors = factorize(num)
            print(f"{num} is not a prime number.")
            print("Factors of", num, ":", factors)

        # Calculate and print the time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time elapsed: {elapsed_time} seconds.")

        # Prompt for retry or exit
        retry = input("Press 'r' to retry or Enter to exit: ")
        if retry != 'r':
            break
