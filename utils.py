import random
import string

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits  # abc...XYZ0123...
    return ''.join(random.choice(characters) for _ in range(length))
