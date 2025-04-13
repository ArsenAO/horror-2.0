import pygame
import random
import sys
import time
import json
import math
pygame.init()
print("lol")
w = pygame.display.set_mode((1000,665))
testSave = {
    "money":0
}
save = None
try:
    with open('Save.json', 'r') as file:
        save = json.load(file)
except:
    with open('Save.json', 'w') as file:
        json.dump(testSave, file)
cl = pygame.time.Clock()
menuFon = pygame.transform.scale(pygame.image.load("image/menu.jpg"), (1000, 665))
classicFon = pygame.transform.scale(pygame.image.load("image/classicFon.jpg"), (1000, 665))
pygame.display.update()
pygame.mixer.init()
sound_day = pygame.mixer.Sound("music/day.mp3")
sound_night = pygame.mixer.Sound("music/night.mp3")
sound_day.set_volume(0.3) 
sound_night.set_volume(0.3) 
pygame.font.init()
w.blit( menuFon,(0,0))
globalRect = pygame.Rect(0, 0, 0, 0)
menuZones=True
clasicZone = False
class HitBox():
    global globalRect
    global puli
    
    def __init__(self, images, x,y,width,height,angle = 90):
        self.rect = pygame.Rect(x,y,width,height)
        self.x1 =x
        self.y1 = y
        self.x2 = self.x1 + globalRect.x
        self.y2 = self.x1 + globalRect.y
        self.image= pygame.image.load(images)
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
    def paint(self):
        self.rect.x =self.x1
        self.rect.y = self.y1
        self.x2 = self.x1 + globalRect.x
        self.y2 = self.y1 + globalRect.y
        w.blit(self.image,(self.x2,self.y2))
    def paint_indickator(self):
        w.blit(self.image, (self.x1,self.y1))
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
class Wall(pygame.sprite.Sprite):
    def __init__(self, color_1,color_2,color_3, x, y, w,h, durability):
        super().__init__()
        self.x1 =x
        self.y1 = y
        self.x2 = self.x1 + globalRect.x
        self.y2 = self.x1 + globalRect.y
        self.width = w
        self.height = h
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.durability = durability
    def draw_wall(self):
        global globalRect
        self.x2 = self.x1 + globalRect.x
        self.y2 = self.y1 + globalRect.y
        w.blit(self.image, (self.x2, self.y2))
    def draw_tma(self):
        self.rect.x =self.x1
        self.rect.y =self.y1
        w.blit(self.image, (self.rect.x, self.rect.y))
class Player(HitBox):
    def __init__(self, images, x,y,width,height,hp,hunger, thirst,reason, money, angle = 90):
        super().__init__(images, x, y, width, height, angle)
        self.navigator = "down"
        self.money = money
        self.hp = hp
        self.hunger = hunger
        self.thirst = thirst
        self.reason = reason
        self.hungerWait = 240
        self.thirstWait = 185
        self.deadWait = 10
        self.damageWait = 120
    def walk(self, l, w, u, d, shift, puli):
        global globalRect
        
        if self.hp > 0:
            if shift and self.hunger >= 50 and self.thirst >= 45:
                if l:
                    globalRect.x +=20
                if r:
                    globalRect.x -=20
                if u:
                    globalRect.y +=20
                if d:
                    globalRect.y -=20
                for pula in puli:
                    if l:
                        pula.pos +=pygame.Vector2(40,0)
                    if r:
                        pula.pos -= pygame.Vector2(40,0)
                    if u:
                        pula.pos +=pygame.Vector2(0,40)
                    if d:
                        pula.pos -=pygame.Vector2(0,40)
            else:
                if l:
                    globalRect.x += 10
                if r:
                    globalRect.x -=10
                if u:
                    globalRect.y +=10
                if d:
                    globalRect.y -=10
                for pula in puli:
                    if l:
                        pula.pos +=pygame.Vector2(20,0)
                    if r:
                        pula.pos -=pygame.Vector2(20,0)
                    if u:
                        pula.pos +=pygame.Vector2(0,20)
                    if d:
                        pula.pos -=pygame.Vector2(0,20)
    def life(self, shift, l, w, d, u, puli):
        if self.hungerWait <= 0:
            if self.hunger > 0:
                self.hunger -=1
                self.hungerWait = 240
        elif self.hungerWait > 0:
            if shift and (l or r or d or u):
                self.hungerWait -= 3
            else:
                self.hungerWait -= 1
        if self.thirstWait <= 0:
            if self.thirst > 0:
                self.thirst -=1
                self.thirstWait = 240
        elif self.thirstWait > 0:
            if shift and (l or r or d or u):
                self.thirstWait -= 3
            else:
                self.thirstWait -= 1
        if self.thirst <= 0:
            self.deadWait -= 1
            if self.deadWait < 0:
                self.hp -= 1
                self.deadWait = 10
        if self.hunger <= 0:
            self.deadWait -= 1
            if self.deadWait < 0:
                self.hp -= 1
                self.deadWait = 10
        if self.reason <= 0:
            self.deadWait -= 1
            if self.deadWait < 0:
                self.hp -= 1
                self.deadWait = 10
        self.walk(l, w, u, d, shift, puli)
        self.paint()
    def paint(self):
        w.blit(self.image,(self.rect.x,self.rect.y))
