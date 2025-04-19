import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Crear los universos de discurso (rango de valores)
riesgo_casilla = ctrl.Antecedent(np.arange(0, 11, 1), 'riesgo_casilla')
distancia_jugador = ctrl.Antecedent(np.arange(0, 11, 1), 'distancia_jugador')
distancia_moneda = ctrl.Antecedent(np.arange(0, 11, 1), 'distancia_moneda')

prioridad = ctrl.Consequent(np.arange(0, 11, 1), 'prioridad')

# 2. Definir funciones de membresía (puedes ajustar valores si quieres)
riesgo_casilla['bajo'] = fuzz.trimf(riesgo_casilla.universe, [0, 0, 5])
riesgo_casilla['medio'] = fuzz.trimf(riesgo_casilla.universe, [2, 5, 8])
riesgo_casilla['alto'] = fuzz.trimf(riesgo_casilla.universe, [5, 10, 10])

distancia_jugador['cercana'] = fuzz.trimf(distancia_jugador.universe, [0, 0, 5])
distancia_jugador['media'] = fuzz.trimf(distancia_jugador.universe, [2, 5, 8])
distancia_jugador['lejana'] = fuzz.trimf(distancia_jugador.universe, [5, 10, 10])

distancia_moneda['cercana'] = fuzz.trimf(distancia_moneda.universe, [0, 0, 5])
distancia_moneda['media'] = fuzz.trimf(distancia_moneda.universe, [2, 5, 8])
distancia_moneda['lejana'] = fuzz.trimf(distancia_moneda.universe, [5, 10, 10])

prioridad['baja'] = fuzz.trimf(prioridad.universe, [0, 0, 5])
prioridad['media'] = fuzz.trimf(prioridad.universe, [2, 5, 8])
prioridad['alta'] = fuzz.trimf(prioridad.universe, [5, 10, 10])

# 3. Definir las reglas difusas
reglas = [
    ctrl.Rule(riesgo_casilla['bajo'] & distancia_moneda['cercana'], prioridad['alta']),
    ctrl.Rule(riesgo_casilla['alto'] & distancia_jugador['cercana'], prioridad['baja']),
    ctrl.Rule(riesgo_casilla['medio'] & distancia_moneda['media'], prioridad['media']),
    ctrl.Rule(distancia_jugador['lejana'] & distancia_moneda['cercana'], prioridad['alta']),
    ctrl.Rule(riesgo_casilla['alto'] & distancia_moneda['lejana'], prioridad['baja']),
]

# 4. Crear el sistema de control difuso
sistema_ctrl = ctrl.ControlSystem(reglas)
simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

# 5. Simular un escenario (puedes cambiar los valores)
# Ejemplo: brisa = 7 (alta), hedor = 8 (fuerte), distancia = 2 (cercana)
simulador.input['riesgo_casilla'] = 7
simulador.input['distancia_moneda'] = 8
simulador.input['distancia_jugador'] = 2

# 5. Función que puedes usar en AI.py
"""
def decidir_prioridad(riesgo_val, dist_jugador_val, dist_moneda_val):
    simulador.input['riesgo_casilla'] = riesgo_val
    simulador.input['dist_jugador'] = dist_jugador_val
    simulador.input['dist_moneda'] = dist_moneda_val
    simulador.compute()
    return simulador.output['prioridad']
    """

# 6. Calcular el resultado
simulador.compute()

# 7. Mostrar resultado numérico y gráfico
print(f"Nivel de riesgo difuso: {simulador.output['prioridad']:.2f}")
prioridad.view(sim=simulador)
plt.show()

