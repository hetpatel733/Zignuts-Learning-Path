def sum_primes(n):
    primes, num = [], 2
    while len(primes) < n:
        if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
            primes.append(num)
        num += 1
    return sum(primes)

print(sum_primes(6))