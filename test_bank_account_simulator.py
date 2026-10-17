"""
================================================================================
Test Suite  : Bank Account Simulator Unit Tests
Description : Comprehensive unit tests verifying balance inquiries, deposits,
              withdrawals, validation rules, transaction logs, and menu flow.
Framework   : Python standard library unittest (no external packages required)
================================================================================
"""

import io
import sys
import unittest
from unittest.mock import patch

# Import functions under test from bank_account_simulator
from bank_account_simulator import (
    CURRENCY_SYMBOL,
    check_balance,
    deposit,
    withdraw,
    show_history,
    prompt_positive_float,
    main,
)


class TestBankAccountSimulator(unittest.TestCase):
    """Test cases for each banking operation and validation rule."""

    def setUp(self):
        """Set up a fresh initial state before each test and suppress console noise."""
        self.initial_balance = 0.0
        self.transactions = []
        # Suppress printed messages during automated tests
        self.suppress_output = patch("sys.stdout", new_callable=io.StringIO)
        self.mock_stdout = self.suppress_output.start()

    def tearDown(self):
        """Clean up patches after each test."""
        self.suppress_output.stop()

    # --------------------------------------------------------------------------
    # 1. BALANCE CHECK TESTS
    # --------------------------------------------------------------------------
    def test_check_balance_displays_formatted_amount(self):
        """Verify check_balance prints the correct formatted amount."""
        captured_output = io.StringIO()
        with patch("sys.stdout", new=captured_output):
            check_balance(1250.50)

        output = captured_output.getvalue()
        self.assertIn("ACCOUNT BALANCE", output)
        self.assertIn(f"{CURRENCY_SYMBOL}1,250.50", output)

    # --------------------------------------------------------------------------
    # 2. DEPOSIT TESTS
    # --------------------------------------------------------------------------
    def test_deposit_valid_amount(self):
        """Verify depositing a positive amount updates balance and records transaction."""
        new_balance = deposit(self.initial_balance, self.transactions, amount=500.0)

        self.assertEqual(new_balance, 500.0)
        self.assertEqual(len(self.transactions), 1)

        txn = self.transactions[0]
        self.assertEqual(txn["type"], "Deposit")
        self.assertEqual(txn["amount"], 500.0)
        self.assertEqual(txn["balance_after"], 500.0)
        self.assertIn("timestamp", txn)

    def test_deposit_multiple_times(self):
        """Verify successive deposits accumulate correctly."""
        balance = deposit(0.0, self.transactions, amount=100.25)
        balance = deposit(balance, self.transactions, amount=200.50)
        balance = deposit(balance, self.transactions, amount=50.25)

        self.assertEqual(balance, 351.00)
        self.assertEqual(len(self.transactions), 3)
        self.assertEqual(self.transactions[-1]["balance_after"], 351.00)

    def test_deposit_zero_or_negative_rejected(self):
        """Verify zero or negative deposit amounts are rejected without state change."""
        balance_zero = deposit(100.0, self.transactions, amount=0.0)
        self.assertEqual(balance_zero, 100.0)
        self.assertEqual(len(self.transactions), 0)

        balance_neg = deposit(100.0, self.transactions, amount=-50.0)
        self.assertEqual(balance_neg, 100.0)
        self.assertEqual(len(self.transactions), 0)

    # --------------------------------------------------------------------------
    # 3. WITHDRAWAL TESTS
    # --------------------------------------------------------------------------
    def test_withdraw_valid_amount(self):
        """Verify withdrawing a valid amount decreases balance and records transaction."""
        balance = 1000.0
        new_balance = withdraw(balance, self.transactions, amount=350.0)

        self.assertEqual(new_balance, 650.0)
        self.assertEqual(len(self.transactions), 1)

        txn = self.transactions[0]
        self.assertEqual(txn["type"], "Withdrawal")
        self.assertEqual(txn["amount"], 350.0)
        self.assertEqual(txn["balance_after"], 650.0)

    def test_withdraw_exact_balance(self):
        """Verify withdrawing the exact balance results in zero without error."""
        balance = 250.0
        new_balance = withdraw(balance, self.transactions, amount=250.0)

        self.assertEqual(new_balance, 0.0)
        self.assertEqual(len(self.transactions), 1)
        self.assertEqual(self.transactions[0]["balance_after"], 0.0)

    def test_withdraw_insufficient_funds(self):
        """Verify withdrawal fails when requested amount exceeds current balance."""
        balance = 200.0
        new_balance = withdraw(balance, self.transactions, amount=500.0)

        # Balance remains unchanged and no transaction is recorded
        self.assertEqual(new_balance, 200.0)
        self.assertEqual(len(self.transactions), 0)

    def test_withdraw_zero_or_negative_rejected(self):
        """Verify zero or negative withdrawal amounts are rejected."""
        balance = 300.0
        new_balance = withdraw(balance, self.transactions, amount=-100.0)
        self.assertEqual(new_balance, 300.0)
        self.assertEqual(len(self.transactions), 0)

    # --------------------------------------------------------------------------
    # 4. TRANSACTION HISTORY TESTS
    # --------------------------------------------------------------------------
    def test_show_history_empty(self):
        """Verify empty transaction history outputs friendly guidance."""
        captured_output = io.StringIO()
        with patch("sys.stdout", new=captured_output):
            show_history([])

        output = captured_output.getvalue()
        self.assertIn("No transactions recorded yet", output)

    def test_show_history_with_records(self):
        """Verify transaction history formats table and calculates summary statistics."""
        balance = 0.0
        balance = deposit(balance, self.transactions, amount=1000.0)
        balance = withdraw(balance, self.transactions, amount=200.0)

        captured_output = io.StringIO()
        with patch("sys.stdout", new=captured_output):
            show_history(self.transactions)

        output = captured_output.getvalue()
        self.assertIn("TRANSACTION HISTORY", output)
        self.assertIn("Deposit", output)
        self.assertIn("Withdrawal", output)
        self.assertIn(f"Total Deposits    : {CURRENCY_SYMBOL}1,000.00", output)
        self.assertIn(f"Total Withdrawals : {CURRENCY_SYMBOL}200.00", output)
        self.assertIn("Total Operations  : 2 records", output)

    # --------------------------------------------------------------------------
    # 5. INPUT VALIDATION TESTS (MOCKED)
    # --------------------------------------------------------------------------
    @patch("builtins.input", side_effect=["", "abc", "-50", "125.50"])
    def test_prompt_positive_float_recovers_from_invalid_inputs(self, mock_input):
        """Verify prompt_positive_float rejects empty, alphabetic, negative input, then accepts valid float."""
        captured_output = io.StringIO()
        with patch("sys.stdout", new=captured_output):
            result = prompt_positive_float("Enter amount: ")

        self.assertEqual(result, 125.50)
        output = captured_output.getvalue()
        self.assertIn("Input cannot be empty", output)
        self.assertIn("is not a valid number", output)
        self.assertIn("Negative amounts are not allowed", output)

    # --------------------------------------------------------------------------
    # 6. FULL INTERACTIVE MENU FLOW TEST (MOCKED)
    # --------------------------------------------------------------------------
    @patch(
        "builtins.input",
        side_effect=[
            "1",           # Check Balance (0.0)
            "2", "500",    # Deposit 500
            "3", "150",    # Withdraw 150
            "4",           # Transaction History
            "99",          # Invalid Menu Option
            "5",           # Exit
        ],
    )
    def test_main_menu_full_flow(self, mock_input):
        """Simulate a complete end-to-end interactive user session."""
        captured_output = io.StringIO()
        with patch("sys.stdout", new=captured_output):
            main()

        output = captured_output.getvalue()
        self.assertIn("WELCOME TO BANK ACCOUNT SIMULATOR", output)
        self.assertIn("Available Balance :", output)
        self.assertIn("DEPOSIT SUCCESSFUL", output)
        self.assertIn("WITHDRAWAL SUCCESSFUL", output)
        self.assertIn("TRANSACTION HISTORY", output)
        self.assertIn("'99' is not a valid choice", output)
        self.assertIn("Thank you for using Bank Account Simulator", output)


if __name__ == "__main__":
    unittest.main()
