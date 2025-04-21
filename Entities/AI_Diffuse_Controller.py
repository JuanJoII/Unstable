import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
# import matplotlib.pyplot as plt

class FuzzController:
    def __init__(self):
        # 1. Crear los universos de discurso (rango de valores)
        self.riesgo_casilla = ctrl.Antecedent(np.arange(0, 11, 1), 'riesgo_casilla')
        self.distancia_jugador = ctrl.Antecedent(np.arange(0, 11, 1), 'distancia_jugador')
        self.distancia_moneda = ctrl.Antecedent(np.arange(0, 11, 1), 'distancia_moneda')

        self.prioridad = ctrl.Consequent(np.arange(0, 11, 1), 'prioridad')
        
        # 2. Definir funciones de membresía (puedes ajustar valores si quieres)
        self._funciones_membresía()
        
        # 3. Definir las reglas difusas
        self._reglas_difusas()
        
        # 4. Crear el sistema de control difuso
        self.sistema_ctrl = ctrl.ControlSystem(self.reglas)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_ctrl)

    def _funciones_membresía(self):
        # 2. Definir funciones de membresía (puedes ajustar valores si quieres)
        self.riesgo_casilla['bajo'] = fuzz.trimf(self.riesgo_casilla.universe, [0, 0, 5])
        self.riesgo_casilla['medio'] = fuzz.trimf(self.riesgo_casilla.universe, [2, 5, 8])
        self.riesgo_casilla['alto'] = fuzz.trimf(self.riesgo_casilla.universe, [5, 10, 10])

        self.distancia_jugador['cercana'] = fuzz.trimf(self.distancia_jugador.universe, [0, 0, 5])
        self.distancia_jugador['media'] = fuzz.trimf(self.distancia_jugador.universe, [2, 5, 8])
        self.distancia_jugador['lejana'] = fuzz.trimf(self.distancia_jugador.universe, [5, 10, 10])

        self.distancia_moneda['cercana'] = fuzz.trimf(self.distancia_moneda.universe, [0, 0, 5])
        self.distancia_moneda['media'] = fuzz.trimf(self.distancia_moneda.universe, [2, 5, 8])
        self.distancia_moneda['lejana'] = fuzz.trimf(self.distancia_moneda.universe, [5, 10, 10])

        self.prioridad['baja'] = fuzz.trimf(self.prioridad.universe, [0, 0, 5])
        self.prioridad['media'] = fuzz.trimf(self.prioridad.universe, [2, 5, 8])
        self.prioridad['alta'] = fuzz.trimf(self.prioridad.universe, [5, 10, 10])

    def _reglas_difusas(self):
        # 3. Definir las reglas difusas con cobertura completa
        self.reglas = [
            # Reglas originales
            ctrl.Rule(self.riesgo_casilla['bajo'] & self.distancia_moneda['cercana'], self.prioridad['alta']),
            ctrl.Rule(self.riesgo_casilla['alto'] & self.distancia_jugador['cercana'], self.prioridad['baja']),
            ctrl.Rule(self.riesgo_casilla['medio'] & self.distancia_moneda['media'], self.prioridad['media']),
            ctrl.Rule(self.distancia_jugador['lejana'] & self.distancia_moneda['cercana'], self.prioridad['alta']),
            ctrl.Rule(self.riesgo_casilla['alto'] & self.distancia_moneda['lejana'], self.prioridad['baja']),
            
            # Regla por defecto para asegurar cobertura completa
            ctrl.Rule(self.riesgo_casilla['medio'] | 
                    (self.distancia_jugador['media'] & self.distancia_moneda['media']), 
                    self.prioridad['media'])
        ]

    def calcular_prioridad(self, riesgo_val, distancia_jugador, distancia_moneda):
        self.simulador.input['riesgo_casilla'] = riesgo_val
        self.simulador.input['distancia_jugador'] = distancia_jugador
        self.simulador.input['distancia_moneda'] = distancia_moneda
        
        try:
            self.simulador.compute()
            prioridad_valor = self.simulador.output['prioridad']
            print(f"Nivel de prioridad difuso: {prioridad_valor:.2f}")
            return prioridad_valor
        except KeyError:
            print("Advertencia: No se activó ninguna regla lo suficiente. Retornando valor por defecto (5)")
            return 5.0  # valor por defecto intermedio

if __name__ == "__main__":
    controlador = FuzzController()
    
    controlador.calcular_prioridad(riesgo_val=8, distancia_jugador=8, distancia_moneda=8)



# sistema_ctrl = ctrl.ControlSystem(reglas)
# simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

# # 5. Simular un escenario (puedes cambiar los valores)
# # Ejemplo: brisa = 7 (alta), hedor = 8 (fuerte), distancia = 2 (cercana)
# simulador.input['riesgo_casilla'] = 7
# simulador.input['distancia_moneda'] = 8
# simulador.input['distancia_jugador'] = 2

# # 5. Función que puedes usar en AI.py
# """
# def decidir_prioridad(riesgo_val, dist_jugador_val, dist_moneda_val):
#     simulador.input['riesgo_casilla'] = riesgo_val
#     simulador.input['dist_jugador'] = dist_jugador_val
#     simulador.input['dist_moneda'] = dist_moneda_val
#     simulador.compute()
#     return simulador.output['prioridad']
#     """

# # 6. Calcular el resultado
# simulador.compute()

# # 7. Mostrar resultado numérico y gráfico
# print(f"Nivel de riesgo difuso: {simulador.output['prioridad']:.2f}")
# prioridad.view(sim=simulador)
# plt.show()