class Arrow(HitBox):
    def __init__(self, images, x,y,width,height,mouse_pos):
        super().__init__(images, x =x, y =y, width = width, height =height)
        self.naprim = naprim
        self.pos = pygame.Vector2(x,y)
        self.direction = mouse_pos - self.pos
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        self.vel = self.direction  * 35
    def paint(self):
        self.rect.topright = (int(self.pos.x), int(self.pos.y))
        w.blit(self.image,(self.rect.x, self.rect.y)) #(self.rect.x + globalRect.x, self.rect.y + globalRect.y))
    def fire(self):
        self.pos += self.vel
        self.paint()
        
class Photo():
    def __init__(self,price):
        self.price = 'l'
class ItemIn():
    global tma
    global monsters
    global naprim
    global puli
    def __init__(self, index,number, acctive = False):
        self.acctive = acctive
        self.number = number
        self.index = index
        self.rect = pygame.Rect(25 * number, 20, 25, 25)
        if self.index == 0:
            self.imageB = "image/null.png"
            self.durability = 1
        if self.index == 1:
            self.imageB = "image/photoaparat.png"
            self.durability = 100
        if self.index == 20:
            self.imageB = "image/gun.png"
            self.durability = 100
        self.image = pygame.transform.scale(pygame.image.load(self.imageB),(self.rect.width,self.rect.height))
    def obnov(self):
        self.rect.x = self.number* 25
        if self.index == 0:
            self.imageB = "image/null.png"
            self.durability = 1
        if self.index == 1:
            self.imageB = "image/photoaparat.png"
            self.durability = 100
        if self.index == 20:
            self.imageB = "image/gun.png"
            self.durability = 100
        self.image = pygame.transform.scale(pygame.image.load(self.imageB),(self.rect.width,self.rect.height))
    def paint(self):
        w.blit(self.image, (self.rect.x, self.rect.y))    
    def function(self, player, mouse):
        if self.index == 1:
            photo = Photo(0)
            for monster in monsters:
                for ten in tma:
                    if naprim == "up":
                        if monster.rect.y >= player.rect.y and monster.rect.y <= player.rect.y + 75 and monster.rect.x > player.rect.x - 50 and monster.rect.x < player.rect.x + 50:
                            photo.price += 10
                    elif naprim == "up":
                        if monster.rect.y >= player.rect.y and monster.rect.y <= player.rect.y + 75 and monster.rect.x > player.rect.x - 50 and monster.rect.x < player.rect.x + 50:
                            photo.price += 10
                    elif naprim == "up":
                        if monster.rect.y >= player.rect.y and monster.rect.y <= player.rect.y + 75 and monster.rect.x > player.rect.x - 50 and monster.rect.x < player.rect.x + 50:
                            photo.price += 10
                    elif naprim == "up":
                        if monster.rect.y >= player.rect.y and monster.rect.y <= player.rect.y + 75 and monster.rect.x > player.rect.x - 50 and monster.rect.x < player.rect.x + 50:
                            photo.price += 10
                            player.money += 10
                            print("L")
        if self.index == 10:
            for monster in monsters:
                if naprim == "up":
                    if monster.rect.y >= player.rect.y and monster.rect.y <= player.rect.y + 35 and monster.rect.x > player.rect.x - 20 and monster.rect.x < player.rect.x + 20:
                        monster.hp -= 10
                elif naprim == "down":
                    if monster.rect.y <= player.rect.y and monster.rect.y <= player.rect.y + 35 and monster.rect.x > player.rect.x - 20 and monster.rect.x < player.rect.x + 20:
                        monster.hp -= 10
                elif naprim == "right":
                    if monster.rect.x >= player.rect.x and monster.rect.x <= player.rect.x + 35 and monster.rect.y > player.rect.y - 20 and monster.rect.y < player.rect.y + 20:
                        monster.hp -= 10
                elif naprim == "left":
                    if monster.rect.x >= player.rect.x and monster.rect.x <= player.rect.x + 35 and monster.rect.y > player.rect.y - 20 and monster.rect.y < player.rect.y + 20:
                        monster.hp -= 10
        if self.index == 20:
            pula = Arrow("image/pula.png",player.rect.x,player.rect.y,15,15, mouse)
            puli.append(pula)

        
