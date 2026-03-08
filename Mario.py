import pygame
import sys
import random

# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
class Constants:
    SCREEN_W = 800
    SCREEN_H = 600
    FPS = 60
    GRAVITY = 0.5
    JUMP_FORCE = -13
    MOVE_SPEED = 4
    TILE = 40  # tamaño de cada bloque

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

def draw_mario(surface, x, y, facing_right=True, hat_color=RED, clothes_color=RED, pants_color=BLUE):
    """
    Dibuja un sprite pixel art de un personaje estilo Mario (32x48 píxeles).
    Parámetros:
    - surface: Superficie de Pygame donde dibujar (e.g., pantalla).
    - x, y: Posición superior izquierda del sprite.
    - facing_right: Booleano para dirección (True: derecha, False: izquierda).
    - hat_color, clothes_color, pants_color: Colores personalizables para sombrero, ropa y pantalones.
    Funcionalidad: Usa pygame.draw.rect para crear formas rectangulares que simulan pixel art.
    Variables locales: ox, oy = coordenadas enteras para precisión.
    """
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


def draw_brick(surface, rect, broken=False):
    """
    Dibuja un ladrillo con textura simple si no está roto.
    Parámetros:
    - surface: Superficie donde dibujar.
    - rect: Tupla (x, y, w, h) para posición y tamaño.
    - broken: Booleano; si True, no dibuja nada (ladrillo destruido).
    Funcionalidad: Dibuja rectángulo principal, borde, y líneas para simular mortero.
    Variables: x, y, w, h desempaquetadas de rect.
    """
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


def draw_coin(surface, cx, cy, r=10, anim=0):
    """Moneda animada (aplana/ensancha en función del anim 0-1)."""
    width = max(3, int(r * 2 * (0.4 + 0.6 * abs(anim))))
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


def draw_background(surface):
    surface.fill(SKY_BLUE)
    # nubes decorativas
    for cx, cy in [(100, 80), (300, 50), (550, 90), (700, 60)]:
        pygame.draw.ellipse(surface, WHITE, (cx-30, cy-15, 60, 30))
        pygame.draw.ellipse(surface, WHITE, (cx-15, cy-25, 50, 30))
        pygame.draw.ellipse(surface, WHITE, (cx+5,  cy-15, 40, 25))


# ─────────────────────────────────────────────
#  CLASES DEL JUEGO
# ─────────────────────────────────────────────

class Coin(pygame.sprite.Sprite):
    """
    Representa una moneda recolectable en el juego.
    Hereda de pygame.sprite.Sprite para integración con grupos.
    Atributos:
    - rect: Rectángulo de colisión y posición (20x20 px).
    - anim: Valor de animación (0-1) para efecto de rotación.
    - anim_dir: Dirección de la animación (+1 o -1).
    - collected: Booleano; True si recolectada, evita dibujado.
    Funcionalidad: update() anima la moneda; draw() la dibuja si no recolectada.
    """
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)  # Posición y tamaño de la moneda
        self.anim = 0.0  # Valor inicial de animación
        self.anim_dir = 1  # Dirección de animación (incrementa)
        self.collected = False  # Estado de recolección

    def update(self):
        """
        Actualiza la animación de la moneda.
        Incrementa anim, invierte dirección en límites para oscilar entre -1 y 1.
        """
        self.anim += 0.05 * self.anim_dir  # Avanza animación
        if self.anim >= 1.0:  # Límite superior
            self.anim_dir = -1  # Invertir dirección
        if self.anim <= -1.0:  # Límite inferior
            self.anim_dir = 1  # Invertir dirección

    def draw(self, surface):
        """
        Dibuja la moneda si no ha sido recolectada.
        Llama a draw_coin con centro del rect y animación actual.
        """
        if not self.collected:
            draw_coin(surface, self.rect.centerx, self.rect.centery,
                      r=10, anim=self.anim)


