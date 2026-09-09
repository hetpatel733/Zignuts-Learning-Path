def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b

def calculator():
    print("=" * 30)
    print("   Simple Calculator")
    print("=" * 30)
    print("Operations:")
    print("  1. Addition       (+)")
    print("  2. Subtraction    (-)")
    print("  3. Multiplication (*)")
    print("  4. Division       (/)")
    print("  5. Exit")
    print("=" * 30)

    while True:
        print()
        choice = input("Choose operation (1/2/3/4/5): ")

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            continue

        if choice == "1":
            result = add(num1, num2)
            symbol = "+"
        elif choice == "2":
            result = subtract(num1, num2)
            symbol = "-"
        elif choice == "3":
            result = multiply(num1, num2)
            symbol = "*"
        elif choice == "4":
            result = divide(num1, num2)
            symbol = "/"

        print(f"\n{num1} {symbol} {num2} = {result}")

if __name__ == "__main__":
    calculator()