class Monster(HitBox):
    def __init__(self, images, width,height,hp, attack,angle = 90):
        
        navigator = random.randint(1,4)
        self.x1 = random.randint(-100, 1100)
        self.y1 = random.randint(-100, 765)
        if navigator == 1:
            self.x1 = 1100
        elif navigator == 2:
            self.x1 = -300
        elif navigator == 3:
            self.y1 = -300
        elif navigator == 4:
            self.y1 =765
        self.rect = pygame.Rect(self.x1,self.y1,width,height)
        self.image= pygame.image.load(images)
        self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        self.hp = hp
        self.attack = attack
        self.angry = random.randint(0,10)
        self.wallBoll = False
        self.waitAttack = 150
        self.waitDead = 120
        self.waitAnimwalk = 120
        self.waitAnimAttack = 120
        self.current_frameWalk = 0
    def walk(self, player_rect, house):
        if (math.sqrt((self.rect.y - player_rect.y) ** 2 + (self.rect.x-player_rect.x) ** 2) > 200) and (((self.hp > 7 and self.angry == 10)or (self.hp > 20 and self.angry > 7)) or self.hp > 50):
            if self.rect.x < (house.rect.x + globalRect.x + house.rect.width/2):
                self.x1 += 10
                self.wallBoll = True
            elif self.rect.x > (house.rect.x + globalRect.x + house.rect.width/2):
                self.x1 -=10
                self.wallBoll = True
            if self.rect.y > (house.rect.y + globalRect.y + house.rect.height/2):
                self.y1 -= 10
                self.wallBoll = True
            if self.rect.y < (house.rect.y + globalRect.y + house.rect.height/2):
                self.y1 += 10
                self.wallBoll = True
        elif (math.sqrt((self.rect.y - player_rect.y) ** 2 + (self.rect.x-player_rect.x) ** 2) < 200) and ((self.hp > 7 and self.angry > 7) or (self.hp > 20 and self.angry > 3) or (self.hp > 50)):
            if self.rect.x < player_rect.x:
                self.x1 += 10
                self.wallBoll = True
            elif self.rect.x > player_rect.x:
                self.x1 -=10
                self.wallBoll = True
            elif self.rect.y > player_rect.y:
                self.y1 -= 10
                self.wallBoll = True
            elif self.rect.y < player_rect.y:
                self.y1 += 10
                self.wallBoll = True
        else:
            if math.sqrt((self.rect.y - player_rect.y) ** 2 + (self.rect.x-player_rect.x) ** 2) < 150:
                if self.rect.x < player_rect.x:
                    self.x1 -= 10
                    self.wallBoll = True
                elif self.rect.x > player_rect.x:
                    self.x1 +=10
                    self.wallBoll = True
                if self.rect.y > player_rect.y:
                    self.y1 += 10
                    self.wallBoll = True
                if self.rect.y < player_rect.y:
                    self.y1 -= 10
                    self.wallBoll = True
            elif math.sqrt((self.rect.y - (globalRect.x + house.x1)) ** 2 + (self.rect.x-(globalRect.y + house.y1)) ** 2) < 150:
                if self.rect.x < (house.rect.x + globalRect.x + house.rect.width/2):
                    self.x1 -= 10
                    self.wallBoll = True
                elif self.rect.x > (house.rect.x + globalRect.x + house.rect.width/2):
                    self.x1 +=10
                    self.wallBoll = True
                if self.rect.y > (house.rect.y + globalRect.y + house.rect.height/2):
                    self.y1 += 10
                    self.wallBoll = True
                if self.rect.y < (house.rect.y + globalRect.y + house.rect.height/2):
                    self.y1 -= 10
                    self.wallBoll = True
            else:
                self.wallBoll = False
    def life(self, player_rect, house):
        self.walk(player_rect,house)
        if self.hp <= 0:
            self.waitDead -= 1
        self.paint()
