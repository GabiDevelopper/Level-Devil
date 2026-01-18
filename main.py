import pyxel as px
import time

WIDTH = 1000
HEIGHT = 600
TITLE = "Level Devil"
FPS = 60

class Game:
    def __init__(self):
        self.mode = "jeu" #jeu ou constructeur
        self.constructeur_speed = 1.0

        self.xplayer, self.yplayer = 130, 418
        self.PLAYER_W, self.PLAYER_H = 16, 32
        self.speed = 2
        self.level = 1
        
        self.SOLIDES = [(0, 0)]

        #self.porte = [(32, 0), (48, 0), (32, 16), (48, 16)]
        self.coordonnes_portes = [(800, 416), (800, 416), (480, 200), (WIDTH, HEIGHT)]

        self.vy = 0  
        self.gravity = 0.4 #0.4      
        self.jump_strength = -7 #-7 
        self.on_ground = True

        self.direction = "droit" #droit, gauche ou neutre
        self.animation_numero = [0, 0] #Numero image/ numero frame

        self.pics_vy = 0
        self.pics_gravity = 0.4
        self.pics_jump_strength = -8
        self.pics_on_ground = True

        self.tilemaplvl = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.traplvl1 = False
        self.rect_anim_lvl1_y = 448
        self.trap1lvl3 = False
        self.rect1_anim_lvl3_y = 448

        self.trap2lvl3 = False
        self.trap2lvl3_x, self.trap2lvl3_y = 260, 448

        self.trap3lvl3 = False
        self.trap3lvl3_x, self.trap3lvl3_y = 900, 432


        self.pics_lvl2 = [
            {"x": 350, "y": 432, "vy": 0, "on_ground": True},
            {"x": 450, "y": 432, "vy": 0, "on_ground": True},
            {"x": 550, "y": 432, "vy": 0, "on_ground": True}
        ]

        self.pics_lvl3 = [
            {"x": 530, "y": 216},
            {"x": 644, "y": 216},
        ]

        self.pics_lvl4 = [
            {"x": 450, "y": 432}
        ]


        px.init(width=WIDTH, height=HEIGHT, title=TITLE, fps=FPS)
        px.colors[4] = 0x996b07
        px.colors[13] = 0xc8c8c8
        px.colors[15] = 0xfeb854
        px.load("assets.pyxres")
        px.run(self.update, self.draw)

    def reinitialiser(self):
        self.xplayer, self.yplayer = 130, 418
        self.speed = 2
        
        self.vy = 0  
        self.gravity = 0.4 #0.4      
        self.jump_strength = -7 #-7 
        self.on_ground = True

        self.pics_vy = 0
        self.pics_gravity = 0.4
        self.pics_jump_strength = -8
        self.pics_on_ground = True

        self.tilemaplvl = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.traplvl1 = False
        self.rect_anim_lvl1_y = 448
        self.trap1lvl3 = False
        self.rect1_anim_lvl3_y = 448
        self.trap2lvl3 = False
        self.trap2lvl3_x, self.trap2lvl3_y = 260, 448
        self.trap3lvl3 = False
        self.trap3lvl3_x, self.trap3lvl3_y = 900, 432

    def level_up(self):
        if self.level < 4:
            self.level_screen()
            self.reinitialiser()
            self.level += 1

    def level_screen(self):
        px.cls(13)
        px.bltm(0, 0, 7, 0, 0, px.width, px.height)
        px.flip()  # forcer l'affichage immédiat
        time.sleep(3)

    def collision_bas(self, x, y):
        return (
            self.est_solide(x + 1, y + self.PLAYER_H) or
            self.est_solide(x + self.PLAYER_W - 2, y + self.PLAYER_H)
        )
    def collision_haut(self, x, y):
        return (
            self.est_solide(x + 1, y - 1) or
            self.est_solide(x + self.PLAYER_W - 2, y - 1)
        )
    def collision_gauche(self, x, y):
        return (
            self.est_solide(x - 1, y + 1) or
            self.est_solide(x - 1, y + self.PLAYER_H - 2)
        )
    def collision_droite(self, x, y):
        return (
            self.est_solide(x + self.PLAYER_W, y + 1) or
            self.est_solide(x + self.PLAYER_W, y + self.PLAYER_H - 2)
        )

    def est_solide(self, x, y):
        TILE = 8

        world_x = x + self.tilemaplvl[self.level-1][0]
        world_y = y + self.tilemaplvl[self.level-1][1]

        tile_x = world_x // TILE
        tile_y = world_y // TILE

        tm = px.tilemaps[self.level - 1]

        if tile_x < 0 or tile_y < 0 or tile_x >= tm.width or tile_y >= tm.height:
            return True

        tile = tm.pget(tile_x, tile_y)
        return tile in self.SOLIDES
    
    def collision_joueur_pics(self, spikes):
        # Rectangle du joueur
        player_left   = self.xplayer +3
        player_right  = self.xplayer + self.PLAYER_W -5
        player_top    = self.yplayer +4
        player_bottom = self.yplayer + self.PLAYER_H -4

        SPIKE_W = 32
        SPIKE_H = 16

        for pic in spikes:
            spike_x = pic["x"]
            spike_y = pic["y"]

            # Rectangle du pic
            spike_left   = spike_x +6
            spike_right  = spike_x + SPIKE_W -5 #bordure dessin
            spike_top    = spike_y +8
            spike_bottom = spike_y + SPIKE_H #bordure dessin

            # collision
            if (player_right > spike_left and
                player_left < spike_right and
                player_bottom > spike_top and
                player_top < spike_bottom):
                return True
        return False

    
    def est_mortel(self, x, y):
        if self.level == 2:
            pass
    
    def dans_porte(self):
        xp, yp = self.xplayer, self.yplayer
        pw, ph = self.PLAYER_W, self.PLAYER_H

        dx, dy = self.coordonnes_portes[self.level - 1]

        return (
            xp < dx + 32 and
            xp + pw > dx and
            yp < dy + 32 and  #32 -> taille de la porte
            yp + ph > dy
        )


    def update(self):
        if px.btnp(px.KEY_M):
            if self.mode == "jeu":
                self.mode = "constructeur"
            else:
                self.mode = "jeu"

        if px.btnp(px.KEY_I):
            print(self.xplayer, self.yplayer, self.constructeur_speed)

        if self.mode == "jeu":
            if px.btnp(px.KEY_UP) and self.on_ground and not self.level == 2:
                self.vy = self.jump_strength
                self.on_ground = False

            if px.btn(px.KEY_LEFT) and not self.collision_gauche(self.xplayer, self.yplayer):
                self.direction = "gauche"
                self.xplayer -= self.speed

            if px.btn(px.KEY_RIGHT) and not self.collision_droite(self.xplayer, self.yplayer):
                self.direction = "droite"
                self.xplayer += self.speed

            if not self.on_ground:
                self.vy += self.gravity
                self.yplayer += self.vy

            #saut pics
            if self.level == 2:
                for pic in self.pics_lvl2:
                    # saut
                    if px.btnp(px.KEY_UP) and pic["on_ground"]:
                        pic["vy"] = self.pics_jump_strength
                        pic["on_ground"] = False
                    # gravité
                    if not pic["on_ground"]:
                        pic["vy"] += self.pics_gravity
                        pic["y"] += pic["vy"]
                        # sol
                        if pic["y"] >= 432:
                            pic["y"] = 432
                            pic["vy"] = 0
                            pic["on_ground"] = True

            #activer pieges lvl 3
            if self.level == 3:
                if self.xplayer >= 150 and not self.trap1lvl3:
                    self.trap1lvl3 = True
                    self.tilemaplvl[2][0] = px.width+24
                if self.trap1lvl3 and self.rect1_anim_lvl3_y < px.height:
                    self.rect1_anim_lvl3_y += 4

                if self.xplayer >= 230:
                    self.trap2lvl3 = True
                #animation monter pic
                if self.trap2lvl3 and self.trap2lvl3_y > 432:
                    self.trap2lvl3_y -= 1

            #detection sol
            if self.collision_bas(self.xplayer, self.yplayer):
                self.yplayer = (self.yplayer // 8) * 8
                self.vy = 0
                self.on_ground = True
            else:
                self.on_ground = False

            #activer piege lvl 1
            if self.level == 1 and self.xplayer >= 578 and not self.traplvl1:
                self.traplvl1 = True
                self.tilemaplvl[0][0] = px.width+24

            #animation rectangle lvl 1
            if self.level == 1 and self.traplvl1 and self.rect_anim_lvl1_y < px.height:
                self.rect_anim_lvl1_y += 4

            #chute player lvl 1 et lvl 3
            if self.level in (1, 3) and self.yplayer >= px.height-self.PLAYER_H:
                self.reinitialiser()

            #detection porte
            if self.dans_porte():
                self.level_up()

            #detection pics
            if self.level == 2 and self.collision_joueur_pics(self.pics_lvl2):
                self.reinitialiser()

            #declenchement piege 3 lvl 3
            if self.level == 3 and self.xplayer >= 400 and not self.trap3lvl3:
                self.trap3lvl3 = True
            #avancer piege 3 lvl 3
            if self.level == 3 and self.trap3lvl3:
                if self.trap3lvl3_x > 325:
                    self.trap3lvl3_x -= self.speed + 5
                else:
                    if self.trap3lvl3_y < 500:
                        self.trap3lvl3_y += self.speed
            #Detections pieges lvl 3
            if self.level == 3:
                if (self.collision_joueur_pics([{"x":self.trap2lvl3_x, "y":self.trap2lvl3_y}])
                 or self.collision_joueur_pics([{"x":self.trap3lvl3_x, "y":self.trap3lvl3_y}])
                 or self.collision_joueur_pics(self.pics_lvl3)):
                    self.reinitialiser()

            if self.level == 4:
                if (self.collision_joueur_pics(self.pics_lvl4)
                    or self.collision_joueur_pics([{"x": 183, "y": 140}])):
                    self.reinitialiser()
                

            #animation
            self.animation_numero[1] += 1
            if self.animation_numero[1] >= FPS/8:
                self.animation_numero[0] += 1
                self.animation_numero[1] = 0


        if self.mode == "constructeur":
            if px.btnp(px.KEY_Z):
                if self.constructeur_speed < 3:
                    self.constructeur_speed += 0.2
            if px.btnp(px.KEY_S):
                if self.constructeur_speed > 1:
                    self.constructeur_speed -= 0.2    

            if px.btn(px.KEY_UP):
                self.yplayer -= self.speed*self.constructeur_speed
            if px.btn(px.KEY_DOWN):
                self.yplayer += self.speed*self.constructeur_speed 
            if px.btn(px.KEY_LEFT):
                self.xplayer -= self.speed*self.constructeur_speed
            if px.btn(px.KEY_RIGHT):
                self.xplayer += self.speed*self.constructeur_speed
        

    def draw(self):
        px.cls(15)
        #Niveau
        px.bltm(0, 0, self.level-1, self.tilemaplvl[self.level-1][0], self.tilemaplvl[self.level-1][1], px.width, px.height)
        #Porte
        px.blt(self.coordonnes_portes[self.level-1][0], self.coordonnes_portes[self.level-1][1], 0, 32, 0, 16, 16, colkey=15)
        px.blt(self.coordonnes_portes[self.level-1][0], self.coordonnes_portes[self.level-1][1]+16, 0, 32, 16, 16, 16, colkey=15)
        px.blt(self.coordonnes_portes[self.level-1][0]+16, self.coordonnes_portes[self.level-1][1], 0, 48, 0, 16, 16, colkey=15)
        px.blt(self.coordonnes_portes[self.level-1][0]+16, self.coordonnes_portes[self.level-1][1]+16, 0, 48, 16, 16, 16, colkey=15)
        #Joueur
        if self.mode == "jeu":
            if self.on_ground and self.direction == "neutre":
                px.blt(self.xplayer, self.yplayer, 0, 16, 0, 16, 16, colkey=15)
                px.blt(self.xplayer, self.yplayer, 0, 16, 0, 16, 32, colkey=15)
            elif self.on_ground and self.direction == "droite":
                if self.animation_numero[0] == 0:
                    px.blt(self.xplayer, self.yplayer, 0, 0, 48, 16, 32, colkey=15)
                elif self.animation_numero[0] == 1:
                    px.blt(self.xplayer, self.yplayer, 0, 16, 48, 16, 32, colkey=15)
                else:
                    self.animation_numero[0] = 0
                    px.blt(self.xplayer, self.yplayer, 0, 0, 48, 16, 32, colkey=15)
            elif self.on_ground and self.direction == "gauche":
                if self.animation_numero[0] == 0:
                    px.blt(self.xplayer, self.yplayer, 0, 0, 80, 16, 32, colkey=15)
                elif self.animation_numero[0] == 1:
                    px.blt(self.xplayer, self.yplayer, 0, 16, 80, 16, 32, colkey=15)
                else:
                    self.animation_numero[0] = 0
                    px.blt(self.xplayer, self.yplayer, 0, 0, 80, 16, 32, colkey=15)
            else:
                if self.direction == "gauche":
                    px.blt(self.xplayer, self.yplayer, 0, 16, 80, 16, 32, colkey=15)
                else:
                    px.blt(self.xplayer, self.yplayer, 0, 16, 48, 16, 32, colkey=15)
            
        else:
            px.rect(self.xplayer, self.yplayer, 8, 8, 5)

        if self.level == 1:
            #rectangle animation lvl 1
            px.rect(599, self.rect_anim_lvl1_y, 57, px.height, 4)

        elif self.level == 2:
            for pic in self.pics_lvl2:
                #pics
                px.blt(pic["x"], pic["y"], 0, 0, 32, w=32, h=16, colkey=15)
        elif self.level == 3:
            #rectangle 1 animation lvl 3
            px.rect(160, self.rect1_anim_lvl3_y, 57, px.height, 4)

            #Pics
            for pic in self.pics_lvl3:
                px.blt(pic["x"], pic["y"], 0, 0, 32, w=32, h=16, colkey=15)
            
            if self.trap2lvl3:
                #Pic
                px.blt(self.trap2lvl3_x, self.trap2lvl3_y, 0, 0, 32, w=32, h=16, colkey=15)
                px.rect(self.trap2lvl3_x, 448, 32, 32, 4)

            #Roue
            if self.trap3lvl3:
                px.blt(self.trap3lvl3_x, self.trap3lvl3_y, 0, 32, 32, 32, 32, colkey=15)
                px.rect(872, 416, 60, 32, 4)
                px.rect(self.trap3lvl3_x, 448, 32, 100, 4)

        elif self.level == 4:
            for pic in self.pics_lvl4:
                px.blt(pic["x"], pic["y"], 0, 0, 32, w=32, h=16, colkey=15)

            px.blt(183, 140, 0, 32, 32, 32, 32, colkey=15)

            px.text(450, 300, "Vous avez fini le jeu !", 0)

        self.direction = "neutre"

Game()