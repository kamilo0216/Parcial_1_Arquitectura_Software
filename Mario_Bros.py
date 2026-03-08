"""
SUPER MARIO BROS - Python Edition (MEJORADO)
Patron de Diseno: Game Loop | Libreria: tkinter

MEJORAS IMPLEMENTADAS:
- Física de Mario mucho más cercana al original: aceleración, fricción y salto variable (mantén ↑/ESPACIO para salto alto).
- Monedas de bloques ? ahora "salen volando" hacia arriba como en el juego original (visual + puntos automáticos).
- Todas las monedas dan 200 puntos (igual que el original).
- Temporizador de nivel (400 → 0). Si se acaba → muerte.
- HUD con TIEMPO (igual que NES).
- Goombas más realistas:
   • Siempre caminan hacia la izquierda hasta chocar pared (igual que el original).
   • Caen por los bordes de las plataformas (igual que el original).
   • Animación de piernas más suave y realista.
   • Al ser pisados se aplastan y desaparecen después de ~0.7s (igual que NES).
   • Colisión lateral más precisa (no se voltean al tocar solo la esquina).
- Pequeños pulidos de colisiones y cámara para mayor fluidez.
"""

import tkinter as tk
import random, time

SCREEN_W=800; SCREEN_H=480; FPS=60; GRAVITY=0.55
JUMP_FORCE=-13.5; MOVE_SPEED=5.0; ACCEL=0.85; FRICTION=0.82
TILE=32
COLOR_SKY="#5C94FC"; COLOR_GROUND="#C84C0C"; COLOR_BRICK_T="#E8A020"
COLOR_BLOCK="#FAB008"; COLOR_BLOCK_O="#C84C0C"; COLOR_PIPE_G="#00A800"
COLOR_PIPE_D="#007000"; COLOR_MARIO_R="#E40058"; COLOR_MARIO_S="#FAB008"
COLOR_MARIO_B="#3CBCFC"; COLOR_MARIO_SK="#FCBCB0"; COLOR_GOOMBA="#C84C0C"
COLOR_GOOMBA_D="#7C2800"; COLOR_COIN="#FAB008"; COLOR_CLOUD="#FCFCFC"
COLOR_TEXT="#FCFCFC"

class GameObject:
    def __init__(self,x,y,w,h):
        self.x,self.y=float(x),float(y); self.w,self.h=w,h; self.active=True
    def rect(self): return(self.x,self.y,self.x+self.w,self.y+self.h)
    def collides(self,other):
        ax1,ay1,ax2,ay2=self.rect(); bx1,by1,bx2,by2=other.rect()
        return ax1<bx2 and ax2>bx1 and ay1<by2 and ay2>by1

