import json
import os
import pygame
from constantes import SCREEN_SIZE

def save_score(score, main_screen):
    # Configuración compacta con fondo
    input_screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Guardar Puntaje")
    
    # Fuentes ajustadas
    title_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 20)
    input_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 18)
    help_font = pygame.font.Font("Assets/UI/PressStart2P.ttf", 12)
    
    # Colores
    BACKGROUND_COLOR = (0, 28, 42)
    TEXT_COLOR = (255, 255, 255)
    ACCENT_COLOR = (0, 255, 255)
    INPUT_BOX_COLOR = (50, 50, 80, 200)  # Con transparencia
    
    # Cargar fondo
    try:
        background = pygame.image.load("Assets/UI/Unstable_Cover.jpg").convert()
        background = pygame.transform.scale(background, (SCREEN_SIZE, SCREEN_SIZE))
    except:
        background = None
    
    input_text = ""
    active = True
    clock = pygame.time.Clock()
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 12 and (event.unicode.isalnum() or event.unicode == ' '):
                        input_text += event.unicode
        
        # Dibujar fondo con overlay oscuro
        if background:
            input_screen.blit(background, (0, 0))
            overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Overlay más oscuro para mejor contraste
            input_screen.blit(overlay, (0, 0))
        else:
            input_screen.fill(BACKGROUND_COLOR)
        
        # Panel central compacto
        panel_rect = pygame.Rect(SCREEN_SIZE//2 - 180, SCREEN_SIZE//2 - 120, 360, 200)
        pygame.draw.rect(input_screen, (0, 28, 42, 220), panel_rect, border_radius=10)
        pygame.draw.rect(input_screen, ACCENT_COLOR, panel_rect, 2, border_radius=10)
        
        # Título compacto
        title_text = title_font.render("GUARDAR", True, ACCENT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 30))
        input_screen.blit(title_text, title_rect)
        
        # Puntuación
        score_text = input_font.render(f"Puntos: {score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 70))
        input_screen.blit(score_text, score_rect)
        
        # Input compacto
        input_box = pygame.Rect(SCREEN_SIZE//2 - 120, panel_rect.y + 100, 240, 30)
        pygame.draw.rect(input_screen, INPUT_BOX_COLOR, input_box, border_radius=5)
        pygame.draw.rect(input_screen, ACCENT_COLOR, input_box, 2, border_radius=5)
        
        # Texto del input
        input_surface = input_font.render(input_text, True, TEXT_COLOR)
        input_screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))
        
        # Cursor parpadeante
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_pos = input_font.size(input_text)[0] + 12
            pygame.draw.line(input_screen, TEXT_COLOR, 
                          (input_box.x + cursor_pos, input_box.y + 5),
                          (input_box.x + cursor_pos, input_box.y + 25), 2)
        
        # Instrucción pequeña
        help_text = help_font.render("ENTER para guardar", True, ACCENT_COLOR)
        help_rect = help_text.get_rect(center=(SCREEN_SIZE//2, panel_rect.y + 160))
        input_screen.blit(help_text, help_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    # Restaurar pantalla principal
    pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    
    if not input_text.strip():
        input_text = "Anónimo"
    
    # Guardar puntaje
    nombre_jugador = input_text.strip()
    datos = {"nombre": nombre_jugador, "puntaje": score}
    
    if not os.path.exists('Saves'):
        os.makedirs('Saves')
    
    try:
        archivo = 'Saves/puntajes.json'
        puntajes = []
        
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                puntajes = json.load(f)
        
        # Actualizar puntajes
        existe = False
        for i, p in enumerate(puntajes):
            if p['nombre'].lower() == nombre_jugador.lower():
                if score > p['puntaje']:
                    puntajes[i] = datos
                existe = True
                break
        
        if not existe:
            puntajes.append(datos)
        
        puntajes.sort(key=lambda x: x['puntaje'], reverse=True)
        
        with open(archivo, 'w') as f:
            json.dump(puntajes[:10], f, indent=4)
            
        return True 
    
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False