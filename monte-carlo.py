import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import tkinter as tk
from matplotlib.animation import FuncAnimation

def integral(x):
    return (5 * x + 3) ** x

def metodo_monte_carlo(a, b, num_simulaciones):
    x_random = np.random.uniform(a, b, num_simulaciones)
    y_random = integral(x_random)
    aproximacion_integral = (b - a) * np.mean(y_random)
    return aproximacion_integral

def calcular():
    try:
        num_simulaciones = int(entry.get())
        if num_simulaciones <= 0:
            raise ValueError

        resultado_matematico, _ = quad(integral, 4, 6)

        root.destroy()

        graficar(4, 6, num_simulaciones, resultado_matematico)

    except ValueError:
        error_label.config(text="Ingrese un número válido")

def enter(event):
    calcular()

def graficar(a, b, num_simulaciones, resultado_matematico):
    fig, ax = plt.subplots(figsize=(6, 4))

    x_puntos = np.linspace(a, b, 100)
    y_puntos = integral(x_puntos)

    ax.plot(x_puntos, y_puntos, label=r'$f(x) = (5x + 3)^x$', color='blue')

    x_random = np.random.uniform(a, b, num_simulaciones)
    y_random = integral(x_random)

    contador_frames = [0]

    def actualizar(frame):
        if contador_frames[0] < num_simulaciones:
            ax.clear()

            ax.plot(x_puntos, y_puntos, label=r'$f(x) = (5x + 3)^x$', color='blue')
            ax.scatter(x_random[:contador_frames[0] + 1], y_random[:contador_frames[0] + 1], color='red', s=10, alpha=0.5)
            ax.fill_between(x_puntos, 0, y_puntos, where=[(a <= x <= b) for x in x_puntos], color='lightblue', alpha=0.5)

            resultado_aproximado = (b - a) * np.mean(y_random[:contador_frames[0] + 1])
            porcentaje_error = abs((resultado_matematico - resultado_aproximado) / resultado_matematico) * 100

            ax.text(4.1, max(y_puntos)*0.8,
                    f"Resultado matemático: {resultado_matematico:.6f}\n"
                    f"Resultado aproximado: {resultado_aproximado:.6f}\n"
                    f"Porcentaje de error: {porcentaje_error:.2f}%\n"
                    f"Simulaciones completadas: {contador_frames[0] + 1}/{num_simulaciones}",
                    fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
            ax.legend()
            ax.grid()

            contador_frames[0] += 1

    ani = FuncAnimation(fig, actualizar, frames=num_simulaciones, repeat=False, interval=100)
    plt.show()

root = tk.Tk()
root.title("Método de Monte Carlo")
root.geometry("300x150")
root.resizable(width=False, height=False)

frame_top = tk.Frame(root)
frame_top.pack(side='top', expand=True, fill='both')

frame_center = tk.Frame(root)
frame_center.pack(side='top')

label = tk.Label(frame_center, text="Ingrese el número de simulaciones:")
label.pack(pady=(0, 5))

entry = tk.Entry(frame_center)
entry.pack(pady=(0, 10))

button = tk.Button(frame_center, text="Calcular", command=calcular)
button.pack()

error_label = tk.Label(frame_center, text="", fg="red")
error_label.pack(pady=(5, 0))

entry.bind('<Return>', enter)

frame_bottom = tk.Frame(root)
frame_bottom.pack(side='top', expand=True, fill='both')

root.mainloop()