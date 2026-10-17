"""
================================================================================
Project     : Menu-Driven Bank Account Simulator
Description : A beginner-friendly, clean, and well-commented banking simulator
              supporting balance inquiries, deposits, withdrawals, and 
              transaction history tracking.
Objective   : Practice functions, loops, validation, and state management.
Level       : Level 1 Python Internship
================================================================================
"""

import sys
from datetime import datetime

# Ensure UTF-8 output encoding for terminal support across Windows/Linux/macOS
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
# Currency symbol used throughout the simulator. You can change this to '$', '€', etc.
CURRENCY_SYMBOL = "₹"


# ==============================================================================
# HELPER / VALIDATION FUNCTIONS
# ==============================================================================
def prompt_positive_float(prompt_message):
    """
    Safely prompts the user for a numeric float amount.
    
    Beginner-Friendly Concept: Input Validation & Exception Handling
    - Uses a `while True` loop so the user is prompted repeatedly until valid input.
    - Uses `try ... except ValueError` to gracefully intercept non-numeric text 
      (like 'abc', '$50', empty strings) without crashing the program.
    - Enforces non-negative values. Entering 0 is treated as a cancellation request.
    - Rounds input to 2 decimal places to prevent floating-point precision issues.

    Parameters:
        prompt_message (str): Text prompt displayed to the user.

    Returns:
        float: A validated numeric amount >= 0.0.
    """
    while True:
        raw_input = input(prompt_message).strip()

        # Reject empty inputs
        if not raw_input:
            print("\n❌ Input cannot be empty. Please enter a valid number.")
            continue

        try:
            amount = float(raw_input)

            # Reject negative values
            if amount < 0:
                print("\n❌ Negative amounts are not allowed. Please enter a positive number (or 0 to cancel).")
                continue

            # Return rounded value to 2 decimal places (standard for currency)
            return round(amount, 2)

        except ValueError:
            # Handle non-numeric input gracefully
            print(f"\n❌ '{raw_input}' is not a valid number. Please enter digits only (e.g., 500 or 150.50).")


# ==============================================================================
# CORE BANKING OPERATIONS
# ==============================================================================
def check_balance(balance):
    """
    Displays the current available account balance.
    
    Beginner-Friendly Concept: String Formatting & Passing Immutable State
    - In Python, numbers (int, float) are immutable.
    - We receive `balance` as a parameter and display it nicely formatted.
    - `,:,.2f` formats numbers with thousand commas and exactly two decimal places
      (e.g., 1000 becomes 1,000.00).

    Parameters:
        balance (float): Current account balance.
    """
    print("\n" + "=" * 45)
    print("              ACCOUNT BALANCE")
    print("=" * 45)
    print(f"  Available Balance : {CURRENCY_SYMBOL}{balance:,.2f}")
    print("=" * 45)


