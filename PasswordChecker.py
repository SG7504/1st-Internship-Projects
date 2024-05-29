import re

def check_password_strength(password):
    # Length check
    if len(password) < 8:
        return "Weak Password: Password should be at least 8 characters long."
    
    # Character diversity check
    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*()]", password):
        return "Weak Password: Password should include a mix of uppercase and lowercase letters, numbers, and special characters."
    
    # Uniqueness check
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        return "Weak Password: Avoid common passwords like 'password', '123456', 'qwerty', etc."
    
    return "Strong Password: Your password is secure!"

# Get user input for password
password = input("Enter your password: ")

# Check password strength and provide feedback
result = check_password_strength(password)
print(result)