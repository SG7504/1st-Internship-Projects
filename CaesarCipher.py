def caesar_cipher(text, shift, encrypt=True):
    """
    
    Arguments:
        text (str): The text to be encrypted or decrypted.
        shift (int): The number of positions to shift the letters.
        encrypt (bool, optional): If True, encrypts the text. If False, decrypts the text. Defaults to True.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ""
    for char in text:
        if char.isalpha():
            # Shift the character
            if encrypt:
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) - shift - 65) % 26 + 65)
        else:
            result += char
    return result

# Get user input
message = input("Enter the message: ")
shift = int(input("Enter the shift value: "))

# Encrypt the message
encrypted_message = caesar_cipher(message, shift, encrypt=True)
print("Encrypted message:", encrypted_message)

# Decrypt the message
decrypted_message = caesar_cipher(encrypted_message, shift, encrypt=False)
print("Decrypted message:", decrypted_message)