house = Wall(233, 150, 122, 250, 132, 500, 350, 100)
wallM = []
wallHouse = Wall(255,160,122, 218, 100, 564, 32, 200)
wallM.append(wallHouse)
wallHouse = Wall(255,160,122, 218, 132, 32, 350, 200)
wallM.append(wallHouse)
wallHouse = Wall(255,160,122, 218, 450, 564, 32, 200)
wallM.append(wallHouse) 
wallHouse = Wall(255,160,122, 750, 100, 32, 350, 200)
wallM.append(wallHouse)
startNewB = HitBox("image/startB.jpg", 400, 257, 200,50)
startConB = HitBox("image/startB.jpg", 400, 357, 200,50)
player = Player("image/player.png", 490, 315.82,20,32.36,100,100,100,100,0)
shift, l,r,u,d = False, False, False, False, False
naprim = "down"
inventory = HitBox("image/inventory.png", 0, 0, 250, 75)
inventoryMas = []
for i in range(10):
    inventory_cells = ItemIn(0,i)
    inventoryMas.append(inventory_cells)
inventoryMas[0].index = 1
inventoryMas[0].acctive = True
inventoryMas[1].index = 20
inventoryNum = 0
tma = []
monsters = []
#time = 21600
time = 0
#monsterTime = 6400
monsterTime = 0
puli = []

a=0
b=0
for cell in inventoryMas:
    cell.obnov()
sound_night.play(loops=-1)
while 1:
    
    temniyKvadrat = Wall(0,0,0, a*52, b*52, 52,52, 0)
    tma.append(temniyKvadrat)
    a +=1
    if a > 19:
        b += 1
        a = 0
    if b == 15:
        break
