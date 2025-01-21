import frappe

def is_employee(user=None):
    """
    Check if the specified user (or the current user) is an employee.

    Args:
        user (str): The user ID to check. Defaults to the current user.

    Returns:
        bool: True if the user is an employee, False otherwise.
    """
    if not user:
        user = frappe.session.user  # Default to the currently logged-in user
    
    # Check if an employee record exists for the user
    return frappe.db.exists("Employee", {"user_id": user})