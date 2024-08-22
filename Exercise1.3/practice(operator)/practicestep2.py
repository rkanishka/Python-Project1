# Get input from the user
value1 = float(input("Enter the first value: "))
value2 = float(input("Enter the second value: "))
operator = input("Enter the operator (+ or -): ")

# Perform the operation based on the input
if operator == "+":
    result = value1 + value2
    print(f"{value1} + {value2} = {result}")
elif operator == "-":
    result = value1 - value2
    print(f"{value1} - {value2} = {result}")
else:
    print("Unknown operator")