stenka2 = 0
while True:
    
    while menuZones:
        w.blit( menuFon,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuZones = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startNewB.is_clicked(pygame.mouse.get_pos()):
                    classicZone = True
                    menuZones = False
                    with open('Save.json', 'w') as file:
                        json.dump(testSave, file)
                if startConB.is_clicked(pygame.mouse.get_pos()):
                    classicZone = True
                    menuZones = False
        startNewB.paint()
        startConB.paint()
        cl.tick(40)
        pygame.display.update()
    while classicZone:
        #print(globalRect)
        w.fill((0, 0, 0))  
        camera_x = player.rect.x - 1000 // 2
        camera_y = player.rect.y - 665 // 2
        w.blit(classicFon,(camera_x,camera_y))
        #player.rect = player.image.get_rect(center=(1000 // 2, 665 // 2))
        w.blit(player.image, player.rect)
        if time >57600:
            time =0
        else:
            time += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                classicZone = False
            if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        l = True
                        naprim == "left"
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        r = True
                        naprim == "right"
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        d = True
                        naprim == "down"
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        u = True
                        naprim == "up"
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        shift = True
                    if event.key == pygame.K_1:
                        inventoryNum = 1
                    if event.key == pygame.K_2:
                        inventoryNum = 2
                    if event.key == pygame.K_3:
                        inventoryNum = 3
                    if event.key == pygame.K_4:
                        inventoryNum = 4
                    if event.key == pygame.K_5:
                        inventoryNum = 5
                    if event.key == pygame.K_6:
                        inventoryNum = 6
                    if event.key == pygame.K_7:
                        inventoryNum = 7
                    if event.key == pygame.K_8:
                        inventoryNum = 8
                    if event.key == pygame.K_9:
                        inventoryNum = 9
                    if event.key == pygame.K_0:
                        inventoryNum = 10
                    if event.key == pygame.K_ESCAPE:
                        menuZones = True
                        clasicZone = False

            if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        l = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        r = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        d = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w: 
                        u = False
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        shift = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                for cell in inventoryMas:
                    if cell.acctive == True:
                        cell.function(player, mouse_pos)
                
        house.draw_wall()
        #print(player.rect, globalRect, player.rect.union(globalRect))
        for monster in monsters:
            for pula in puli:
                if monster.rect.colliderect(pula.rect):
                    monster.hp -= 10
                    puli.remove(pula)
            if monster.rect.colliderect(player.rect.union(globalRect)):
                if player.damageWait == 0:
                    player.hp -= monster.attack
                    
                    player.damageWait =120
                else:
                    player.damageWait -= 1
            for wall in wallM:
                if monster.rect.colliderect(wall.rect):
                    if monster.waitAttack <= 0:
                        wall.durability -= monster.attack
                    else:
                        monster.waitAttack -= 1
        for pula in puli:
            pula.fire()
            if pula.rect.x < -1100+ globalRect.x  or pula.rect.x > 1100 + globalRect.x or pula.rect.y > 765 + globalRect.y  or pula.rect.y < -765 + globalRect.y :
                puli.remove(pula)
               # print(pula.rect)
        for monster in monsters:
            if monster.hp <= 0:
                monsters.remove(monster)
            monster.life(player.rect,house)
        
        for stenka in wallM:
            if stenka.rect.colliderect(player.rect.union(globalRect)):
                if (player.rect.bottom > stenka.rect.top and player.rect.top < stenka.rect.top):
                    globalRect.y -= 10
                elif (player.rect.top < stenka.rect.bottom and player.rect.bottom > stenka.rect.bottom):
                    globalRect.y += 10
                elif (player.rect.right > stenka.rect.left and player.rect.left < stenka.rect.left):
                    globalRect.x -=10
                elif (player.rect.left < stenka.rect.right and player.rect.right > stenka.rect.right):
                    globalRect.x +=10
            for monster in monsters:
                if monster.rect.colliderect(stenka):
                    if (monster.rect.bottom > stenka.rect.top and monster.rect.top < stenka.rect.top):
                        monster.y1 -= 10
                    elif (monster.rect.top < stenka.rect.bottom and monster.rect.bottom > stenka.rect.bottom):
                        monster.y1 += 10
                    elif (monster.rect.right > stenka.rect.left and monster.rect.left < stenka.rect.left):
                        monster.x1 -=10
                    elif (monster.rect.left < stenka.rect.right and monster.rect.right > stenka.rect.right):
                        monster.x1 +=10
                print(monster.rect.width,monster.rect.height)
        for wall in wallM:
            if wall.durability <=0:
                wallM.remove(wall)
            wall.draw_wall()
        player.life(shift, l, w, d, u, puli)
        for teni in tma:
            
           
            
            if time >= 52800 or time < 9600:
                teni.image.set_alpha(250)
                if monsterTime <= 0:
                    for i in range(random.randint(1,4)):
                        monster = Monster("image/monster.png",70, 70, 100, random.randint(6, 13))
                        monsters.append(monster)
                    monsterTime = random.randint(19200,19200)
                else:
                    #print(monsterTime)
                    monsterTime -= 1
            elif (time >= 9600 and time < 21600) or(time >= 43200 and time < 52800):
                teni.image.set_alpha(70)
            elif time >= 21600 and time < 43200:
                teni.image.set_alpha(0)
            elif time == 21600:
                sound_night.stop()
                sound_day.play(loops=-1)
            elif time == 43200:
                sound_day.stop()
                sound_night.play(loops=-1)
            
            tmaRast = math.sqrt((teni.rect.x - (house.x2 + house.width/2)) ** 2 +  (teni.rect.y - (house.y2 + house.height/2)  ) ** 2)
            if (tmaRast<= 300) and (tmaRast >= -300):
                teni.image.set_alpha(0)
            elif (tmaRast > 300 and tmaRast <= 370) or (tmaRast < -300 and tmaRast >= -370):
                teni.image.set_alpha(50)
            elif (tmaRast > -370 and tmaRast <= 450) or (tmaRast < -370 and tmaRast >= -450):
                teni.image.set_alpha(150)
            elif (tmaRast > 450) or (tmaRast < -450):
                teni.image.set_alpha(255)
            print(tmaRast)
            teni.draw_tma()
        for cell in inventoryMas:
            cell.acctive= False
        if inventoryNum == 1:
            inventoryMas[0].acctive = True
        elif inventoryNum == 2:
            inventoryMas[1].acctive = True
        elif inventoryNum == 3:
            inventoryMas[2].acctive = True
        elif inventoryNum == 4:
            inventoryMas[3].acctive = True
        elif inventoryNum == 5:
            inventoryMas[4].acctive = True
        elif inventoryNum == 6:
            inventoryMas[5].acctive = True
        elif inventoryNum == 7:
            inventoryMas[6].acctive = True
        elif inventoryNum == 8:
            inventoryMas[7].acctive = True
        elif inventoryNum == 9:
            inventoryMas[8].acctive = True
        elif inventoryNum == 10:
            inventoryMas[9].acctive = True
        inventory.paint_indickator()
        for cell in inventoryMas:
            cell.paint()
        
        cl.tick(40)
        pygame.display.update()
    if menuZones == False and clasicZone == False:
        break