class Brick(pygame.sprite.Sprite):
    """
    Representa un ladrillo destructible en el juego.
    Se rompe al ser golpeado desde abajo, con animación de sacudida.
    Atributos:
    - rect: Posición y tamaño (usando TILE por defecto).
    - broken: Booleano; True si destruido.
    - shake: Contador de frames para animación de ruptura (0-8).
    - oy: Posición Y original para animación.
    Funcionalidad: hit() inicia ruptura; update() maneja animación; draw() dibuja si no roto.
    """
    def __init__(self, x, y, w=TILE, h=TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # Rectángulo de colisión
        self.broken = False  # Estado de ruptura
        self.shake = 0  # Frames restantes de animación
        self.oy = y  # Posición Y original

    def hit(self):
        """
        Marca el ladrillo como roto y inicia animación de sacudida.
        Solo si no estaba roto previamente.
        """
        if not self.broken:
            self.broken = True  # Marcar como roto
            self.shake = 8  # Iniciar animación de 8 frames

    def update(self):
        """
        Actualiza la animación de ruptura.
        Si shake > 0, mueve Y alternadamente para efecto de sacudida.
        Decrementa shake hasta 0, luego restaura Y original.
        """
        if self.shake > 0:
            self.rect.y = self.oy - (self.shake % 2) * 4  # Sacudida: alterna -4 y 0
            self.shake -= 1  # Reducir contador
        else:
            self.rect.y = self.oy  # Restaurar posición original

    def draw(self, surface):
        """
        Dibuja el ladrillo si no está roto.
        Llama a draw_brick con rect actual.
        """
        if not self.broken:
            draw_brick(surface, (self.rect.x, self.rect.y,
                                 self.rect.w, self.rect.h))


class GroundTile(pygame.sprite.Sprite):
    """
    Representa un tile de suelo o plataforma sólida.
    No tiene lógica especial, solo colisión y dibujado.
    Atributos:
    - rect: Posición y tamaño (usando TILE por defecto).
    Funcionalidad: draw() dibuja el tile usando draw_ground_tile.
    """
    def __init__(self, x, y, w=TILE, h=TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)  # Rectángulo de colisión

    def draw(self, surface):
        """
        Dibuja el tile de suelo.
        Llama a draw_ground_tile con coordenadas del rect.
        """
        draw_ground_tile(surface, (self.rect.x, self.rect.y,
                                   self.rect.w, self.rect.h))


class Flag(pygame.sprite.Sprite):
    """
    Representa la bandera de victoria al final del nivel.
    Objetivo del juego: alcanzar para ganar.
    Atributos:
    - rect: Poste alto (20x200 px) para colisión.
    Funcionalidad: draw() dibuja poste y bandera roja.
    """
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 200)  # Poste alto para fácil colisión

    def draw(self, surface):
        """
        Dibuja la bandera: poste gris y bandera roja triangular.
        """
        # Poste vertical
        pygame.draw.rect(surface, GRAY, (self.rect.x + 8, self.rect.y, 4, self.rect.h))
        # Bandera roja en la cima
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y, 20, 40))


class Pipe(pygame.sprite.Sprite):
    """
    Representa una tubería verde como obstáculo decorativo.
    Similar a Super Mario Bros, bloquea paso pero no interactúa.
    Atributos:
    - rect: Posición y altura variable (ancho fijo TILE).
    Funcionalidad: draw() dibuja tubería verde con borde.
    """
    def __init__(self, x, y, h=2*TILE):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE, h)  # Ancho TILE, altura variable

    def draw(self, surface):
        """
        Dibuja la tubería: rectángulo verde con borde oscuro.
        """
        pygame.draw.rect(surface, GREEN, self.rect)  # Cuerpo verde
        pygame.draw.rect(surface, DARK_GREEN, self.rect, 2)  # Borde oscuro


class Player(pygame.sprite.Sprite):
    """
    Representa al personaje jugable (Mario o Luigi).
    Maneja movimiento, física, colisiones y dibujado.
    Atributos principales:
    - character: "mario" o "luigi" para colores y nombre.
    - rect: Posición y tamaño (32x50 px).
    - vel_x, vel_y: Velocidades horizontal y vertical.
    - on_ground: Booleano para estado en suelo.
    - facing_right: Dirección del sprite.
    - score: Puntos acumulados.
    - hat_col, clothes_col, pants_col: Colores personalizados.
    Funcionalidad: move() procesa input y física; colisiones en _collide_x/y.
    """
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
        """
        Aplica gravedad a la velocidad vertical.
        Incrementa vel_y con GRAVITY, limita a 16 para evitar caídas infinitas.
        """
        self.vel_y += GRAVITY  # Aplicar aceleración gravitacional
        if self.vel_y > 16:  # Límite de velocidad de caída
            self.vel_y = 16

    def move(self, keys, platforms):
        """
        Procesa input del usuario y actualiza posición con física.
        Parámetros:
        - keys: Estado de teclas (de pygame.key.get_pressed()).
        - platforms: Lista de sprites para colisiones.
        Funcionalidad: Maneja movimiento horizontal, salto, gravedad, colisiones.
        Variables: vel_x/vel_y actualizadas; rect movido; límites de pantalla.
        """
        # Movimiento horizontal: izquierda/derecha o A/D
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
        """
        Maneja colisiones horizontales con plataformas.
        Parámetros: platforms - lista de sprites sólidos.
        Funcionalidad: Para cada plataforma, si colisión, ajusta rect.x para detener movimiento.
        Ignora ladrillos rotos.
        """
        for p in platforms:
            if isinstance(p, Brick) and p.broken:  # Ignorar ladrillos destruidos
                continue
            if self.rect.colliderect(p.rect):  # Colisión detectada
                if self.vel_x > 0:  # Moviendo derecha
                    self.rect.right = p.rect.left  # Ajustar a borde izquierdo
                else:  # Moviendo izquierda
                    self.rect.left = p.rect.right  # Ajustar a borde derecho

    def _collide_y(self, platforms):
        """
        Maneja colisiones verticales con plataformas.
        Parámetros: platforms - lista de sprites sólidos.
        Funcionalidad: Detecta colisión, ajusta posición y velocidad.
        Si cayendo, pone en suelo; si golpeando arriba, rompe ladrillo.
        Ignora ladrillos rotos.
        """
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

