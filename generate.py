import secrets

print("SECRET_KEY:", secrets.token_hex(32))  # Generates a 64-character key
print("JWT_SECRET_KEY:", secrets.token_hex(32))