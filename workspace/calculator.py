
def calculate(num1, num2, operation):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero is not allowed."
    else:
        return "Error: Invalid operation. Please choose from 'add', 'subtract', 'multiply', or 'divide'."

if __name__ == "__main__":
    print(calculate(10, 5, "add"))
    print(calculate(10, 5, "subtract"))
    print(calculate(10, 5, "multiply"))
    print(calculate(10, 5, "divide"))
    print(calculate(10, 0, "divide"))
    print(calculate(10, 5, "power"))