class MarioBrosGame:
    """
    Clase principal que implementa el patrón de diseño Game Loop.
    El Game Loop es el ciclo principal del juego, ejecutado en run():
    while running:
        process_input()  # 1. Procesar entrada del usuario
        update()         # 2. Actualizar estado del juego (lógica, física)
        render()         # 3. Dibujar en pantalla
        clock.tick(FPS)  # 4. Controlar velocidad (60 FPS)

    Estados del juego:
    - SELECT: Pantalla de selección de personaje.
    - PLAYING: Juego activo, con movimiento y colisiones.
    - PAUSED: Juego pausado, esperando input para reanudar.
    - GAMEOVER: Fin del juego, victoria al alcanzar bandera.

    Atributos principales:
    - screen: Superficie de Pygame para dibujar.
    - clock: Controla FPS.
    - state: Estado actual del juego.
    - player: Instancia del personaje jugable.
    - all_sprites: Grupo de todos los sprites para dibujado eficiente.
    - platforms, bricks, coins, pipes: Grupos específicos de objetos.
    - flag: Bandera de victoria.
    - particles, coin_popups: Efectos visuales.

    Funcionalidad: Inicializa Pygame, maneja loop, transiciones de estado.
    """

    def __init__(self):
        """
        Inicializa el juego, configura Pygame y prepara grupos de sprites.
        """
        try:
            pygame.init()
        except Exception as e:
            print(f"Error inicializando Pygame: {e}")
            sys.exit(1)
        pygame.display.set_caption("Mario Bros - Game Loop Pattern")
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
        """
        EJECUCIÓN DEL GAME LOOP PRINCIPAL:
        Ciclo continuo mientras running=True.
        Fases del Game Loop:
        1. process_input(): Maneja eventos y teclas.
        2. update(): Actualiza lógica del juego.
        3. render(): Dibuja en pantalla.
        4. clock.tick(FPS): Limita a 60 FPS.
        Al salir, cierra Pygame y termina programa.
        """
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
        """
        FASE 1 DEL GAME LOOP: Procesar entrada del usuario.
        Maneja eventos de Pygame (teclas, mouse, cierre ventana).
        Dependiendo del estado:
        - SELECT: Cambiar personaje, iniciar juego.
        - PLAYING: Pausar con P.
        - PAUSED: Reanudar con P.
        - GAMEOVER: Reiniciar o salir.
        Variables: event (de pygame.event.get()), self.state actualizado.
        """
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
        """
        FASE 2 DEL GAME LOOP: Actualizar estado del juego.
        Solo ejecuta si estado es PLAYING o PAUSED (pero en PAUSED no actualiza lógica).
        Funcionalidad:
        - Mover jugador con input y física.
        - Actualizar ladrillos (romper si golpeados).
        - Recolectar monedas, actualizar puntuación.
        - Gestionar partículas y popups.
        - Verificar victoria (alcanzar bandera).
        Variables: keys (estado teclas), self.player, grupos de sprites actualizados.
        """
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
        """
        FASE 3 DEL GAME LOOP: Dibujar el estado actual en pantalla.
        Dependiendo del estado, llama a método específico:
        - SELECT: Pantalla de selección de personaje.
        - PLAYING: Juego activo con sprites y HUD.
        - PAUSED: Juego + overlay de pausa.
        - GAMEOVER: Pantalla de victoria.
        Finalmente, pygame.display.flip() actualiza pantalla.
        Variables: self.screen actualizada con dibujos.
        """
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
    def _render_select(self):
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

        # Jugador (ya incluido en all_sprites, pero asegurar)
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
        restart = self.font_small.render("R → Volver al menú   |   ESC → Salir", True, GRAY)

        self.screen.blit(title,   (SCREEN_W//2 - title.get_width()//2,   140))
        self.screen.blit(info,    (SCREEN_W//2 - info.get_width()//2,    290))
        self.screen.blit(restart, (SCREEN_W//2 - restart.get_width()//2, 360))

    # ══════════════════════════════════════════
    #  INICIALIZAR NIVEL
    # ══════════════════════════════════════════

    def _start_game(self, character):
        self.player = Player(character)
        self.all_sprites.empty()
        self.platforms.empty()
        self.bricks.empty()
        self.coins.empty()
        self.pipes.empty()
        self.particles = []
        self.coin_popups = []

        # ── Suelo continuo (estilo Mario 1-1) ──────────────────────────────
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

        # ── Ladrillos ──────────────
        brick_data = [
            (250, 320), (300, 320), (350, 320),  # Sobre primera plataforma
            (450, 270), (500, 270), (550, 270),  # Sobre segunda
            (650, 220), (700, 220),  # Sobre tercera
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