def deposit(balance, transactions, amount=None):
    """
    Deposits funds into the bank account and records the transaction.
    
    Beginner-Friendly Concept: State Mutation & Returning Updated State
    - Floats are immutable, so this function calculates and returns the new balance.
    - Lists are mutable, so `transactions.append(...)` updates the transaction list
      directly without needing to return it.
    - The optional `amount` parameter allows direct calls during automated testing.
      If `amount` is None, it interactively prompts the user for input.

    Parameters:
        balance (float): Current account balance before deposit.
        transactions (list): List of recorded transaction dictionaries.
        amount (float, optional): Direct deposit amount (defaults to None for interactive input).

    Returns:
        float: Updated account balance after deposit (or unchanged if cancelled/invalid).
    """
    # Interactive input if amount was not explicitly passed
    if amount is None:
        print("\n--- Deposit Funds ---")
        amount = prompt_positive_float(f"Enter amount to deposit (or 0 to cancel): {CURRENCY_SYMBOL}")
        if amount == 0.0:
            print("ℹ️  Deposit cancelled. Returning to main menu.")
            return balance

    # Validation: deposit amount must be strictly greater than 0
    if amount <= 0:
        print("❌ Error: Deposit amount must be greater than zero.")
        return balance

    amount = round(amount, 2)
    new_balance = round(balance + amount, 2)

    # Create transaction record dictionary
    # Storing timestamp, transaction type, amount, and balance after
    record = {
        "type": "Deposit",
        "amount": amount,
        "balance_after": new_balance,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    transactions.append(record)

    # User feedback
    print("\n" + "-" * 45)
    print("  ✅ DEPOSIT SUCCESSFUL")
    print("-" * 45)
    print(f"  Deposited Amount : {CURRENCY_SYMBOL}{amount:,.2f}")
    print(f"  New Balance      : {CURRENCY_SYMBOL}{new_balance:,.2f}")
    print("-" * 45)

    return new_balance


def withdraw(balance, transactions, amount=None):
    """
    Withdraws funds from the bank account after checking for sufficient balance.
    
    Beginner-Friendly Concept: Business Logic & Condition Checks
    - Validates that the requested amount does not exceed the current balance.
    - If funds are insufficient, displays a clear warning and keeps balance intact.
    - If valid, deducts the amount, records the transaction, and returns the new balance.

    Parameters:
        balance (float): Current account balance before withdrawal.
        transactions (list): List of recorded transaction dictionaries.
        amount (float, optional): Direct withdrawal amount (defaults to None for interactive input).

    Returns:
        float: Updated account balance after withdrawal (or unchanged if failed).
    """
    # Interactive input if amount was not explicitly passed
    if amount is None:
        print("\n--- Withdraw Funds ---")
        amount = prompt_positive_float(f"Enter amount to withdraw (or 0 to cancel): {CURRENCY_SYMBOL}")
        if amount == 0.0:
            print("ℹ️  Withdrawal cancelled. Returning to main menu.")
            return balance

    # Validation: withdrawal amount must be strictly greater than 0
    if amount <= 0:
        print("❌ Error: Withdrawal amount must be greater than zero.")
        return balance

    amount = round(amount, 2)

    # Condition Check: Insufficient Funds
    if amount > balance:
        print("\n" + "-" * 45)
        print("  ❌ TRANSACTION FAILED: INSUFFICIENT FUNDS")
        print("-" * 45)
        print(f"  Available Balance : {CURRENCY_SYMBOL}{balance:,.2f}")
        print(f"  Requested Amount  : {CURRENCY_SYMBOL}{amount:,.2f}")
        print(f"  Shortfall         : {CURRENCY_SYMBOL}{(amount - balance):,.2f}")
        print("-" * 45)
        print("  Please try again with an amount within your available balance.")
        return balance

    # Process successful withdrawal
    new_balance = round(balance - amount, 2)

    # Create transaction record dictionary
    record = {
        "type": "Withdrawal",
        "amount": amount,
        "balance_after": new_balance,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    transactions.append(record)

    # User feedback
    print("\n" + "-" * 45)
    print("  ✅ WITHDRAWAL SUCCESSFUL")
    print("-" * 45)
    print(f"  Withdrawn Amount : {CURRENCY_SYMBOL}{amount:,.2f}")
    print(f"  New Balance      : {CURRENCY_SYMBOL}{new_balance:,.2f}")
    print("-" * 45)

    return new_balance


def show_history(transactions):
    """
    Displays the complete transaction history in a clear, formatted table.
    
    Beginner-Friendly Concept: Iterating Lists of Dictionaries & Aggregation
    - If the list is empty, displays a friendly prompt.
    - Loops through each transaction dictionary using `enumerate(..., start=1)`.
    - Formats table columns neatly with width alignment specifiers (e.g., `<20`, `>16`).
    - Calculates and displays summary totals (Total Deposited, Total Withdrawn).

    Parameters:
        transactions (list): List of transaction dictionaries.
    """
    print("\n" + "=" * 75)
    print("                           TRANSACTION HISTORY")
    print("=" * 75)

    # Check if any transactions exist
    if not transactions:
        print("  No transactions recorded yet.")
        print("  Make a deposit or withdrawal to view your transaction records here.")
        print("=" * 75)
        return

    # Table Header
    print(f"  {'#':<4} {'Date & Time':<20} {'Type':<12} {'Amount':>16} {'Balance After':>16}")
    print("  " + "-" * 71)

    total_deposited = 0.0
    total_withdrawn = 0.0
    deposit_count = 0
    withdrawal_count = 0

    # Iterate through transactions
    for idx, txn in enumerate(transactions, start=1):
        txn_type = txn.get("type", "Unknown")
        amount = txn.get("amount", 0.0)
        bal_after = txn.get("balance_after", 0.0)
        timestamp = txn.get("timestamp", "N/A")

        if txn_type == "Deposit":
            amount_str = f"+{CURRENCY_SYMBOL}{amount:,.2f}"
            total_deposited += amount
            deposit_count += 1
        elif txn_type == "Withdrawal":
            amount_str = f"-{CURRENCY_SYMBOL}{amount:,.2f}"
            total_withdrawn += amount
            withdrawal_count += 1
        else:
            amount_str = f"{CURRENCY_SYMBOL}{amount:,.2f}"

        bal_str = f"{CURRENCY_SYMBOL}{bal_after:,.2f}"
        print(f"  {idx:<4} {timestamp:<20} {txn_type:<12} {amount_str:>16} {bal_str:>16}")

    # Summary Statistics
    print("  " + "-" * 71)
    print("  Summary:")
    print(f"  • Total Deposits    : {CURRENCY_SYMBOL}{total_deposited:,.2f} ({deposit_count} deposit{'s' if deposit_count != 1 else ''})")
    print(f"  • Total Withdrawals : {CURRENCY_SYMBOL}{total_withdrawn:,.2f} ({withdrawal_count} withdrawal{'s' if withdrawal_count != 1 else ''})")
    print(f"  • Total Operations  : {len(transactions)} record{'s' if len(transactions) != 1 else ''}")
    print("=" * 75)


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
def main():
    """
    Main driver function that runs the interactive menu loop.
    
    Beginner-Friendly Concept: State Management & Control Flow
    - State (`balance` and `transactions`) is held inside `main()` as local variables.
    - State is passed as arguments into operations, avoiding risky global variables.
    - Runs a `while True` loop to keep presenting the menu until option 5 (Exit) is chosen.
    - Handles KeyboardInterrupt (Ctrl+C) gracefully to prevent messy traceback logs.
    """
    # Local State Management
    balance = 0.0
    transactions = []

    print("\n" + "=" * 52)
    print("        WELCOME TO BANK ACCOUNT SIMULATOR")
    print("=" * 52)
    print("  Manage your account simply, securely, and accurately.")

    try:
        while True:
            # Display interactive menu
            print("\n" + "=" * 32)
            print("         BANKING MENU")
            print("=" * 32)
            print("  1. Check Balance")
            print("  2. Deposit")
            print("  3. Withdraw")
            print("  4. Transaction History")
            print("  5. Exit")
            print("=" * 32)

            choice = input("Enter your choice (1-5): ").strip()

            # Menu navigation using if / elif / else
            if choice == "1":
                check_balance(balance)

            elif choice == "2":
                balance = deposit(balance, transactions)

            elif choice == "3":
                balance = withdraw(balance, transactions)

            elif choice == "4":
                show_history(transactions)

            elif choice == "5":
                print("\n" + "=" * 52)
                print("   Thank you for using Bank Account Simulator!")
                print("               Have a great day! 👋")
                print("=" * 52 + "\n")
                break

            else:
                # Handle invalid menu selections
                print(f"\n❌ Error: '{choice}' is not a valid choice.")
                print("   Please enter a number between 1 and 5.")

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\n\n⚠️  Session interrupted by user. Exiting cleanly. Goodbye!\n")


# Standard Python convention to execute main() only when run directly
if __name__ == "__main__":
    main()
