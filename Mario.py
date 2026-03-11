# importacion de librerias
import pygame
import sys
import random

# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
class Constants: #clase para agrupar constantes del juego
    SCREEN_W = 800 # ancho de la ventana
    SCREEN_H = 600 # alto de la ventana
    FPS = 60 # frames por segundo para control de tiempo
    GRAVITY = 0.5 # Gravedad aplicada al jugador cada frame
    JUMP_FORCE = -13 # Fuerza de salto
    MOVE_SPEED = 4 # Velocidad de movimiento
    TILE = 30  # tamaño de cada bloque

    # Colores
    SKY_BLUE = (107, 196, 255)
    GROUND_COL = (139, 90, 43)
    BRICK_COL = (200, 100, 40)
    BRICK_DARK = (160, 70, 20)
    COIN_GOLD = (255, 215, 0)
    COIN_DARK = (200, 150, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 50, 50)
    GREEN = (40, 180, 40)
    DARK_RED = (160, 20, 20)
    DARK_GREEN = (20, 120, 20)
    SKIN = (255, 200, 150)
    BLUE = (50, 100, 220)
    BROWN = (120, 70, 30)
    YELLOW = (255, 240, 0)
    GRAY = (180, 180, 180)
    DARK_GRAY = (100, 100, 100)

# Usar constantes desde la clase
SCREEN_W, SCREEN_H = Constants.SCREEN_W, Constants.SCREEN_H
FPS = Constants.FPS
GRAVITY = Constants.GRAVITY
JUMP_FORCE = Constants.JUMP_FORCE
MOVE_SPEED = Constants.MOVE_SPEED
TILE = Constants.TILE

# Colores
SKY_BLUE = Constants.SKY_BLUE
GROUND_COL = Constants.GROUND_COL
BRICK_COL = Constants.BRICK_COL
BRICK_DARK = Constants.BRICK_DARK
COIN_GOLD = Constants.COIN_GOLD
COIN_DARK = Constants.COIN_DARK
WHITE = Constants.WHITE
BLACK = Constants.BLACK
RED = Constants.RED
GREEN = Constants.GREEN
DARK_RED = Constants.DARK_RED
DARK_GREEN = Constants.DARK_GREEN
SKIN = Constants.SKIN
BLUE = Constants.BLUE
BROWN = Constants.BROWN
YELLOW = Constants.YELLOW
GRAY = Constants.GRAY
DARK_GRAY = Constants.DARK_GRAY

# ─────────────────────────────────────────────
#  FUNCIONES DE DIBUJO DE SPRITES (pixel art)
# ─────────────────────────────────────────────

def draw_mario(surface, x, y, facing_right=True, hat_color=RED, clothes_color=RED, pants_color=BLUE):# Dibuja un sprite de Mario o Luigi en la posición (x, y) con colores personalizados.

    ox, oy = int(x), int(y)  # Convertir a enteros para evitar errores de dibujo

    # Dibujar sombrero: ala inferior, copa superior, borde negro
    pygame.draw.rect(surface, hat_color,  (ox+6,  oy,    20, 6))   # Ala del sombrero
    pygame.draw.rect(surface, hat_color,  (ox+8,  oy-8,  16, 8))   # Copa del sombrero
    pygame.draw.rect(surface, BLACK,      (ox+10, oy-9,  12, 2))   # Borde negro en la copa

    # Dibujar cara: piel, bigote
    pygame.draw.rect(surface, SKIN,       (ox+6,  oy+6,  20, 14))  # Área de la cara
    pygame.draw.rect(surface, BROWN,      (ox+8,  oy+14, 16, 4))   # Bigote marrón

    # Dibujar ojos según dirección: cuadrado negro en posición correspondiente
    if facing_right:
        pygame.draw.rect(surface, BLACK,  (ox+18, oy+8,  4, 4))  # Ojo derecho
    else:
        pygame.draw.rect(surface, BLACK,  (ox+10, oy+8,  4, 4))  # Ojo izquierdo

    # Dibujar cuerpo: overol, tirantes, botones
    pygame.draw.rect(surface, clothes_color, (ox+4,  oy+20, 24, 14))  # Overol principal
    pygame.draw.rect(surface, pants_color,   (ox+6,  oy+20, 6, 14))   # Tirante izquierdo
    pygame.draw.rect(surface, pants_color,   (ox+20, oy+20, 6, 14))   # Tirante derecho
    pygame.draw.rect(surface, YELLOW,    (ox+8,  oy+24, 4, 4))        # Botón izquierdo
    pygame.draw.rect(surface, YELLOW,    (ox+20, oy+24, 4, 4))        # Botón derecho

    # Dibujar pantalón: dos rectángulos para piernas
    pygame.draw.rect(surface, pants_color, (ox+4,  oy+34, 10, 10))    # Pierna izquierda
    pygame.draw.rect(surface, pants_color, (ox+18, oy+34, 10, 10))    # Pierna derecha

    # Dibujar zapatos: rectángulos negros en la base
    pygame.draw.rect(surface, BLACK,      (ox+2,  oy+44, 12, 6))      # Zapato izquierdo
    pygame.draw.rect(surface, BLACK,      (ox+18, oy+44, 12, 6))      # Zapato derecho


