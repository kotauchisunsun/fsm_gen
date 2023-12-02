from random import randint

def get_random_name(prefix):
    sig = "".join(str(randint(0,9)) for i in range(10))
    return f"{prefix}_{sig}"