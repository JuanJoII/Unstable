import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Crear los universos de discurso (rango de valores)
brisa = ctrl.Antecedent(np.arange(0, 11, 1), 'brisa')
hedor = ctrl.Antecedent(np.arange(0, 11, 1), 'hedor')
distancia = ctrl.Antecedent(np.arange(0, 11, 1), 'distancia')

riesgo = ctrl.Consequent(np.arange(0, 11, 1), 'riesgo')

# 2. Definir funciones de membresía (puedes ajustar valores si quieres)
brisa['baja'] = fuzz.trimf(brisa.universe, [0, 0, 5])
brisa['media'] = fuzz.trimf(brisa.universe, [2, 5, 8])
brisa['alta'] = fuzz.trimf(brisa.universe, [5, 10, 10])

hedor['debil'] = fuzz.trimf(hedor.universe, [0, 0, 5])
hedor['medio'] = fuzz.trimf(hedor.universe, [2, 5, 8])
hedor['fuerte'] = fuzz.trimf(hedor.universe, [5, 10, 10])

distancia['cercana'] = fuzz.trimf(distancia.universe, [0, 0, 5])
distancia['media'] = fuzz.trimf(distancia.universe, [2, 5, 8])
distancia['lejana'] = fuzz.trimf(distancia.universe, [5, 10, 10])

riesgo['bajo'] = fuzz.trimf(riesgo.universe, [0, 0, 5])
riesgo['medio'] = fuzz.trimf(riesgo.universe, [2, 5, 8])
riesgo['alto'] = fuzz.trimf(riesgo.universe, [5, 10, 10])

# 3. Definir las reglas difusas
regla1 = ctrl.Rule(brisa['alta'] & hedor['fuerte'], riesgo['alto'])
regla2 = ctrl.Rule(brisa['baja'] & hedor['debil'], riesgo['bajo'])
regla3 = ctrl.Rule(brisa['media'] & distancia['lejana'], riesgo['medio'])
regla4 = ctrl.Rule(hedor['fuerte'] & distancia['cercana'], riesgo['alto'])
regla5 = ctrl.Rule(hedor['medio'] & brisa['media'], riesgo['medio'])

# 4. Crear el sistema de control difuso
sistema_riesgo = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
simulador = ctrl.ControlSystemSimulation(sistema_riesgo)

# 5. Simular un escenario (puedes cambiar los valores)
# Ejemplo: brisa = 7 (alta), hedor = 8 (fuerte), distancia = 2 (cercana)
simulador.input['brisa'] = 7
simulador.input['hedor'] = 8
simulador.input['distancia'] = 2

# 6. Calcular el resultado
simulador.compute()

# 7. Mostrar resultado numérico y gráfico
print(f"Nivel de riesgo difuso: {simulador.output['riesgo']:.2f}")
riesgo.view(sim=simulador)
plt.show()