def draw_brick(surface, rect, broken=False):# Dibuja un ladrillo en la posición (x, y) con colores personalizados.
      
    if broken:
        return  # No dibujar si el ladrillo está roto
    x, y, w, h = rect  # Desempaquetar coordenadas
    pygame.draw.rect(surface, BRICK_COL,  rect)  # Rectángulo principal en color ladrillo
    pygame.draw.rect(surface, BRICK_DARK, rect, 2)  # Borde oscuro de 2 píxeles
    # Líneas horizontales de mortero en el centro
    pygame.draw.line(surface, BRICK_DARK, (x, y+h//2), (x+w, y+h//2), 2)
    # Líneas verticales intercaladas para patrón de ladrillo
    pygame.draw.line(surface, BRICK_DARK, (x+w//2, y), (x+w//2, y+h//2), 2)
    pygame.draw.line(surface, BRICK_DARK, (x+w//4, y+h//2), (x+w//4, y+h), 2)
    pygame.draw.line(surface, BRICK_DARK, (x+3*w//4, y+h//2), (x+3*w//4, y+h), 2)


def draw_coin(surface, cx, cy, r=10, anim=0):# Moneda animada (aplana/ensancha)
    width = max(3, int(r * 2 * (0.4 + 0.6 * abs(anim)))) # Efecto de giro de delgada a ancha
    pygame.draw.ellipse(surface, COIN_GOLD, (cx - width//2, cy - r, width, r*2))
    pygame.draw.ellipse(surface, COIN_DARK, (cx - width//2, cy - r, width, r*2), 2)
    if width > 6:
        pygame.draw.line(surface, COIN_DARK, (cx, cy - r + 3), (cx, cy + r - 3), 2)


def draw_ground_tile(surface, rect):
    x, y, w, h = rect
    pygame.draw.rect(surface, GROUND_COL, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    # césped encima
    pygame.draw.rect(surface, (80, 180, 60), (x, y, w, 8))


def draw_background(surface):# Dibuja el fondo del juego con cielo y nubes decorativas
    surface.fill(SKY_BLUE)
    # nubes decorativas
    for cx, cy in [(100, 80), (300, 50), (550, 90), (700, 60)]:
        pygame.draw.ellipse(surface, WHITE, (cx-30, cy-15, 60, 30))
        pygame.draw.ellipse(surface, WHITE, (cx-15, cy-25, 50, 30))
        pygame.draw.ellipse(surface, WHITE, (cx+5,  cy-15, 40, 25))


# ─────────────────────────────────────────────
#  CLASES DEL JUEGO
# ─────────────────────────────────────────────

class Coin(pygame.sprite.Sprite):# monedas recolectables
    
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)  # Posición y tamaño de la moneda
        self.anim = 0.0  # Valor inicial de animación
        self.anim_dir = 1  # Dirección de animación (incrementa)
        self.collected = False  # Indica si la moneda ha sido recolectada

    def update(self): # Actualiza la animación de la moneda
        
        self.anim += 0.05 * self.anim_dir  # Avanza animación
        if self.anim >= 1.0:  # Límite superior
            self.anim_dir = -1  # Invertir dirección
        if self.anim <= -1.0:  # Límite inferior
            self.anim_dir = 1  # Invertir dirección

    def draw(self, surface): # Dibuja la moneda si no ha sido recolectada, con animación de giro
        
        if not self.collected:
            draw_coin(surface, self.rect.centerx, self.rect.centery,
                      r=10, anim=self.anim)


class Brick(pygame.sprite.Sprite):# Dibuja ladrillos que pueden ser rotos
   
    def __init__(self, x, y, w=TILE, h=TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # Rectángulo de colisión
        self.broken = False  # Estado de ruptura
        self.shake = 0  # Frames restantes de animación
        self.oy = y  # Posición Y original

    def hit(self):# Logica si el ladrillo esta o no roto
       
        if not self.broken:
            self.broken = True  # Marcar como roto
            self.shake = 8  # Iniciar animación de 8 frames

    def update(self):# Efecto de ruptura del ladrillo
     
        if self.shake > 0:
            self.rect.y = self.oy - (self.shake % 2) * 4  # Sacudida: alterna
            self.shake -= 1  # Reducir contador
        else:
            self.rect.y = self.oy  # Restaurar posición original

    def draw(self, surface):#    Dibuja el ladrillo si no está roto.
        
        if not self.broken:
            draw_brick(surface, (self.rect.x, self.rect.y,
                                 self.rect.w, self.rect.h))


class GroundTile(pygame.sprite.Sprite):# Dibujo del suelo
    
    def __init__(self, x, y, w=TILE, h=TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # Rectángulo de colisión

    def draw(self, surface): # Dibuja el suelo con coordenadas del rect.
        draw_ground_tile(surface, (self.rect.x, self.rect.y,
                                   self.rect.w, self.rect.h))


class Flag(pygame.sprite.Sprite):# Bandera de finalizacion del nivel
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 200)  # Poste alto para fácil colisión

    def draw(self, surface):
       
        # Poste vertical
        pygame.draw.rect(surface, GRAY, (self.rect.x + 8, self.rect.y, 4, self.rect.h))
        # Bandera roja en la cima
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y, 20, 40))


class Pipe(pygame.sprite.Sprite):# Tuberias tipo mario clasico
  
    def __init__(self, x, y, h=2*TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE, h)  # Ancho TILE, altura variable

    def draw(self, surface):
        
        pygame.draw.rect(surface, GREEN, self.rect)  # Cuerpo verde
        pygame.draw.rect(surface, DARK_GREEN, self.rect, 2)  # Borde oscuro


class Player(pygame.sprite.Sprite):# Dibuja los personajes principales, maneja su lógica de movimiento, salto y colisiones. 
    def __init__(self, character="mario"):
        super().__init__()
        self.character = character  # Tipo de personaje
        self.rect = pygame.Rect(100, 400, 32, 50)  # Posición inicial y tamaño
        self.vel_x = 0.0  # Velocidad horizontal
        self.vel_y = 0.0  # Velocidad vertical
        self.on_ground = False  # Estado: en suelo
        self.facing_right = True  # Dirección del sprite
        self.score = 0  # Puntuación

        # Colores según personaje
        if character == "mario":
            self.hat_col = RED
            self.clothes_col = RED
            self.pants_col = BLUE
            self.name = "MARIO"
        else:
            self.hat_col = GREEN
            self.clothes_col = GREEN
            self.pants_col = BLUE
            self.name = "LUIGI"

    # ── Física ──────────────────────────────
    def apply_gravity(self):
      
        self.vel_y += GRAVITY  # Aplicar aceleración gravitacional
        if self.vel_y > 16:  # Límite de velocidad de caída
            self.vel_y = 16

    def move(self, keys, platforms):
        
        # Movimiento horizontal: izquierda/derecha
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED  # Velocidad negativa para izquierda
            self.facing_right = False  # Cambiar dirección del sprite
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED  # Velocidad positiva para derecha
            self.facing_right = True  # Cambiar dirección
        else:
            self.vel_x = 0  # Detener si no hay input

        # Salto: ESPACIO, ARRIBA o W, solo si en suelo
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_FORCE  # Aplicar fuerza de salto (negativa)
            self.on_ground = False  # Ya no en suelo

        self.apply_gravity()  # Aplicar gravedad

        # Mover en X: actualizar rect.x, luego colisiones
        self.rect.x += int(self.vel_x)
        self._collide_x(platforms)

        # Mover en Y: actualizar rect.y, reset on_ground, colisiones
        self.rect.y += int(self.vel_y)
        self.on_ground = False  # Asumir no en suelo hasta colisión
        self._collide_y(platforms)

        # Límites de pantalla: evitar salir por lados o arriba
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_W:
            self.rect.right = SCREEN_W
        if self.rect.top > SCREEN_H:
            self.rect.top = 0  # Respawn arriba si cae abajo

    def _collide_x(self, platforms):
    
        for p in platforms:
            if isinstance(p, Brick) and p.broken:  # Ignorar ladrillos destruidos
                continue
            if self.rect.colliderect(p.rect):  # Colisión detectada
                if self.vel_x > 0:  # Moviendo derecha
                    self.rect.right = p.rect.left  # Ajustar a borde izquierdo
                else:  # Moviendo izquierda
                    self.rect.left = p.rect.right  # Ajustar a borde derecho

    def _collide_y(self, platforms):
       
        for p in platforms:
            if isinstance(p, Brick) and p.broken:  # Ignorar rotos
                continue
            if self.rect.colliderect(p.rect):  # Colisión
                if self.vel_y > 0:  # Cayendo
                    self.rect.bottom = p.rect.top  # Ajustar a cima
                    self.vel_y = 0  # Detener caída
                    self.on_ground = True  # Marcar en suelo
                elif self.vel_y < 0:  # Golpeando desde abajo
                    self.rect.top = p.rect.bottom  # Ajustar abajo
                    self.vel_y = 0  # Detener subida
                    if isinstance(p, Brick):  # Si es ladrillo, romper
                        p.hit()

    def draw(self, surface):
        draw_mario(surface,
                   self.rect.x, self.rect.y,
                   facing_right = self.facing_right,
                   hat_color    = self.hat_col,
                   clothes_color= self.clothes_col,
                   pants_color  = self.pants_col)


# ─────────────────────────────────────────────
#  CLASE PRINCIPAL: GAME LOOP PATTERN
# ─────────────────────────────────────────────

class MarioBrosGame: # Inicializa el juego, configura Pygame y prepara grupos de sprites.

    def __init__(self):
        
        try:
            pygame.init()
        except Exception as e:
            print(f"Error inicializando Pygame: {e}")
            sys.exit(1)
        pygame.display.set_caption("Mario Bros - Parcial 1 Arquitectura de Software")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock  = pygame.time.Clock()
        self.font_big   = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)

        self.state   = "SELECT"   # SELECT → PLAYING → GAMEOVER → PAUSED
        self.player  = None
        self.all_sprites = pygame.sprite.Group()  # Grupo para todos los sprites
        self.platforms = pygame.sprite.Group()
        self.bricks    = pygame.sprite.Group()
        self.coins     = pygame.sprite.Group()
        self.particles = []       # efectos visuales al destruir ladrillo
        self.coin_popups = []     # texto "+1" flotante
        self.flag = None
        self.pipes = pygame.sprite.Group()

        self.selected_char = "mario"  # cursor de selección
        self.running = True

    # ══════════════════════════════════════════
    #  GAME LOOP
    # ══════════════════════════════════════════

    def run(self):
       
        while self.running:  # Bucle principal del Game Loop
            self.process_input()  # Fase 1: Procesar entrada
            self.update()         # Fase 2: Actualizar estado
            self.render()         # Fase 3: Renderizar
            self.clock.tick(FPS)  # Fase 4: Controlar tiempo
        pygame.quit()  # Cerrar Pygame al salir
        sys.exit()  # Terminar programa

    # ══════════════════════════════════════════
    #  PROCESS INPUT (Fase 1 del Game Loop)
    # ══════════════════════════════════════════

    def process_input(self):
      
        for event in pygame.event.get():  # Procesar cola de eventos
            if event.type == pygame.QUIT:  # Cerrar ventana
                self.running = False  # Salir del loop

            if self.state == "SELECT":  # Pantalla de selección
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                        # Cambiar selección de personaje
                        self.selected_char = "luigi" if self.selected_char == "mario" else "mario"
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._start_game(self.selected_char)  # Iniciar juego

            elif self.state == "PLAYING":  # Juego activo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "PAUSED"  # Pausar

            elif self.state == "PAUSED":  # Pausado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "PLAYING"  # Reanudar

            elif self.state == "GAMEOVER":  # Fin del juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = "SELECT"  # Reiniciar selección
                    if event.key == pygame.K_ESCAPE:
                        self.running = False  # Salir

    # ══════════════════════════════════════════
    #  UPDATE (Fase 2 del Game Loop)
    # ══════════════════════════════════════════

    def update(self):

        if self.state not in ("PLAYING", "PAUSED"):  # Solo en estados activos
            return

        if self.state == "PAUSED":  # En pausa, no actualizar lógica
            return

        keys = pygame.key.get_pressed()  # Estado actual de teclas

        # Actualizar jugador: movimiento, colisiones
        all_platforms = list(self.platforms) + list(self.bricks)  # Combinar plataformas sólidas
        self.player.move(keys, all_platforms)

        # Actualizar ladrillos: animaciones y remover destruidos
        self.bricks.update()
        self.bricks = pygame.sprite.Group(b for b in self.bricks if not b.broken)  # Filtrar rotos

        # Actualizar monedas: animaciones y recolección
        self.coins.update()
        for c in self.coins:
            if not c.collected and self.player.rect.colliderect(c.rect):  # Colisión con jugador
                c.collected = True
                self.player.score += 1  # Incrementar puntuación
                self.coin_popups.append({  # Agregar popup "+1"
                    "x": c.rect.centerx, "y": c.rect.top,
                    "life": 45  # Duración del popup
                })

        # Limpiar monedas recolectadas de grupos
        self.coins = pygame.sprite.Group(c for c in self.coins if not c.collected)
        self.all_sprites = pygame.sprite.Group(s for s in self.all_sprites if not (hasattr(s, 'collected') and s.collected))

        # Actualizar partículas: movimiento y vida
        for p in self.particles:
            p["x"] += p["vx"]  # Mover horizontal
            p["y"] += p["vy"]  # Mover vertical
            p["vy"] += 0.4     # Gravedad
            p["life"] -= 1     # Reducir vida
        self.particles = [p for p in self.particles if p["life"] > 0]  # Remover muertas

        # Actualizar popups de monedas
        for pop in self.coin_popups:
            pop["y"] -= 1  # Flotar hacia arriba
            pop["life"] -= 1  # Reducir vida
        self.coin_popups = [p for p in self.coin_popups if p["life"] > 0]  # Remover expirados

        # Crear partículas al romper ladrillos (una vez por frame)
        for b in self.bricks:
            if b.broken and b.shake == 7:  # En frame específico de ruptura
                for _ in range(6):  # 6 fragmentos
                    self.particles.append({
                        "x": b.rect.centerx, "y": b.rect.centery,
                        "vx": random.uniform(-3, 3),  # Velocidad aleatoria
                        "vy": random.uniform(-6, -1),
                        "life": 25,  # Duración
                        "color": random.choice([BRICK_COL, BRICK_DARK, BROWN])  # Color aleatorio
                    })

        # Verificar condición de victoria: alcanzar bandera
        if self.flag and self.player.rect.colliderect(self.flag.rect):
            self.state = "GAMEOVER"  # Cambiar a fin de juego

    # ══════════════════════════════════════════
    #  RENDER (Fase 3 del Game Loop)
    # ══════════════════════════════════════════

    def render(self):

        if self.state == "SELECT":
            self._render_select()  # Dibujar selección
        elif self.state == "PLAYING":
            self._render_game()  # Dibujar juego
        elif self.state == "PAUSED":
            self._render_game()  # Dibujar juego base
            self._render_paused()  # Superponer pausa
        elif self.state == "GAMEOVER":
            self._render_gameover()  # Dibujar fin

        pygame.display.flip()  # Actualizar pantalla con cambios

    # ─────────────────────────────────────────
    #  Pantalla de selección
    # ─────────────────────────────────────────
    def _render_select(self): # dibuja partes visuales
        draw_background(self.screen)

        # Título
        title = self.font_big.render("MARIO BROS", True, RED)
        sub   = self.font_med.render("¡Elige tu personaje!", True, WHITE)
        self.screen.blit(title, (SCREEN_W//2 - title.get_width()//2, 60))
        self.screen.blit(sub,   (SCREEN_W//2 - sub.get_width()//2,  110))

        # Instrucciones
        inst = self.font_small.render(
            "← → para cambiar   |   ENTER / ESPACIO para jugar", True, WHITE)
        self.screen.blit(inst, (SCREEN_W//2 - inst.get_width()//2, 150))

        # Mario
        mx = 220
        draw_mario(self.screen, mx, 220,
                   hat_color=RED, clothes_color=RED, pants_color=BLUE)
        mlbl = self.font_med.render("MARIO", True, RED)
        self.screen.blit(mlbl, (mx - mlbl.get_width()//2 + 16, 280))

        # Luigi
        lx = 520
        draw_mario(self.screen, lx, 220,
                   hat_color=GREEN, clothes_color=GREEN, pants_color=BLUE)
        llbl = self.font_med.render("LUIGI", True, GREEN)
        self.screen.blit(llbl, (lx - llbl.get_width()//2 + 16, 280))

        # Cursor (flecha) encima del seleccionado
        arrow_x = mx + 16 if self.selected_char == "mario" else lx + 16
        arrow   = self.font_big.render("▼", True, YELLOW)
        self.screen.blit(arrow, (arrow_x - arrow.get_width()//2, 195))

    # ─────────────────────────────────────────
    #  Pantalla de juego
    # ─────────────────────────────────────────
    def _render_game(self):
        draw_background(self.screen)

        # Dibujar todos los sprites visibles en pantalla
        screen_rect = self.screen.get_rect()
        for sprite in self.all_sprites:
            if screen_rect.colliderect(sprite.rect):
                sprite.draw(self.screen)

        # Partículas
        for p in self.particles:
            if screen_rect.collidepoint(p["x"], p["y"]):
                pygame.draw.rect(self.screen, p["color"],
                                 (int(p["x"]), int(p["y"]), 6, 6))

        # Jugador
        if screen_rect.colliderect(self.player.rect):
            self.player.draw(self.screen)

        # Popups "+1"
        for pop in self.coin_popups:
            if screen_rect.collidepoint(pop["x"], pop["y"]):
                alpha = min(255, pop["life"] * 6)
                surf  = self.font_med.render("+1", True, COIN_GOLD)
                surf.set_alpha(alpha)
                self.screen.blit(surf, (pop["x"] - surf.get_width()//2, pop["y"]))

        # HUD
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_W, 40))
        name_surf  = self.font_med.render(self.player.name, True,
                                          RED if self.player.character=="mario" else GREEN)
        score_surf = self.font_med.render(f"Monedas: {self.player.score}", True, COIN_GOLD)
        ctrl_surf  = self.font_small.render(
            "← → Moverse   ESPACIO/↑ Saltar   P Pausar", True, GRAY)

        self.screen.blit(name_surf,  (10, 8))
        self.screen.blit(score_surf, (SCREEN_W//2 - score_surf.get_width()//2, 8))
        self.screen.blit(ctrl_surf,  (SCREEN_W - ctrl_surf.get_width() - 10, 10))

    # ─────────────────────────────────────────
    #  Pantalla de pausa
    # ─────────────────────────────────────────
    def _render_paused(self):
        # Superponer un overlay semi-transparente
        overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Texto de pausa
        pause_surf = self.font_big.render("PAUSADO", True, WHITE)
        resume_surf = self.font_med.render("Presiona P para continuar", True, GRAY)
        self.screen.blit(pause_surf, (SCREEN_W//2 - pause_surf.get_width()//2, SCREEN_H//2 - 50))
        self.screen.blit(resume_surf, (SCREEN_W//2 - resume_surf.get_width()//2, SCREEN_H//2 + 10))
    # ─────────────────────────────────────────
    def _render_gameover(self):
        draw_background(self.screen)

        char_col = RED if self.player.character == "mario" else GREEN
        draw_mario(self.screen, SCREEN_W//2 - 16, 220,
                   hat_color=self.player.hat_col,
                   clothes_color=self.player.clothes_col,
                   pants_color=self.player.pants_col)

        title = self.font_big.render("¡GANASTE!", True, YELLOW)
        info  = self.font_med.render(
            f"{self.player.name} recogió {self.player.score} monedas 🪙",
            True, WHITE)
        restart = self.font_small.render("R → Volver al menú   |   ESC → Salir", True, RED)

        self.screen.blit(title,   (SCREEN_W//2 - title.get_width()//2,   140))
        self.screen.blit(info,    (SCREEN_W//2 - info.get_width()//2,    290))
        self.screen.blit(restart, (SCREEN_W//2 - restart.get_width()//2, 360))

    # ══════════════════════════════════════════
    #  INICIALIZAR NIVEL
    # ══════════════════════════════════════════

    def _start_game(self, character):# Se construye el nivel con plataformas, ladrillos, monedas y la bandera, y se inicializa el jugador.
        self.player = Player(character)
        self.all_sprites.empty()
        self.platforms.empty()
        self.bricks.empty()
        self.coins.empty()
        self.pipes.empty()
        self.particles = []
        self.coin_popups = []

        # ── Suelo continuo ──────────────────────────────
        for col in range(SCREEN_W // TILE + 1):
            tile = GroundTile(col * TILE, SCREEN_H - TILE)
            self.platforms.add(tile)
            self.all_sprites.add(tile)

        # ── Plataformas flotantes ──────────────
        plat_data = [
            (200, 400, 3),  # Plataforma baja
            (400, 350, 4),  # Plataforma media
            (600, 300, 3),  # Plataforma alta
        ]
        for px, py, n in plat_data:
            for i in range(n):
                tile = GroundTile(px + i * TILE, py)
                self.platforms.add(tile)
                self.all_sprites.add(tile)

        # ── Tuberías ──────────────
        pipe_data = [
            (100, SCREEN_H - 2*TILE, 2*TILE),  # Tubo bajo
            (500, SCREEN_H - 3*TILE, 3*TILE),  # Tubo alto
        ]
        for px, py, h in pipe_data:
            pipe = Pipe(px, py, h)
            self.pipes.add(pipe)
            self.all_sprites.add(pipe)
            self.platforms.add(pipe)  # Para colisiones

        # ── Ladrillos Posiciones ──────────────
        brick_data = [
            (45, 330), (120, 120), (30, 120),  # primera plataforma
            (250, 300), (200, 90), (275, 90),  # segunda platorma
            (460, 250), (400, 40), (500, 40), # tercera plataforma
            (600, 60), (700, 60),  # cuarta plataforma
        ]
        for bx, by in brick_data:
            brick = Brick(bx, by)
            self.bricks.add(brick)
            self.all_sprites.add(brick)

        # ── Monedas ────────────────────────────
        coin_positions = [
            (225, 370), (275, 370), (325, 370),  # Sobre plataformas
            (425, 320), (475, 320), (525, 320),
            (625, 270), (675, 270),
            (150, SCREEN_H - TILE - 20),  # En suelo
            (700, SCREEN_H - TILE - 20),
        ]
        for cx, cy in coin_positions:
            coin = Coin(cx, cy)
            self.coins.add(coin)
            self.all_sprites.add(coin)

        # ── Bandera ────────────────────────────
        self.flag = Flag(750, SCREEN_H - 200)
        self.all_sprites.add(self.flag)

        self.all_sprites.add(self.player)  # Agregar jugador al grupo
        self.state = "PLAYING"


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    game = MarioBrosGame()
    game.run()