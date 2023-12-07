import re
from terminales import terminals
from gramatica import grammar
import tkinter as tk
from tkinter import ttk
import sys

class PDA:
    def __init__(self, grammar, terminals,  stack_label):
        self.grammar = grammar
        self.terminals = terminals
        self.stack = []
        self.stack_label = stack_label

    def parse(self, input_string):
        self.stack.append("S")  # Símbolo de inicio
        print("Pila:", self.stack)
        index = 0
        while self.stack and index <= len(input_string):
            index = self.skip_whitespace(
                input_string, index
            )  # Saltar espacios en blanco
            if index >= len(input_string):
                break

            top = self.peek()
            remaining_input = input_string[index:]

            if top in self.grammar:
                self.process_non_terminal(top, remaining_input)
            elif self.match_terminal(top, remaining_input):
                match_length = len(
                    re.match(self.terminals[top], remaining_input).group()
                )
                index += match_length
                self.pop()
            else:
                raise Exception(f"Error de sintaxis cerca de la posición {index}")
            print("Pila:", self.stack)
        return len(self.stack) == 0

    def process_non_terminal(self, non_terminal, input_string):
        self.pop()

        if non_terminal == "S":
            self.choose_production_for_S(input_string)
        elif non_terminal == "FU4":
            self.push_production(self.grammar["FU4"][0])
        elif non_terminal == "CN1":
            self.push_production(self.grammar["CN1"][0])
        elif non_terminal == "CN2":
            self.push_production(self.grammar["CN2"][0])
        elif non_terminal == "CN5":
            self.push_production(self.grammar["CN5"][0])
        elif non_terminal == "FU2":
            self.push_production(self.grammar["FU2"][0])
        # elif non_terminal == "FN":
        #     self.push_production(self.grammar["FN"][0])
        elif non_terminal == "CM1":
            self.push_production(self.grammar["CM1"][0])
        elif non_terminal == "CM2":
            self.push_production(self.grammar["CM2"][0])
        elif non_terminal == "CM4":
            self.push_production(self.grammar["CM4"][0])
        elif non_terminal == "MA5":
            self.push_production(self.grammar["MA5"][0])
        elif non_terminal == "MA9":
            self.push_production(self.grammar["MA9"][0])
        else:
            self.choose_production(non_terminal, input_string)

  

    def choose_production_for_S(self, input_string):
        if input_string.startswith("var"):
            self.push_production(self.grammar["S"][0]) 
        elif input_string.startswith("funn"):
            self.push_production(self.grammar["S"][1]) 
        elif input_string.startswith("repite"):
            self.push_production(self.grammar["S"][2]) 
        elif input_string.startswith("si"):
            self.push_production(self.grammar["S"][3]) 
        elif input_string.startswith("Funn"):
            self.push_production(self.grammar["S"][4])
        else:
            raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {input_string}"
        )

    def choose_production(self, non_terminal, input_string):
        for production in self.grammar[non_terminal]:
            if self.is_valid_production(production, input_string):
                self.push_production(production)
                return
        raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {input_string}"
        )

    def is_valid_production(self, production, input_string):
        symbols = production.split()
        if not symbols:
            return False
        first_symbol = symbols[0]
        if first_symbol in self.terminals:
            return re.match(self.terminals[first_symbol], input_string) is not None
        else:
            return False

    def push_production(self, production):
        for symbol in reversed(production.split()):
            self.push(symbol)

    def skip_whitespace(self, input_string, index):
        while index < len(input_string) and input_string[index].isspace():
            index += 1
        return index

    def match_terminal(self, terminal, input_string):
        pattern = self.terminals[terminal]
        return re.match(pattern, input_string)

    def push(self, symbol):
        if symbol != "ε":  # ε cadena vacía
            self.stack.append(symbol)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None

    def update_stack_display(self):
        stack_str = "Pila: " + " ".join(self.stack)
        self.stack_label.config(text=stack_str)

def analizar():
    cadena = cadena_entry.get()
    
    # Redirigir la salida estándar a un widget de texto
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)  # Limpiar el contenido anterior
    original_stdout = sys.stdout
    sys.stdout = TextRedirector(output_text, "stdout")

    # Realizar el análisis
    es_valida = pda.parse(cadena)

    # Mostrar el resultado en el widget de texto
    print("Resultado del análisis:", "Correcta" if es_valida else "Correcta")

    # Restaurar la salida estándar
    sys.stdout = original_stdout
    output_text.config(state=tk.DISABLED)  # Desactivar la edición del widget de texto

    pda.update_stack_display()

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)
# Configurar la raíz de Tkinter
root = tk.Tk()
root.title("Analizador Sintáctico")

# Cambiar el tamaño de la fuente para toda la interfaz
font_style = ttk.Style()
font_style.configure("TLabel", font=("Arial", 14))  # Cambia la fuente de las etiquetas
font_style.configure("TEntry", font=("Arial", 14))  # Cambia la fuente de los campos de entrada
font_style.configure("TButton", font=("Arial", 14))  # Cambia la fuente de los botones

# Ajustar el tamaño de la ventana principal
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Crear instancias de PDA y configurar la interfaz
stack_label = ttk.Label(root, text="Pila: ")
pda = PDA(grammar, terminals, stack_label)

# Configurar widgets
cadena_label = ttk.Label(root, text="Ingrese su cadena:")
cadena_entry = tk.Entry(root, width=50, )  # Ajustar el ancho y la altura según tus preferencias
analizar_button = ttk.Button(root, text="Analizar", command=analizar)

# Nuevo Text widget para mostrar las impresiones
output_text = tk.Text(root, wrap=tk.WORD, height=10, state=tk.DISABLED)
output_text.tag_config("stdout", foreground="black")

# Ubicar widgets en la interfaz
cadena_label.grid(row=0, column=0, padx=20, pady=20)
cadena_entry.grid(row=0, column=1, padx=20, pady=20)
analizar_button.grid(row=1, column=0, columnspan=2, pady=20)
output_text.grid(row=2, column=0, columnspan=2, pady=20)
stack_label.grid(row=3, column=0, columnspan=2, pady=20)

# Actualizar la visualización de la pila después de la configuración inicial
pda.update_stack_display()

# Iniciar el bucle principal
root.mainloop()