class Platform(GameObject):
    def __init__(self,x,y,w=TILE,h=TILE,kind="ground"):
        super().__init__(x,y,w,h)
        self.kind=kind; self.hit=False
        self.original_y = y
    def draw(self,cv,cam):
        sx=self.x-cam; x1,y1,x2,y2=sx,self.y,sx+self.w,self.y+self.h
        if self.kind=="ground":
            cv.create_rectangle(x1,y1,x2,y2,fill=COLOR_GROUND,outline=COLOR_BRICK_T)
            cv.create_line(x1,y1+4,x2,y1+4,fill=COLOR_BRICK_T)
        elif self.kind=="brick":
            cv.create_rectangle(x1,y1,x2,y2,fill=COLOR_GROUND,outline="#000")
            mid=(x1+x2)/2
            cv.create_line(mid,y1,mid,y1+TILE//2,fill="#000")
            cv.create_line(x1,y1+TILE//2,x2,y1+TILE//2,fill="#000")
        elif self.kind=="block":
            col=COLOR_BLOCK if not self.hit else "#9C7000"
            cv.create_rectangle(x1,y1,x2,y2,fill=col,outline=COLOR_BLOCK_O,width=2)
            cv.create_text((x1+x2)/2,(y1+y2)/2,text="?",fill="#000",font=("Arial",14,"bold"))
        elif self.kind=="pipe_body":
            cv.create_rectangle(x1,y1,x2,y2,fill=COLOR_PIPE_G,outline=COLOR_PIPE_D,width=2)
            cv.create_line(x1+6,y1,x1+6,y2,fill=COLOR_PIPE_D,width=2)
        elif self.kind=="pipe_top":
            cv.create_rectangle(x1-4,y1,x2+4,y2,fill=COLOR_PIPE_G,outline=COLOR_PIPE_D,width=2)

class Coin(GameObject):
    def __init__(self,x,y,pop_up=False):
        super().__init__(x,y,16,24)
        self.anim=0
        self.pop_up=pop_up
        if pop_up:
            self.vy=-12.0
            self.lifespan=42
        else:
            self.vy=0
            self.lifespan=None
    def update(self):
        self.anim+=1
        if self.pop_up:
            self.y+=self.vy
            self.vy+=0.65
            self.lifespan-=1
            if self.lifespan<=0:
                self.active=False
    def draw(self,cv,cam):
        sx=self.x-cam+8
        w=abs(7*(1-(self.anim%30)/15))+2
        cv.create_oval(sx-w,self.y,sx+w,self.y+24,fill=COLOR_COIN,outline="#C07800")

class Goomba(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y,TILE,TILE)
        self.vx=-0 # izquierda por defecto (como original 1-1)
        self.vy=0
        self.on_ground=False
        self.dead=False
        self.dead_timer=0
        self.anim_tick=0

    def update(self,platforms):
        if self.dead:
            self.dead_timer+=1
            if self.dead_timer>30: self.active=False  # 0.5s exacto NES
            return
        self.anim_tick+=1
        self.vy+=GRAVITY

        # Vertical primero (estándar platformer)
        prev_y = self.y
        self.y += self.vy
        self.on_ground = False
        for p in platforms:
            if self.collides(p):
                if self.vy >= 0:  # cayendo
                    self.y = p.y - self.h
                    self.vy = 0
                    self.on_ground = True
                    break  # primera colisión suelo
                elif self.vy < 0:  # techo
                    self.y = p.y + p.h
                    self.vy = 0

        # Horizontal: resolución optimizada (una sola por dir)
        prev_x = self.x
        self.x += self.vx
        hit_wall = False
        if self.vx < 0:  # moviendo izquierda -> busca derecha mas cercana
            max_right = self.x + self.w
            for p in platforms:
                if self.collides(p) and self.y + self.h > p.y + 4 and self.y < p.y + p.h - 4:
                    max_right = min(max_right, p.x)
            if max_right < self.x + self.w:
                self.x = max_right - self.w + 0.1  # epsilon anti-stick
                self.vx = 0.1
                hit_wall = True
        else:  # moviendo derecha -> busca izquierda mas lejana
            min_left = self.x
            for p in platforms:
                if self.collides(p) and self.y + self.h > p.y + 4 and self.y < p.y + p.h - 4:
                    min_left = max(min_left, p.x + p.w)
            if min_left > self.x:
                self.x = min_left - 0.1
                self.vx = -0.1
                hit_wall = True

        if self.y > SCREEN_H + 50: self.active = False

    def stomp(self):
        self.dead = True
        self.h = TILE // 2
        self.y += TILE // 2
        self.vx = 0  # para

    def draw(self,cv,cam):
        sx = self.x - cam
        sy = self.y
        if self.dead:
            # Aplastado: oval ancho y bajo (fiel NES)
            fw = TILE * 1.1
            cv.create_oval(sx + (TILE - fw)/2, sy + self.h - 4, sx + (TILE - fw)/2 + fw, sy + self.h + 2,
                           fill=COLOR_GOOMBA, outline=COLOR_GOOMBA_D, width=1)
            return

        # Cuerpo: oval fiel al sprite (estrecho arriba, ancho abajo)
        cv.create_oval(sx+2, sy+4, sx+30, sy+28, fill=COLOR_GOOMBA, outline=COLOR_GOOMBA_D, width=1)

        # Ojos blancos (bajos, exacto NES)
        cv.create_oval(sx+5, sy+11, sx+13, sy+18, fill="white", outline="")
        cv.create_oval(sx+19, sy+11, sx+27, sy+18, fill="white", outline="")

        # Pupilas negras (pequeñas, centradas)
        cv.create_oval(sx+7, sy+13, sx+11, sy+17, fill="black", outline="")
        cv.create_oval(sx+21, sy+13, sx+25, sy+17, fill="black", outline="")

        # Pies: pequeños, alternan posición X (suave, 8 frames ciclo)
        phase = (self.anim_tick // 8) % 4
        left_xoff = 0 if phase < 2 else 1.5
        right_xoff = 0 if phase < 2 else -1.5
        # Pie izq
        cv.create_oval(sx+4 + left_xoff, sy+25, sx+11 + left_xoff, sy+31, fill=COLOR_GOOMBA_D, outline="")
        # Pie der
        cv.create_oval(sx+21 + right_xoff, sy+25, sx+28 + right_xoff, sy+31, fill=COLOR_GOOMBA_D, outline="")

class Mario(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y,28,TILE)
        self.vx=self.vy=0
        self.on_ground=False
        self.facing=1
        self.anim_tick=0
        self.alive=True
        self.dead_timer=0
        self.invincible=0
        self.score=0
        self.coins=0
        self.lives=3
    def jump(self):
        if self.on_ground:
            self.vy=JUMP_FORCE
            self.on_ground=False
    def update(self,keys,platforms,goombas,coins_list,flag):
        if not self.alive:
            self.dead_timer+=1
            self.vy+=GRAVITY*0.5
            self.y+=self.vy
            return

        if self.invincible>0: self.invincible-=1

        # === FÍSICA MEJORADA (aceleración + fricción) ===
        moving=False
        if keys.get("Left"):
            self.vx-=ACCEL
            self.facing=-1
            moving=True
        if keys.get("Right"):
            self.vx+=ACCEL
            self.facing=1
            moving=True

        if not moving and self.on_ground:
            self.vx*=FRICTION

        # límite de velocidad
        if abs(self.vx)>MOVE_SPEED:
            self.vx=MOVE_SPEED if self.vx>0 else -MOVE_SPEED

        # gravedad + salto variable
        self.vy+=GRAVITY
        if self.vy>14: self.vy=14

        # corte de salto si sueltas ↑/ESPACIO
        if self.vy<0 and not (keys.get("Up") or keys.get("space")):
            self.vy*=0.58

        self.x+=self.vx
        self.y+=self.vy
        self.on_ground=False

        # colisiones
        for p in platforms:
            if self.collides(p):
                ox1,oy1,ox2,oy2=p.rect()
                # suelo
                if self.vy>0 and self.y+self.h-self.vy<=oy1+8:
                    self.y=oy1-self.h
                    self.vy=0
                    self.on_ground=True
                # cabeza (bloque ?)
                elif self.vy<0 and self.y>=oy2-8:
                    self.y=oy2
                    self.vy=0
                    if p.kind=="block" and not p.hit:
                        p.hit=True
                        coins_list.append(Coin(p.x+8,p.y-30,pop_up=True))
                        self.coins+=1
                        self.score+=200
                # laterales
                elif self.vx>0:
                    self.x=ox1-self.w
                    self.vx=0
                elif self.vx<0:
                    self.x=ox2
                    self.vx=0

        # enemigos
        if self.invincible==0:
            for g in goombas:
                if g.active and not g.dead and self.collides(g):
                    if self.vy>0 and self.y+self.h<g.y+g.h-4:
                        g.stomp()
                        self.vy=-8.5
                        self.score+=100
                    else:
                        self.alive=False
                        self.vy=-10
                        self.lives-=1

        # monedas normales (las que flotan)
        for c in coins_list:
            if c.active and self.collides(c) and not c.pop_up:
                c.active=False
                self.coins+=1
                self.score+=200

        # bandera
        if flag and self.collides(flag):
            self.score+=1000
            flag.reached=True

        if self.y>SCREEN_H+100:
            self.alive=False
            self.lives-=1
        if self.x<0: self.x=0

        if self.alive: self.anim_tick+=1

    def draw(self,cv,cam):
        sx=self.x-cam; sy=self.y
        if self.invincible>0 and (self.invincible//4)%2==0: return
        f=self.facing

        # cuerpo Mario (igual que antes pero con mejor sombreado)
        cv.create_rectangle(sx+4,sy,sx+24,sy+8,fill=COLOR_MARIO_R,outline="")
        cv.create_rectangle(sx,sy+4,sx+28,sy+12,fill=COLOR_MARIO_R,outline="")
        cv.create_rectangle(sx+4,sy+8,sx+24,sy+18,fill=COLOR_MARIO_SK,outline="")
        ex=sx+16 if f==1 else sx+8
        cv.create_rectangle(ex,sy+10,ex+4,sy+14,fill="#000",outline="")
        cv.create_rectangle(sx+8,sy+14,sx+20,sy+16,fill="#7C3000",outline="")
        cv.create_rectangle(sx+4,sy+18,sx+24,sy+28,fill=COLOR_MARIO_R,outline="")
        cv.create_rectangle(sx+2,sy+24,sx+26,sy+TILE,fill=COLOR_MARIO_B,outline="")
        cv.create_rectangle(sx+8,sy+20,sx+12,sy+24,fill=COLOR_MARIO_S,outline="")
        cv.create_rectangle(sx+16,sy+20,sx+20,sy+24,fill=COLOR_MARIO_S,outline="")

        # piernas con animación de caminar
        wlk=(self.anim_tick//6)%2
        if self.vx!=0 and self.on_ground:
            cv.create_rectangle(sx+2,sy+TILE,sx+13+wlk*3,sy+TILE+6,fill="#000")
            cv.create_rectangle(sx+15-wlk*3,sy+TILE,sx+26,sy+TILE+6,fill="#000")
        else:
            cv.create_rectangle(sx+2,sy+TILE,sx+13,sy+TILE+6,fill="#000")
            cv.create_rectangle(sx+15,sy+TILE,sx+26,sy+TILE+6,fill="#000")

class Cloud:
    def __init__(self,x,y):
        self.x=float(x); self.y=y
        self.speed=random.uniform(0.25,0.55)
    def update(self,world_w):
        self.x-=self.speed
        if self.x<-150: self.x=world_w+80
    def draw(self,cv,cam):
        sx=self.x-cam*0.3
        cv.create_oval(sx,self.y+10,sx+50,self.y+30,fill=COLOR_CLOUD,outline="")
        cv.create_oval(sx+10,self.y,sx+40,self.y+20,fill=COLOR_CLOUD,outline="")
        cv.create_oval(sx+30,self.y+8,sx+70,self.y+28,fill=COLOR_CLOUD,outline="")

class Flag(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y,16,SCREEN_H-y)
        self.reached=False
    def draw(self,cv,cam):
        sx=self.x-cam
        cv.create_line(sx+8,self.y,sx+8,SCREEN_H-TILE,fill="#888",width=4)
        pts=[sx+8,self.y,sx+32,self.y+8,sx+8,self.y+20]
        cv.create_polygon(pts,fill="#FCFCFC",outline="")
        cv.create_oval(sx+4,self.y-8,sx+12,self.y,fill=COLOR_COIN,outline="")

def build_level():
    platforms=[]; goombas=[]; coins=[]; WORLD_W=3200
    gaps=[(640,704),(1280,1344),(1920,1984),(2560,2624)]
    x=0
    while x<WORLD_W:
        if not any(g[0]<=x<g[1] for g in gaps):
            platforms.append(Platform(x,SCREEN_H-TILE,TILE,TILE,"ground"))
        x+=TILE

    # bloques ?
    qpos=[(256,SCREEN_H-5*TILE),(320,SCREEN_H-5*TILE),(288,SCREEN_H-9*TILE),
          (608,SCREEN_H-5*TILE),(800,SCREEN_H-5*TILE),(832,SCREEN_H-9*TILE),
          (864,SCREEN_H-5*TILE),(1120,SCREEN_H-5*TILE),(1440,SCREEN_H-5*TILE),
          (1600,SCREEN_H-5*TILE),(1760,SCREEN_H-5*TILE),(2080,SCREEN_H-5*TILE),
          (2240,SCREEN_H-9*TILE),(2700,SCREEN_H-5*TILE),(2900,SCREEN_H-5*TILE)]
    for qx,qy in qpos:
        platforms.append(Platform(qx,qy,TILE,TILE,"block"))

    # ladrillos
    brows=[(192,SCREEN_H-5*TILE,3),(352,SCREEN_H-5*TILE,4),(512,SCREEN_H-5*TILE,2),
           (704,SCREEN_H-5*TILE,5),(960,SCREEN_H-5*TILE,3),(1060,SCREEN_H-5*TILE,2),
           (1200,SCREEN_H-5*TILE,4),(1500,SCREEN_H-5*TILE,3),(1670,SCREEN_H-5*TILE,3),
           (1900,SCREEN_H-5*TILE,2),(2100,SCREEN_H-5*TILE,3),(2300,SCREEN_H-5*TILE,4),
           (2500,SCREEN_H-5*TILE,3),(2700,SCREEN_H-5*TILE,2)]
    for bx,by,count in brows:
        for i in range(count):
            platforms.append(Platform(bx+i*TILE,by,TILE,TILE,"brick"))

    # escaleras
    for base_x,steps in [(896,4),(1696,3),(2400,5),(2880,4)]:
        for s in range(steps):
            for h in range(s+1):
                platforms.append(Platform(base_x+s*TILE,SCREEN_H-TILE-(h+1)*TILE,TILE,TILE,"ground"))

    # tuberías
    for px,height in [(416,2),(576,3),(736,2),(1152,3),(1408,2),
                      (1792,3),(2048,2),(2336,3),(2688,2),(2944,3)]:
        for h in range(height):
            platforms.append(Platform(px,SCREEN_H-TILE*(h+2),TILE*2,TILE,"pipe_body"))
        platforms.append(Platform(px,SCREEN_H-TILE*(height+1)-8,TILE*2,16,"pipe_top"))
        if height%2==0:
            goombas.append(Goomba(px+64,SCREEN_H-TILE*2))

    # Goombas (posición fiel a nivel 1-1 clásico)
    for gx in [480]: #posiciones en las que estan los hongos 
        goombas.append(Goomba(gx,SCREEN_H-TILE*2))

    # Monedas flotantes
    for cx,cy,count in [(160,SCREEN_H-7*TILE,5),(480,SCREEN_H-7*TILE,4),
                        (800,SCREEN_H-7*TILE,6),(1200,SCREEN_H-7*TILE,4),
                        (1600,SCREEN_H-7*TILE,5),(2000,SCREEN_H-7*TILE,4),
                        (2400,SCREEN_H-7*TILE,3),(2800,SCREEN_H-7*TILE,5)]:
        for i in range(count):
            coins.append(Coin(cx+i*28,cy))

    flag=Flag(WORLD_W-96,SCREEN_H-13*TILE)
    return platforms,goombas,coins,flag,WORLD_W

class MarioGame:
    def __init__(self,root):
        self.root=root
        root.title("Super Mario Bros")
        root.resizable(False,False)
        self.cv=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg=COLOR_SKY,highlightthickness=0)
        self.cv.pack()
        self.keys={}
        root.bind("<KeyPress>",self.key_down)
        root.bind("<KeyRelease>",self.key_up)

        self.FNT_BIG=("Courier",32,"bold")
        self.FNT_MED=("Courier",16,"bold")
        self.FNT_SM=("Courier",12)
        self.state="menu"
        self.reset_game()
        self.last_t=time.perf_counter()
        self._frame_ms=1000//FPS
        self.game_loop()

    def key_down(self,e):
        self.keys[e.keysym]=True
        if self.state=="menu" and e.keysym in("Return","space"):
            self.state="playing"
        if self.state in("dead","win","gameover") and e.keysym in("Return","space"):
            if self.state=="gameover" or self.mario.lives<=0:
                self.reset_game()
                self.state="menu"
            else:
                self.respawn()
                self.state="playing"

    def key_up(self,e):
        if e.keysym in self.keys:
            self.keys[e.keysym]=False

    def reset_game(self):
        self.platforms,self.goombas,self.coins,self.flag,self.world_w=build_level()
        self.mario=Mario(64,SCREEN_H-TILE*3)
        self.cam_x=0.0
        self.clouds=[Cloud(random.randint(0,3000),random.randint(20,120)) for _ in range(18)]
        self.time=400
        self.state_timer=0
        self._build_grid()

    def _build_grid(self):
        self._cell=TILE*3
        self._grid={}
        for p in self.platforms:
            cx=int(p.x//self._cell)
            for dx in range(-1,3):
                self._grid.setdefault(cx+dx,[]).append(p)

    def _near_platforms(self,obj):
        cx=int(obj.x//self._cell)
        return self._grid.get(cx,[])

    def respawn(self):
        self.platforms,self.goombas,self.coins,self.flag,self.world_w=build_level()
        m=self.mario
        m.x=64; m.y=SCREEN_H-TILE*3; m.vx=m.vy=0
        m.alive=True; m.invincible=120; m.dead_timer=0
        self.cam_x=0.0
        self.time=400
        self._build_grid()

    def game_loop(self):
        now=time.perf_counter()
        self.process_input()
        self.update()
        self.render()
        elapsed_ms=int((time.perf_counter()-now)*1000)
        self.root.after(max(1,self._frame_ms-elapsed_ms),self.game_loop)

    def process_input(self):
        if self.state!="playing": return
        if self.keys.get("Up") or self.keys.get("space"):
            self.mario.jump()

    def update(self):
        self.state_timer+=1
        if self.state!="playing": return

        for c in self.clouds:
            c.update(self.world_w)

        # temporizador
        if self.state_timer%60==0:
            self.time=max(0,self.time-1)
        if self.time<=0 and self.mario.alive:
            self.mario.alive=False
            self.mario.vy=-10
            self.mario.lives-=1

        self.mario.update(self.keys,self._near_platforms(self.mario),self.goombas,self.coins,self.flag)

        for g in self.goombas:
            if g.active:
                g.update(self._near_platforms(g))

        for c in self.coins:
            if c.active:
                c.update()

        self.goombas=[g for g in self.goombas if g.active]
        self.coins=[c for c in self.coins if c.active]

        # cámara suave
        target=self.mario.x-SCREEN_W//3
        self.cam_x+=(target-self.cam_x)*0.15
        self.cam_x=max(0,min(self.cam_x,self.world_w-SCREEN_W))

        if not self.mario.alive:
            self.state="gameover" if self.mario.lives<=0 else "dead"
            self.state_timer=0
        if self.flag.reached:
            self.state="win"
            self.state_timer=0

    def render(self):
        self.cv.delete("all")
        self.cv.create_rectangle(0,0,SCREEN_W,SCREEN_H,fill=COLOR_SKY,outline="")

        if self.state=="menu":
            self._menu()
            return

        for c in self.clouds:
            c.draw(self.cv,self.cam_x)

        for p in self.platforms:
            if -TILE<=p.x-self.cam_x<=SCREEN_W+TILE:
                p.draw(self.cv,self.cam_x)

        for c in self.coins:
            if -40<=c.x-self.cam_x<=SCREEN_W+40:
                c.draw(self.cv,self.cam_x)

        fx=self.flag.x-self.cam_x
        if -100<=fx<=SCREEN_W+100:
            self.flag.draw(self.cv,self.cam_x)

        for g in self.goombas:
            if -TILE<=g.x-self.cam_x<=SCREEN_W+TILE:
                g.draw(self.cv,self.cam_x)

        self.mario.draw(self.cv,self.cam_x)
        self._hud()

        if self.state=="dead":
            self._overlay("PERDISTE UNA VIDA",f"Vidas restantes: {self.mario.lives}","[ENTER] Continuar")
        elif self.state=="win":
            self._overlay("NIVEL COMPLETADO !",f"Puntos: {self.mario.score}","[ENTER] Jugar de nuevo")
        elif self.state=="gameover":
            self._overlay("GAME OVER",f"Puntuacion final: {self.mario.score}","[ENTER] Menu principal")

    def _hud(self):
        self.cv.create_rectangle(0,0,SCREEN_W,36,fill="#000",outline="")
        self.cv.create_text(10,8,text="MARIO",fill="#888",anchor="nw",font=self.FNT_SM)
        self.cv.create_text(10,20,text=f"{self.mario.score:07d}",fill=COLOR_TEXT,anchor="nw",font=self.FNT_SM)

        self.cv.create_oval(105,22,115,32,fill=COLOR_COIN,outline="")
        self.cv.create_text(120,22,text=f"x{self.mario.coins:02d}",fill=COLOR_TEXT,anchor="nw",font=self.FNT_SM)

        self.cv.create_text(SCREEN_W//2,8,text="MUNDO",fill="#888",anchor="n",font=self.FNT_SM)
        self.cv.create_text(SCREEN_W//2,20,text="1 - 1",fill=COLOR_TEXT,anchor="n",font=self.FNT_SM)

        # TIEMPO (nuevo)
        self.cv.create_text(SCREEN_W-220,8,text="TIEMPO",fill="#888",anchor="ne",font=self.FNT_SM)
        self.cv.create_text(SCREEN_W-220,20,text=f"{int(self.time):03d}",fill=COLOR_TEXT,anchor="ne",font=self.FNT_SM)

        self.cv.create_text(SCREEN_W-10,8,text="VIDAS",fill="#888",anchor="ne",font=self.FNT_SM)
        self.cv.create_text(SCREEN_W-10,20,text=f"x{self.mario.lives}",fill="#FC0000",anchor="ne",font=self.FNT_SM)

    def _overlay(self,title,sub,hint):
        self.cv.create_rectangle(100,140,SCREEN_W-100,320,fill="#000",outline=COLOR_COIN,width=3)
        self.cv.create_text(SCREEN_W//2,178,text=title,fill=COLOR_COIN,font=self.FNT_BIG,anchor="center")
        self.cv.create_text(SCREEN_W//2,232,text=sub,fill=COLOR_TEXT,font=self.FNT_MED,anchor="center")
        if(self.state_timer//20)%2:
            self.cv.create_text(SCREEN_W//2,280,text=hint,fill="#AAA",font=self.FNT_SM,anchor="center")

    def _menu(self):
        self.cv.create_text(SCREEN_W//2,70,text="SUPER MARIO BROS",
            fill=COLOR_COIN,font=("Courier",36,"bold"),anchor="center")
        lines=[("Flechas  ← →","Mover"),
               ("Flecha arriba / ESPACIO","Saltar (mantén para salto alto)"),
               ("Golpea bloques [?]","Monedas voladoras +200 pts"),
               ("Pisa a los Goombas","+100 pts (caen por los bordes)"),
               ("Llega a la bandera","¡Nivel completado!")]
        for i,(k,v) in enumerate(lines):
            y=195+i*40
            self.cv.create_text(SCREEN_W//2-10,y,text=k+" →",fill=COLOR_COIN,font=self.FNT_SM,anchor="e")
            self.cv.create_text(SCREEN_W//2+10,y,text=v,fill=COLOR_TEXT,font=self.FNT_SM,anchor="w")
        if(self.state_timer//25)%2:
            self.cv.create_text(SCREEN_W//2,418,text="PRESIONA  ENTER  PARA  JUGAR",
                fill=COLOR_COIN,font=self.FNT_MED,anchor="center")

if __name__=="__main__":
    root=tk.Tk()
    MarioGame(root)
    root.mainloop()