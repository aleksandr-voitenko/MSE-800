from functools import wraps

is_logged_in = False


def login_required(func):
    """Forbids to call a function without logging in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_logged_in:
            print(f"! Access Denied: log in to use {func.__name__}().")
            return None  # Stop here so the protected function never runs.

        return func(*args, **kwargs)

    return wrapper

def log_call(func):
    """Logs function call"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}()")
        return func(*args, **kwargs)
    return wrapper

def login():
    """Simulate login by updating a global variable"""
    global is_logged_in
    is_logged_in = True
    print("[Employee logged in]")


def logout():
    """Clear the employee's login state"""
    global is_logged_in
    is_logged_in = False
    print("[Employee logged out]")


@log_call
@login_required
def view_salary():
    print("> Annual salary: $75,000.")

@log_call
@login_required
def view_personal_details():
    print("> Employee: Alex Smith | Department: IT.")

@log_call
@login_required
def download_report():
    print("> Employee report downloaded.")

@log_call
def view_company_info():
    """Public information is available without logging in"""
    print("> Company: Example Company | Office hours: 9 am to 5 pm.")


def main():
    print("Employee Access Management System")

    print("\n--- Before login ---")
    view_company_info()
    view_salary()
    view_personal_details()
    download_report()

    print("\n--- After login ---")
    login()
    view_salary()
    view_personal_details()
    download_report()

    print("\n--- After logout ---")
    logout()
    view_salary()
    view_personal_details()
    download_report()
    view_company_info()


if __name__ == "__main__":
    main()
