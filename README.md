## Simple ATM Controller Implementation

### Installation and Setup Instructions

#### Prerequisites
- Python 3.9 or higher must be installed.

---

## Installing Python 3.9 (Mac)

### 1. Install `pyenv` and `pyenv-virtualenv` using Homebrew

`pyenv` helps manage multiple versions of Python easily, and `pyenv-virtualenv` is a tool for managing Python virtual environments. You can install both with Homebrew.

```bash
brew install pyenv pyenv-virtualenv
```

### 2. Initialize `pyenv` and `pyenv-virtualenv`

After installation, add the following lines to your terminal configuration file (e.g., `.bashrc`, `.zshrc`) to enable `pyenv` and `pyenv-virtualenv`.

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

After editing the file, reload the terminal settings:

```bash
source ~/.zshrc  # You can replace with .bashrc or .bash_profile depending on your shell
```

### 3. Install Python 3.9

Use `pyenv` to install Python 3.9.

```bash
pyenv install 3.9
```

You can verify the installed Python versions:

```bash
pyenv versions
```

### 4. Activate Python 3.9

#### Set Globally (applies to all projects)

To set Python 3.9 globally:

```bash
pyenv global 3.9
```

#### Set Locally (applies to a specific project)

To use Python 3.9 only in a specific project directory, run:

```bash
pyenv local 3.9
```

### 5. Create a Virtual Environment

Use `pyenv-virtualenv` to create a Python 3.9-based virtual environment.

```bash
pyenv virtualenv 3.9 myenv3.9
```

### 6. Activate and Deactivate the Virtual Environment

#### Activate the virtual environment:

```bash
pyenv activate myenv3.9
```

#### Deactivate the virtual environment:

```bash
pyenv deactivate
```

---

## Cloning and Running the Project

```bash
git clone https://github.com/jmp7786/atm-controller.git
cd atm-controller
```

Run the test cases using `unittest`:

```bash
python -m unittest tests/test_atm_controller.py
```

---

## Explanation of the Test Code

The `tests/test_atm_controller.py` file contains various test cases to validate the functionality of the ATM controller and handle edge cases.

### Key Test Cases

1. **Full ATM Flow Test (`test_full_atm_flow`)**
   - Tests the complete flow, from inserting the card, entering the PIN, selecting the account, checking the balance, depositing, withdrawing, to ejecting the card.

2. **Invalid PIN Entry Test (`test_invalid_pin`)**
   - Verifies proper handling of invalid PIN entry.

3. **Insufficient Funds Test (`test_insufficient_funds`)**
   - Tests the system's response when attempting to withdraw more than the account balance.

4. **Cash Bin Limit Test (`test_cash_bin_limits`)**
   - Ensures the system rejects withdrawal attempts when the requested amount exceeds the available cash in the ATM.

5. **Concurrent Session Test (`test_concurrent_sessions`)**
   - Verifies that two separate cards can operate independently in concurrent sessions.

6. **Negative Amount Operation Test (`test_negative_amount_operations`)**
   - Ensures the system rejects deposits or withdrawals with negative amounts.

7. **Invalid Account Selection Test (`test_select_invalid_account`)**
   - Tests rejection of attempts to select an account that does not exist.

8. **Operation Without Authentication Test (`test_operations_without_authentication`)**
   - Verifies the system prevents operations without successful authentication.

9. **Invalid Card Number Test (`test_invalid_card_number`)**
   - Checks the proper handling of attempts to operate with an invalid card number.

10. **Withdraw Exact Balance Test (`test_withdraw_exact_balance`)**
    - Verifies successful withdrawal when the requested amount matches the account balance.

11. **Withdraw Exact Cash Bin Amount Test (`test_withdraw_exact_cash_bin_amount`)**
    - Ensures successful withdrawal when the requested amount matches the remaining cash in the ATM.

12. **Withdrawal with Zero Balance Test (`test_withdraw_when_balance_zero`)**
    - Verifies the system rejects withdrawal attempts when the account balance is zero.

13. **Minimum Withdrawal Amount Test (`test_withdraw_minimum_amount`)**
    - Ensures successful withdrawal of the minimum allowed amount.

14. **Select Account Without PIN Test (`test_select_account_without_pin`)**
    - Tests rejection of attempts to select an account without PIN authentication.

15. **Withdraw With No Cash in Bin Test (`test_withdraw_with_no_cash_in_bin`)**
    - Verifies the system prevents withdrawal when the ATM has no cash available.