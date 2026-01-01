# utils/id_gen.py
import random, string, config

def gen_id():
    n = config.PASTE_ID_LENGTH
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=n))
