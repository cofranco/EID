def validar_funcion(func_str):
    """Valida que la función no esté vacía"""
    if not func_str.strip():
        raise ValueError("La función no puede estar vacía.")
    return True
