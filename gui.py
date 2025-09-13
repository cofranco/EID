import customtkinter as ctk
from analyzer import full_function_analysis, format_sympy_set, evaluate_with_steps
from graphics import plot_function

ctk.set_appearance_mode("Dark") # Modo oscuro para que se vea mejor
ctk.set_default_color_theme("blue")

class FunctionAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analizador de Funciones (MAT1185)")
        self.geometry("800x650")

        # Contenedor principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Entradas ---
        self.label_func = ctk.CTkLabel(main_frame, text="Ingrese la función f(x):", font=("Roboto", 14))
        self.label_func.pack(pady=(10, 5))
        self.entry_func = ctk.CTkEntry(main_frame, width=400, placeholder_text="Ej: (x**2 - 1) / (x - 1)")
        self.entry_func.pack(pady=5)

        self.label_x = ctk.CTkLabel(main_frame, text="Evaluar en x (opcional):", font=("Roboto", 14))
        self.label_x.pack(pady=(10, 5))
        self.entry_x = ctk.CTkEntry(main_frame, width=200, placeholder_text="Ej: 3")
        self.entry_x.pack(pady=5)

        # --- Botones ---
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        self.btn_analizar = ctk.CTkButton(button_frame, text="Analizar Función", command=self.analizar_funcion)
        self.btn_analizar.pack(side="left", padx=10)
        self.btn_graficar = ctk.CTkButton(button_frame, text="Graficar Función", command=self.graficar_funcion, state="disabled")
        self.btn_graficar.pack(side="left", padx=10)

        # --- Caja de resultados ---
        self.result_box = ctk.CTkTextbox(main_frame, width=700, height=300, font=("Courier New", 12))
        self.result_box.pack(pady=10, fill="both", expand=True)

        # Variables de estado
        self.analysis_results = None
        self.eval_point = None

    def analizar_funcion(self):
        func_str = self.entry_func.get()
        self.result_box.delete("1.0", "end")
        
        if not func_str.strip():
            self.result_box.insert("end", "⚠️ Error: Debe ingresar una función.\n")
            self.btn_graficar.configure(state="disabled")
            return

        try:
            # Realizar el análisis completo
            self.analysis_results = full_function_analysis(func_str)
            
            # Formatear resultados para mostrarlos
            domain_str = format_sympy_set(self.analysis_results["domain_set"])
            range_str = format_sympy_set(self.analysis_results["range_set"])
            x_int = self.analysis_results["intersections"]['x']
            y_int = self.analysis_results["intersections"]['y']
            x_int_str = ", ".join([f"({p[0]}, {p[1]})" for p in x_int]) if x_int else "No hay"
            y_int_str = ", ".join([f"({p[0]}, {p[1]})" for p in y_int]) if y_int else "No hay"
            asymptotes_str = ", ".join([f"x = {a}" for a in self.analysis_results["asymptotes"]]) if self.analysis_results["asymptotes"] else "No hay"
            holes_str = ", ".join([f"en ({h[0]}, {h[1]:.2f})" for h in self.analysis_results["holes"]]) if self.analysis_results["holes"] else "No hay"

            # Mostrar resultados principales
            self.result_box.insert("end", "--- ANÁLISIS DE LA FUNCIÓN ---\n")
            self.result_box.insert("end", f"Función Original: f(x) = {self.analysis_results['original_expr']}\n")
            self.result_box.insert("end", f"Función Simplificada: f(x) = {self.analysis_results['simplified_expr']}\n\n")
            self.result_box.insert("end", f" • Dominio: {domain_str}\n")
            self.result_box.insert("end", f" • Recorrido: {range_str}\n")
            self.result_box.insert("end", f" • Intersección Eje X: {x_int_str}\n")
            self.result_box.insert("end", f" • Intersección Eje Y: {y_int_str}\n")
            self.result_box.insert("end", f" • Asíntotas Verticales: {asymptotes_str}\n")
            self.result_box.insert("end", f" • Agujeros (Discontinuidades): {holes_str}\n\n")

            # Mostrar justificación del dominio
            self.result_box.insert("end", "--- JUSTIFICACIÓN DEL DOMINIO ---\n")
            self.result_box.insert("end", self.analysis_results["domain_steps"] + "\n\n")

            # Si hay valor de x para evaluar
            self.eval_point = None
            if self.entry_x.get().strip():
                try:
                    valor = float(self.entry_x.get())
                    result, steps = evaluate_with_steps(self.analysis_results['simplified_expr'], valor)
                    if result is not None:
                        self.eval_point = (valor, float(result))
                        self.result_box.insert("end", f"--- EVALUACIÓN EN x = {valor} ---\n")
                        self.result_box.insert("end", "\n".join(steps) + "\n")
                except ValueError:
                    self.result_box.insert("end", "⚠️ Error: El valor de x para evaluar debe ser un número.\n")
            
            # Habilitar el botón de graficar
            self.btn_graficar.configure(state="normal")

        except Exception as e:
            self.result_box.insert("end", f"❌ Error de análisis: {e}\nVerifique la sintaxis de la función (use '**' para potencias).\n")
            self.btn_graficar.configure(state="disabled")

    def graficar_funcion(self):
        if not self.analysis_results:
            self.result_box.insert("end", "⚠️ Primero debe analizar la función antes de graficar.\n")
            return
        
        # Usamos la expresión simplificada para graficar, ya que es la que se ve
        plot_function(self.analysis_results["simplified_expr"], self.analysis_results, self.eval_point)

