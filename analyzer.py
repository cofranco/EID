# analyzer.py
from sympy import symbols, sympify, Reals, oo, solve, Union, Interval, simplify, cancel, Poly
from sympy.calculus.util import continuous_domain, function_range

# Define el símbolo x
x = symbols("x")

def get_denominator(expr):
    """Extrae el denominador de la expresión. Si no hay, devuelve 1."""
    if expr.is_rational_function():
        # Extrae el numerador y denominador SIN simplificar
        return expr.as_numer_denom()[1]
    return 1

def analyze_domain_with_steps(original_expr):
    """
    Calcula el dominio y genera una explicación paso a paso.
    Devuelve el conjunto del dominio y la cadena de texto con la justificación.
    """
    denominador = get_denominator(original_expr)
    
    if denominador == 1:
        domain_set = Reals
        steps = "La función es un polinomio, por lo que no tiene restricciones.\nEl dominio son todos los números reales."
        return domain_set, steps

    try:
        # Resolver denominador = 0 para encontrar las restricciones
        restricted_points = solve(denominador, x)
        
        # Crear la explicación
        steps = f"1. Para encontrar el dominio, buscamos restricciones en el denominador: {denominador}.\n"
        steps += f"2. Se resuelve la ecuación {denominador} = 0 para encontrar los valores que x no puede tomar.\n"
        
        if not restricted_points:
            steps += "3. El denominador nunca es cero, por lo que no hay restricciones.\nEl dominio son todos los números reales."
            return Reals, steps

        steps += f"3. Las soluciones son: x = {', '.join(map(str, restricted_points))}.\n"
        steps += "4. Por lo tanto, el dominio son todos los números reales excepto estos puntos."

        # Calcular el dominio como un conjunto de SymPy
        domain_set = Reals
        for p in restricted_points:
            domain_set = domain_set - {p}
            
        return domain_set, steps

    except Exception as e:
        return Reals, f"No se pudo calcular el dominio automáticamente. Error: {e}"

def format_sympy_set(sympy_set):
    """Convierte un objeto de SymPy (Interval, Union, etc.) en una cadena legible."""
    if sympy_set is Reals:
        return "Todos los números reales (-∞, ∞)"
    if isinstance(sympy_set, Interval):
        lower = "-∞" if sympy_set.left == -oo else str(sympy_set.left)
        upper = "∞" if sympy_set.right == oo else str(sympy_set.right)
        lower_bracket = "[" if not sympy_set.left_open else "("
        upper_bracket = "]" if not sympy_set.right_open else ")"
        return f"{lower_bracket}{lower}, {upper}{upper_bracket}"
    
    if isinstance(sympy_set, Union):
        parts = [format_sympy_set(s) for s in sympy_set.args]

        # Se crea una pequeña función interna para ordenar correctamente los intervalos
        # que contienen el símbolo de infinito.
        def sort_key(part_str):
            # Extrae el primer número del string, ej: de "(-∞, 1)" extrae "-∞"
            value_str = part_str.split(',')[0][1:] 
            if value_str == '-∞':
                return float('-inf') # Usa el valor de infinito de Python para la comparación
            return float(value_str)

        return " U ".join(sorted(parts, key=sort_key))
    
    return str(sympy_set)


def full_function_analysis(func_str):
    """
    Realiza un análisis completo de la función, incluyendo dominio,
    rango, intersecciones, asíntotas y agujeros.
    """
    original_expr = sympify(func_str)
    simplified_expr = cancel(original_expr) # Simplifica la expresión para encontrar agujeros

    # --- Análisis del Dominio y Justificación ---
    domain_set, domain_steps = analyze_domain_with_steps(original_expr)
    
    # --- Rango (calculado con la expresión simplificada) ---
    try:
        range_set = function_range(simplified_expr, x, Reals)
    except Exception:
        range_set = "No se pudo calcular"

    # --- Intersecciones (calculadas con la expresión simplificada) ---
    intersections = {'x': [], 'y': []}
    try:
        y_int = simplified_expr.subs(x, 0)
        if y_int.is_real: intersections['y'].append((0, float(y_int)))
    except: pass
    try:
        x_roots = solve(simplified_expr, x)
        for root in x_roots:
            if root.is_real: intersections['x'].append((float(root), 0))
    except: pass

    # --- Diferenciar Asíntotas y Agujeros ---
    original_den_roots = set(solve(get_denominator(original_expr), x))
    simplified_den_roots = set(solve(get_denominator(simplified_expr), x))
    
    asymptotes = [r for r in original_den_roots if r in simplified_den_roots]
    hole_xs = [r for r in original_den_roots if r not in simplified_den_roots]
    
    # Calcular la coordenada Y de los agujeros
    holes = []
    for hx in hole_xs:
        try:
            # Límite de la función simplificada cuando x tiende al valor del agujero
            hy = simplified_expr.subs(x, hx)
            holes.append((float(hx), float(hy)))
        except:
            pass
            
    return {
        "original_expr": original_expr,
        "simplified_expr": simplified_expr,
        "domain_set": domain_set,
        "domain_steps": domain_steps,
        "range_set": range_set,
        "intersections": intersections,
        "asymptotes": [float(a) for a in asymptotes],
        "holes": holes,
    }

def evaluate_with_steps(expr, value):
    """Evalúa la función en x=value mostrando pasos"""
    try:
        sustitucion = expr.subs(x, value)
        resultado = sustitucion.evalf()
        steps = [
            f"1. Se sustituye x={value} en f(x): {expr}",
            f"2. f({value}) = {sustitucion}",
            f"3. Resultado aproximado: {resultado:.4f}"
        ]
        return resultado, steps
    except Exception as e:
        return None, [f"Error en la evaluación: {e}"]