#funciones extra de usuarios
import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # ''. este caracter convierte a cadena 
    return ''.join(random.choice(chars) for _ in range(size)) 