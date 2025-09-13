# graphics.py
import matplotlib.pyplot as plt
from sympy import lambdify, symbols, Reals
from sympy.calculus.util import continuous_domain

x = symbols("x")

def plot_function(expr, analysis_results, eval_point=None):
    """Genera una gráfica clara con intersecciones, asíntotas, agujeros y puntos evaluados."""
    
    intersections = analysis_results["intersections"]
    holes = analysis_results["holes"]
    
    # Usamos 'math' en lugar de 'numpy'
    f = lambdify(x, expr, "math")

    # Creamos los puntos para X usando Python estándar
    X_vals = [i / 40.0 for i in range(-400, 401)] # Rango de -10 a 10 con 801 puntos
    Y_vals = []
    
    domain = continuous_domain(expr, x, Reals)
    
    # Calculamos Y para cada X, manejando las discontinuidades (asíntotas)
    for val in X_vals:
        if val in domain:
            try:
                Y_vals.append(f(val))
            except (ValueError, ZeroDivisionError):
                Y_vals.append(None) # Para cortar la línea en el gráfico
        else:
            Y_vals.append(None)

    plt.figure(figsize=(10, 8))
    plt.axhline(0, color="black", linewidth=0.75)
    plt.axvline(0, color="black", linewidth=0.75)
    
    plt.plot(X_vals, Y_vals, label=f"f(x) = {analysis_results['original_expr']}", color="blue")

    # --- Graficar Puntos Relevantes ---

    # Intersecciones con eje X (puntos rojos)
    x_int_pts = intersections.get('x', [])
    if x_int_pts:
        plt.scatter([p[0] for p in x_int_pts], [p[1] for p in x_int_pts], color="red", zorder=5, label="Intersección Eje X")

    # Intersección con eje Y (punto verde)
    y_int_pts = intersections.get('y', [])
    if y_int_pts:
        plt.scatter([p[0] for p in y_int_pts], [p[1] for p in y_int_pts], color="green", zorder=5, label="Intersección Eje Y")

    # Agujeros (círculos blancos con borde azul)
    if holes:
        plt.scatter(
            [h[0] for h in holes], [h[1] for h in holes], 
            facecolors='white', edgecolors='blue', s=80, zorder=5, 
            label="Agujero (Discontinuidad)"
        )

    # Punto evaluado (punto morado)
    if eval_point:
        plt.scatter(eval_point[0], eval_point[1], color="purple", s=100, zorder=5, label=f"Punto ({eval_point[0]}, {eval_point[1]:.2f})")

    # Configuración final del gráfico
    plt.title("Gráfica de la Función", fontsize=16)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("f(x)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    
    # Limitar el eje Y para que las asíntotas no arruinen la vista
    plt.ylim(-20, 20)
    
    plt.show()
