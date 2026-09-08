try:
    num1 = float(input("Enter the first number: "))
    operator = input("Enter an operator (+, -, *, /): ")
    num2 = float(input("Enter the second number: "))

    if operator == '+':
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")

    elif operator == '-':
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")

    elif operator == '*':
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")

    elif operator == '/':
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")

    else:
        print("Error: Invalid operator entered. Please use +, -, *, or /.")

except ValueError:
    print("Error: Invalid input. Please enter valid numbers.")
