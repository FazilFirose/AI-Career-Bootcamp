print("="*30)
print("      SMART CALCULATOR")
print("="*30)
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("5. Exit")
while True:
 choice = input("\nChoose an option (1-5): ")
 if choice == "1":
    print("you chose Addition!")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    result = num1 + num2

    print("Result:", result)
 elif choice == "2":
    print("you chose Subtraction!")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print("Result:", num1 - num2)

 elif choice == "3":
    print("you chose Multiplication!")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print("Result:", num1 * num2)

 elif choice == "4":
    print("you chose Division!")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if num2 == 0:
        print("Cannot divide by zero!")
    else:
        print("Result:", num1 / num2)

 elif choice == "5":
    print("Thank you for using Smart Calculator!")
    break

 else:
    print("Invalid choice!")