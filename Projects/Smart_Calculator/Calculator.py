from datetime import datetime
def show_menu():
  print("="*30)
  print("     SMART CALCULATOR V2")
  print("="*30)
  print("1. Addition")
  print("2. Subtraction")
  print("3. Multiplication")
  print("4. Division")
  print("5. Show History")
  print("6. Clear History")
  print("7. Exit")
def save_history(calculation):
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    with open("history.txt", "a") as file:
        file.write(f"[{current_time}] {calculation}\n")
def get_number(msg):
   while True:
      try:
         return float(input(msg))
      except ValueError:
         print("invalid input!, Plese enter numbers Only")
def addition():
     print("you chose Addition!")
     num1 = get_number("Enter first number: ")
     num2 = get_number("Enter second number: ")
     result = num1 + num2
     print("="*30)
     print("  Result:", result)
     print("="*30)
     save_history(f"{num1} + {num2} = {result}")
def subtraction():
   print("you chose Subtraction!")
   num1 = get_number("Enter first number: ")
   num2 = get_number("Enter second number: ")
   result = num1-num2
   print("="*30)
   print("  Result:", result)
   print("="*30)
   save_history(f"{num1} - {num2} = {result}")
def multiplication():
   print("you chose Multiplication!")
   num1 = get_number("Enter first number: ")
   num2 = get_number("Enter second number: ")
   result = num1 * num2
   print("="*30)
   print("  Result:", result)
   print("="*30)
   save_history(f"{num1} * {num2} = {result}")
def division():
   print("you chose Division!")
   num1 = get_number("Enter first number: ")
   num2 = get_number("Enter second number: ")

   if num2 == 0:
        print("Cannot divide by zero!")
   else:
       result = num1/num2
       print("="*30)
       print("  Result:", result)
       print("="*30)
       save_history(f"{num1} / {num2} = {result}")
def view_history():
    try:
        with open("history.txt", "r") as file:
            history = file.read()

            if history:
                print("\n===== HISTORY =====")
                print(history)
            else:
                print("History is empty.")

    except FileNotFoundError:
        print("No history found.")
def clear_history():
    with open("history.txt", "w") as file:
        pass

    print("History Cleared!")
def pause():
    input("\nPress Enter to continue...")
while True:
 show_menu()
 choice = input("\nChoose an option (1-7): ")
 if choice == "1":
    addition()
    pause()
 elif choice == "2":
    subtraction()
    pause()

 elif choice == "3":
    multiplication()
    pause()

 elif choice == "4":
    division()
    pause()
 elif choice == "5":
    view_history()
    pause()
 elif choice == "6":
    clear_history()
    pause()
 elif choice == "7":
    print("Thank you for using Smart Calculator!")
    break

 else:
    print("Invalid choice!")