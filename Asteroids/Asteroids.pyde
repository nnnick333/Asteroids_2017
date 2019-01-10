add_library('minim')
import random
#Used to control game modes
mode = 0
#2D array storing score and player name
scores = []
#variable contraining last key pressed
lk = ''
#variable containing player's entered name
name = ''
#variable used to state whether or not player has entered their name
entered = False
#Class shared amound all objects name moveable
class Moveable():
    def __init__(self,x,y,r,dx,dy,rotation):
        #ATTRIBUTES FOR ALL
        #OBJECTS X COORD
        self.x = x
        #OBJECTS Y COORD
        self.y = y
        #OBJECTS X VELOCITY
        self.dx = dx
        #OBJECTS Y VELOCITY
        self.dy = dy
        #OBJECTS RADIUS
        self.r = r
        #ATTRIBUTES FOR PLAYER
        self.dr = 0
        #PLAYER LAST ROTATION BEFORE THRUST IS OFF
        self.temprotation = -90
        #PLAYERS ENTERED ROTATION VALUE
        self.rotation = rotation
        #PLAYERS ACCELERATION
        self.acceleration = 0
        #PLAYERS TRANSLATION X VALUE
        self.translationx = 0
        #PLAYERS TRANSLATION Y VALUE
        self.translationy = 0
        #PLAYERS SCORE
        self.score = 0
        #PLAYERS LIVES REMAINING
        self.lives = 3
        #PLAYERS THRUST STATE
        self.thrust = 0
        #PLAYERS ROTATION THRUST STATE
        self.rotthrust = 0
        #PLAYERS INVINCIBILITY STATE
        self.playerinv = 0
        #PLAYERS FLICKERING VALUE CONTROLS INVULNERABLITY AND GRAPHICS
        self.flickervalue = 0
        #ATTRIBUTES FOR BULLET
        #BULLET LIFE IS A DECAYING VALUE THAT CAUSES THE BULLET TO DISSAPEAR
        self.bulletlife = 2
        #ATTRIBUTES FOR ASTEROID
        #CONTROLS WHETHER OR NOT AN ASTEROIDS WILL BE DELETED
        self.asteroidlife = True
        #ATTRIBUTES FOR UFO
        #CONTROLS HOW OFTEN A BULLET IS FIRED
        self.ufoshot = 70
        #ATTRIBUTE USED TO CHANGE DIRECTION OF MOVING UFO
        self.ufochangedir = 50
    #CONTROLS MOVEMENT OF OBJECTS
    def move(self):
        #ADDS ROTATION VELOCITY TO ROTATION VALUE
        self.rotation += self.dr
        #RESETS ROTATION VALUE UPON EXCEEDING 360 OR 0
        if self.rotation >= 360:
            self.rotation = 0
        elif self.rotation <= -360:
            self.rotation = 0
        #ADDS X AND Y VELOCITY TO X AND Y
        self.x += self.dx
        self.y += self.dy
        #WRAPPING CODE: IF IT GOES BEYOND SCREEN THEN IT WILL RETURN FROM OPPOSITE SIDE
        if self.x >= 1210-self.translationx:
            self.x = -10-self.translationx
        elif self.x <= -10-self.translationx:
            self.x = 1210-self.translationx
        if self.y >= 810-self.translationy:
            self.y = -10-self.translationy
        elif self.y <= -10-self.translationy:
            self.y = 810-self.translationy
        # IF THRUST IS ON
        if self.thrust == 1:
            #MAX ACC = 4
            if self.acceleration <= 4:
                #AUTOMATICALLY SET ACC TO 1
                if self.acceleration <= 1:
                    self.acceleration = 1.5
                else:
                    #INCREASE IN ACC
                    self.acceleration *= 1.05
        #IF THRUST IS OFF
        if self.thrust == 0:
            #DECREASE IN ACC
            self.acceleration *= 0.985
        #IF BRAKE 'S' IS PRESSED
        if self.thrust == -1:
            #FASTER DECREASED IN ACC
            self.acceleration *= 0.80
        #IF ROTATION THRUST RIGHT IS ON
        if self.rotthrust == 1:
            #MAX DR = 3.5
            if self.dr <= 3.5:
                #IF LESS THAN 1 AUTOMATICALLY 2
                if self.dr <= 1:
                    self.dr = 2
                else:
                    #DR INCREASED CONSTANTLY 
                    self.dr *= 1.1
        #SAME AS ABOVE WITH NEGATIVE VALUES FOR LEFT TURN
        if self.rotthrust == -1:
            if self.dr >= -3.5:
                if self.dr >= -1:
                    self.dr = -2
                else:
                    self.dr *= 1.1
        # IF TURNING IN NEITHER DIRECTION THEN ROTATION VELOCITY CONSTANTLY DECREASED
        if self.rotthrust == 0:
            self.dr *= 0.9
    #METHOD TO CREATE BULLETS BASED ON ROTATION POINT OF THE PLAYER/UFO,PARAMETERS TO DECIDE WHETHER IT IS UFO OR PLAYER
    def create_bullet(self,size,bullettype):
        #SHOOT SOUND
        shoot.play()
        shoot.rewind()
        #CREATES BULLET
        bullet = Bullet(self.translationx + self.x, self.translationy + self.y,size,cos(radians(self.rotation)) * 9,sin(radians(self.rotation)) * 9,0)
        #APPENDS BULLET TO APPROPRIATE LIST
        return bullettype.append(bullet)
    #FIND APPROX DISTANCE BETWEEN THE CENTRE OF TWO OBJECTS
    def get_distance(self,point2):
        distance = sqrt((abs(self.x - point2.x) ** 2) + (abs(self.y - point2.y) ** 2))
        return distance
    #FIND THE SLOPE BETWEEN TWO POINTS(FOR UFO TARGETTING)
    def get_slope(self,point2):
        slope = (self.y - point2.y)/(self.x - point2.x)
        return slope
    #FIND THE ANGLE THAT FROM ONE POINT TO ANOTHER
    def get_angle(self,point2):
        angle = atan(self.get_slope(point2))
        return angle
#NOTE: ALL CLASSES INHERIT MOVEMENT
#NOTE: UFO BULLET RADIUS SLIGHTLY LARGER TO DIFFRENTIATE BETWEEN THE 2 IN CONDITIONAL STATEMENTS
#BULLET CLASS
class Bullet(Moveable):
    #USED TO DETERMINE BULLET LIFETIME
    def bullettime(self):
        #BULLETLIFE ATTRIBUTE CONSTANTLY DECREASED
        self.bulletlife *= 0.99
        #UPON REASON CERTAIN POINT(APPROXIMATELY 600 UNITS) ITS BULLETLIFE VALUE WILL FIT THE CONDITION
        if self.bulletlife <= 0.95:
            #IT IS REMOVED FROM PLAYER LIST
            if self.r == 7:
                bullets.remove(self)
            #IT IS REMOVED FROM UFO BULLET LIST
            elif self.r == 7.01:
                ufo_bullets.remove(self)
#ASTEROID CLASS
class Asteroids(Moveable):
    #METHOD USED TO DETERMINE COLLISION BETWEEN THE ASTEROID AND BULLETS,PLAYER OR UFOS
    #PARAMETER IS ITSELF AND ANOTHER OBJECT
    def asteroid_collision(self, collidable):  
        #IF DISTANCE BETWEEN THE TWO IS SMALLER THAN THE TWO RADIUS COMBINED(+20 BECAUSE EARLY HITBOX DETECTION)
        if (self.get_distance(collidable)+20) <= (self.r + collidable.r):
            #IF LARGE ASTEROID
            if self.r == 70:
                #SPLIT ASTEROID FUNCTION
                break_asteroid(self.x,self.y,50)
                #IF NOT UFO BULLET OR UFO COLLISION
                if collidable.r != 7.01 and collidable.r != 31 and collidable.r != 11.001:
                    #PLAYERS SCORE INCREASES BY 20
                    player.score += 20
            #CODE BELOW FOLLOWS SAME FORMAT AS LARGE ASTEROID COLLISION
            if self.r == 50:
                break_asteroid(self.x,self.y,30)
                if collidable.r != 7.01 and collidable.r != 31 and collidable.r != 11.001:
                    player.score += 50
            #CODE BELOW FOLLOWS SAME FORMAT AS LARGE ASTEROID COLLISION
            if self.r == 30:
                if collidable.r != 7.01 and collidable.r != 31 and collidable.r != 11.001:
                    player.score += 100
            #IF THE COLLIDABLE IS A BULLET THEN REMOVE IT FROM ITS RESPECTIVE LIST
            if collidable.r == 7:
                bullets.remove(collidable)
            if collidable.r == 7.01:
                ufo_bullets.remove(collidable)
            #IF THE COLLIDABLE IS A PLAYER CALL THE METHOD DEATH() TO KILL PLAYER
            elif collidable.r == 11:
                player.death()
            #IF THE COLLIDABLE IS A UFO KILL THE UFO
            elif collidable.r == 31 or collidable.r == 11.001:
                ufo.remove(collidable)
            #CALL METHOD TO FINALLY DESTROY ASTEROID
            self.asteroidlife = False
    #METHOD TO DESTROY ASTEROID
    def asteroiddeath(self):
        #IF DEAD
        if self.asteroidlife == False:
            #PLAY RESPECTIVE EXPLOSION SOUNDS BASED ON ASTEROID SIZE
            if self.r == 70:
                largeex.play()
                largeex.rewind()
            if self.r == 50:
                mediumex.play()
                mediumex.rewind()
            else:
                smallex.play()
                smallex.rewind()
            #THEN REMOVE ASTEROID FROM LIST
            asteroid.remove(self)
#PLAYER CLASS
class Player(Moveable):
    #FLICKER CONTROLS PLAYERS FLICKERING IMAGE WHEN INVLUNERABLE
    def flicker(self):
        #UPON DEATH PLAYERS INV VALUE = 2
        #METHOD ONLY USED WHEN INVULNERABLE
        if self.playerinv != 0:
            self.flickervalue += 0.5
            if self.flickervalue >= 10:
                self.flickervalue = 0
    #INVINCE METHOD 
    def invince(self):
        #UPON DEATH PLAYERS INV VALUE = 2
        if self.playerinv >= 0:
            #PLAYERS INV VALUE BEING CONSTANTLY DECREASED
            self.playerinv *= 0.99
            #AFTER BRIEF TIME PLAYER INV IS SET BACK TO 0 AND THUS VULNERABLE
            if self.playerinv <=0.5:
                self.playerinv = 0
                self.flickervalue = 0
    #ROTATION THRUST MOVEMENT
    def rotmove(self):
        #IF THE PLAYER IS THRUSTING
        if self.thrust == 1:
            #MOVES IN DIRECTION OF ROTATION BASED ON TRIGANOMETRIC MATH
            self.dx = (cos(radians(self.rotation))) * self.acceleration
            self.dy = (sin(radians(self.rotation))) * self.acceleration
        #IF THE PLAYER IS NOT THRUSTING
        if self.thrust != 1:
            #MOVES IN DIRECTION OF ITS LAST ROTATION VALUE BEFORE THRUST TURNED OFF BASED ON TRIGANOMETRIC MATH
            self.dx = (cos(radians(self.temprotation))) * self.acceleration
            self.dy = (sin(radians(self.temprotation))) * self.acceleration
    #NOTE: EXACT SPEED BASED ON ACCELERATION ATTRIBUTE
    #IF THE PLAYER COLLIDES WITH SOMETHING THAT IS NOT AN ASTEROID
    def player_collision(self,collidable):
        #REPEATED COLLISION MATH
        if (self.get_distance(collidable)-10) <= (self.r + collidable.r):
            #PLAYS EXPLOSION FOR PLAYER DEATH
            mediumex.play()
            mediumex.rewind()
            #IF COLLIDABLE IS UFO BULLET IT REMOVES BULLET FROM LIST
            if collidable.r == 7.01:
                ufo_bullets.remove(collidable)
            #IF COLLIDABLE IS UFO IT ADDS 200 POINTS AND REMOVES THE UFO FROM LIST
            elif collidable.r == 31 or collidable.r == 11.001:
                if collidable.r == 31:
                    player.score += 200
                if collidable.r == 11.001:
                    player.score += 1000
                ufo.remove(collidable)
                #IF NO MORE UFOS LEFT IT PAUSES UFO SOUND EFFECTS
            #COLLISION PROMPTS PLAYERS DEATH
            player.death()
    #UPON DYING TO HAS ITS VALUES RESET
    def death(self):
        self.x = 0
        self.y = 0
        self.r = 2
        self.dx = 0
        self.dy = 0
        self.rotation = -90
        player = Player(0,0,2,0,0,-90)
        #LOSES 1 LIFE
        self.lives -= 1
        self.acceleration = 0
        #PLAYER TEMPORARY INVULNERABILITY
        self.playerinv = 2
#UFO CLASS
class UFO(Moveable):
    #METHOD USED TO RANDOMLY CHANGE ROTATION POINT WHICH AFFECTS BULLET DIRECTION
    def change_direction_shot(self):
        #UFOSHOT IS A TIMER ATTRIBUTE THAT CONTROLS WHEN THE NEXT BULLET IS FIRED
        self.ufoshot -= 1
        #WHEN ITS TIME TO FIRE BULLET
        if self.ufoshot <=0:
            #LARGE UFO
            if self.r == 31:
                #RANDOM ROTATION
                self.rotation = random.randint(0,360)
            #SMALL UFO TARGETTING MATH
            if self.r == 11.001:
                #IF PLAYERS X COORD IS GREATER THAN OR EQUAL UFO X COORD
                if player.translationx + player.x >= self.x:
                    #FINDS THE ROTATION ANGLE TO POINT TO PLAYER
                    self.rotation = degrees(self.get_angle(Player(player.translationx + player.x, player.translationy + player.y,11,0,0,0)))
                #IF LESS THAN UFO X COORD
                if player.translationx + player.x < self.x:
                    #SUBRACT 180 DEGREE(THE CALCULATED SLOPE WOULD ONLY ALLOW FOR BULLETS TO BE SHOT IN THE POSITIVE X DIRECTION)
                    #WITHOUT -180 IT WOULD SHOOT IN THE INVERSE DIRECTION OF THE SHIP(EXAMPLE: WHEN PLAYER IS 180 DEGREES IT WOULD SHOOT IN THE DIRECTION OF 0 DEGREES)
                    self.rotation = degrees(self.get_angle(Player(player.translationx + player.x, player.translationy + player.y,11,0,0,0))) - 180
            #CREATES A UFO BULLET
            self.create_bullet(7.01,ufo_bullets)
            #RESETS THE BULLET TIMER
            self.ufoshot = 70
    #IF THE UFO COLLIDES WITH A PLAYER BULLET
    def ufo_collision(self,collidable):
        #COLLISION MATH
        if (self.get_distance(collidable)) <= (self.r + collidable.r):
            #EXPLOSION SOUND
            mediumex.play()
            mediumex.rewind()
            #REMOVE BULLET
            bullets.remove(collidable)
            #REMOVE UFO
            ufo.remove(self)
            #ADD SCORES
            if self.r == 31:
                player.score += 200
            if self.r == 11.001:
                player.score += 1000
    #CODE TO CHANGE THE UFOS MOVEMENT DY VALUE AT RANDOM
    def change_movement(self):
        self.ufochangedir -= 1
        if self.ufochangedir <= 0:
            choice1 = random.randint(0,1)
            if choice1 == 0:
                self.dy = random.uniform(-2,-0.5)
            if choice1 == 1:
                self.dy = random.uniform(0.5,2)
            self.ufochangedir = 50
#FUNCTION TO SPLIT MEDIUM AND LARGE ASTEROIDS                
def break_asteroid(x,y,radius):
    #SPAWNS TO ASTEROIDS AT CENTER OF COLLISION WITH RANDOM VELOCITYS AND THEN APPENDS THEM TO ASTEROID LIST
    asteroid1 = Asteroids(x,y,radius,random.uniform(-2,2),random.uniform(-2,2),0)
    asteroid2 = Asteroids(x,y,radius,random.uniform(-2,2),random.uniform(-2,2),0)
    asteroid.append(asteroid1)
    asteroid.append(asteroid2)
#FUNCTION TO CREATE NEW ASTEROID OUTSIDE SCREEN
def create_asteroid(asteroid):
    #ALL VARIABLES BELOW DECIDE RANDOM ENDS OF SCREEN TO CREATE ASTEROID AND THEN ASSIGNS RANDOM VELOCITYS AS WELL
    choice1 = random.randint(0,1)
    choice2 = random.randint(0,1)
    if choice1 == 0:
        if choice2 == 0:
            x = random.randint(-50,0)
            dx = random.uniform(0.5,1.8)
        if choice2 == 1:
            x = random.randint(1200,1250)
            dx = random.uniform(-1.8,-0.5)
        y = random.randint(0,800)
        dy = random.uniform(-1.1,1.1)
    if choice1 == 1:
        if choice2 == 0:
            y = random.randint(-100,0)
            dy = random.uniform(0.5,1.8)
        if choice2 == 1:
            y = random.randint(800,850)
            dy = random.uniform(-1.8,-0.5)
        x = random.randint(0,1200)
        dx = random.uniform(-1.1,1.1)
    #APPENDS ASTEROID TO LIST
    return asteroid.append(Asteroids(x,y,70,dx,dy,0))
#FUNCTION TO CREATE NEW UFO
def create_UFO(ufo):
    #SPAWNING SYSTEM SIMILAR TO ASTEROIDS
    global ufospawntime
    choice1 = random.randint(0,1)
    small_or_large = random.randint(0,1)
    if choice1 == 0:
        x = random.randint(-50,0)
        dx = random.uniform(1.5,2)
    if choice1 == 1:
        x = random.randint(1200,1250)
        dx = random.uniform(-2,-1.5)
    y = random.randint(0,800)
    #RESETS UFO CREATION TIMER
    ufospawntime = 650
    #SMALL OR LARGE UFO
    if small_or_large == 0:
        r = 31
        #PLAYS UFO SOUND EFFECTS
        ufobig.loop()
    elif small_or_large == 1:
        r = 11.001
        #PLAYS UFO SOUND EFFECTS
        ufosmall.loop()
    #APPENDS NEW UFO TO UFO LIST
    return ufo.append(UFO(x,y,r,dx,0,0))
#FUNCTION TO RESET ALL OBJECTS AND LIST FOR IN-GAME PURPOSES
def reset():
    global player,asteroid,bullets,ufo,ufospawntime,ufo_bullets
    asteroid = []
    bullets = []
    ufo = []
    ufo_bullets = []
    for n in range(5):
        create_asteroid(asteroid)
    player = Player(0,0,11,0,0,-90)
    player.translationx = 600
    player.translationy = 400
    ufospawntime = 650
#CREATE 10 ASTEROIDS AT START OF GAME
asteroid = []
for n in range(5):
    create_asteroid(asteroid)
#SETUP
def setup():
    global shoot,minim,thrust,smallex,mediumex,largeex,beat,high_scores,ufobig,ufosmall
    size(1200,800)
    #MINIM USED FOR SOUNDS
    minim = Minim(this)
    #SHOT SOUND
    shoot = minim.loadFile("fire.wav")
    #SMALL EXPLOSION SOUND
    smallex = minim.loadFile("bangSmall.wav")
    #MEDIUM EXPLOSION SOUND
    mediumex = minim.loadFile("bangMedium.wav")
    #LARGE EXPLOSION SOUND
    largeex = minim.loadFile("bangLarge.wav")
    #BEATING BACKGROUND SOUND
    beat = minim.loadFile("Beater.wav")
    #SOUND FOR LARGE UFO
    ufobig = minim.loadFile("saucerBig.wav")
    #SOUND FOR UFO SMALL
    ufosmall = minim.loadFile("saucerSmall.wav")
    #TEMP LISTS USED TO READ HIGH SCORES FROM FILES
    temp_all = []
    temp_scores = []
    temp_names = []
    #APPENDS THE NAMES AND SCORES FROM FILE TO TEMP_ALL
    with open("scores.txt", "r") as in_score:
        for line in in_score:
            temp_all.append(line)
    list_length = len(temp_all)
    #PLACES NAMES IN TEMP_SCORES AND TURNS SCORES INTO INTS AND PLACES THEM INTO TEMP_SCORES
    for n in range(list_length):
        if n % 2 == 0:
            temp_scores.append(int(temp_all[n]))
        else:
            temp_names.append(temp_all[n])
    #COMBINES TEMP_NAMES AND TEMP_SCORES AND CREATES 2D ARRAY WITH HIGHSCORES ASSOCIATED WITH PLAYER NAME
    for n in range(list_length/2):
        temp = []
        temp.append(temp_scores[n])
        temp.append(temp_names[n])
        scores.append(temp)
    #CONVERT MOST RECENT PLAYER SCORES INTO HIGH SCORES USING SORTING
    if len (scores) >= 1:
        high_scores = (sorted(scores,key=lambda l:l[0], reverse=True))
#DRAW
def draw():
    global mode,score,name,ufospawntime,asteroids
    #BLACK BACKGROUND
    background(0)
    strokeWeight(2)
    fill(0)
    #DRAWS ASTEROIDS IN ALL MODES OF GAME
    for a in asteroid:
            a.move()
            ellipse(a.x,a.y,a.r,a.r)
    fill(255)
    #TITLE SCREEN
    if mode == 0:
        #TEXT AND TEXT BOXES
        textSize(80)
        text("ASTEROIDS",390,200)
        fill (0)
        stroke (255)
        rect(440,300,300,70)
        rect(420,405,350,70)
        fill (255)
        textSize(50)
        text("PLAY GAME",450,355)
        text("HIGH SCORES",430,455)
        textSize(40)
        text("Recent Players:",455,520)
        textSize(35)
        text("Controls:",15,45)
        #DISPLAYING RECENT PLAYERS
        if len (scores) >= 1:
            text(scores[-1][1],425,570)
            text(scores[-1][0],705,570)
        if len (scores) >= 2:
            text(scores[-2][1],425,610)
            text(scores[-2][0],705,610)
        if len (scores) >= 3:
            text(scores[-3][1],425,650)
            text(scores[-3][0],705,650)
        if len (scores) >= 4:
            text(scores[-4][1],425,690)
            text(scores[-4][0],705,690)
        textSize(20)
        #CONTROLS
        text("W or UP ARROW = Thrust",15,85)
        text("S or DOWN ARROW = Brake",15,115)
        text("A or LEFT ARROW = Left Turn",15,145)
        text("D or RIGHT ARROW = Right Turn",15,175)
        text("SHIFT = Teleport",15,205)
        text("Spacebar = Shoot",15,235)
    #IN-GAME
    if mode == 1:
        if len (asteroid) <= 0:
            for n in range(4):
                create_asteroid(asteroid)
        #UFO SPAWN TIME CONSTANTLY BEING DECREASED TO 0 TO SPAWN NEW UFOS
        ufospawntime -= 1
        if ufospawntime <= 0:
            create_UFO(ufo)
        #IF THE PLAYERS LIVES GO TO 0 THE PLAYER IS SENT TO THE GAME OVER SCREEN
        if player.lives <= 0:
            mode = 2
            #THE BEATING SOUND IS PAUSED
            beat.pause()
            #ALL UFO SOUNDS STOP
            ufobig.pause()
            ufosmall.pause()
        fill(0)
        #ALL CODE IN PUSH AND POP MATRIX CONCERNS THE PLAY OBJECT
        pushMatrix()
        #TRANSLATE BASED ON TRANSLATION VALUES AND COORDINATE VALUES
        translate(player.translationx+player.x,player.translationy+player.y)
        #CALLING PLAYER METHODS
        player.move()
        player.rotmove()
        player.invince()
        player.flicker()
        rotate(radians(player.rotation+90))
        #WHEN THE PLAYERS FLICKER VALUE IS BELOW 0 IT WILL SHOW ROCKET
        if player.flickervalue < 5:
            fill(0)
            triangle(0,-15,15,10,-15,10)
            fill(255)
            strokeWeight(2)
            line(15, 10, 22, 23)
            line(-15, 10, -22, 23)
            #ROCKET THRUST ANIMATION
            if player.thrust == 1:
                fill(255,100,0)
                triangle(-8,13,8,13,0,25)
        popMatrix()
        fill(0)
        #DRAWING UFOS FROM LIST
        for u in ufo:
            u.move()
            u.change_direction_shot()
            u.change_movement()
            #SHAPE OF UFO
            if u.r == 31:
                quad(u.x-10,u.y-20,u.x+10,u.y-20,u.x+15,u.y-10,u.x-15,u.y-10)
                quad(u.x-30,u.y+5,u.x+30,u.y+5,u.x+15,u.y-10,u.x-15,u.y-10)
                quad(u.x-30,u.y+5,u.x+30,u.y+5,u.x+15,u.y+20,u.x-15,u.y+20)
            if u.r == 11.001:
                quad(u.x-5,u.y-10,u.x+5,u.y-10,u.x+7.5,u.y-5,u.x-7.5,u.y-5)
                quad(u.x-15,u.y+2.5,u.x+15,u.y+2.5,u.x+7.5,u.y-5,u.x-7.5,u.y-5)
                quad(u.x-15,u.y+2.5,u.x+15,u.y+2.5,u.x+7.5,u.y+10,u.x-7.5,u.y+10)
            #IF PLAYER IS NOT INVICIBLE IT WILL CALL COLLISION CHECK
            if player.playerinv == 0:
                Player(player.translationx + player.x, player.translationy + player.y,11,0,0,0).player_collision(u)
        #CHECKING FOR HOW MANY UFOS ARE ALIVE
        counterbig = 0
        countersmall = 0
        for u in ufo:
            if u.r == 31:
                counterbig += 1
            if u.r == 11.001:
                countersmall += 1
        if counterbig == 0:
            ufobig.pause()
        if countersmall == 0:
            ufosmall.pause()
        countersmall = 0
        counterbig = 0
        #CHECKING FOR COLLISION BETWEEN ASTEROIDS AND:
        for a in asteroid:
            #BULLETS
            for b in bullets:
                a.asteroid_collision(b)
            #PLAYER
            if player.playerinv == 0:
                a.asteroid_collision(Player(player.translationx + player.x, player.translationy + player.y,11,0,0,0))
            #UFO
            for u in ufo:
                a.asteroid_collision(u)
            #UFO BULLET
            for ub in ufo_bullets:
                a.asteroid_collision(ub)
            #CHECKING TO SEE IF ASTEROID IS DEAD
            a.asteroiddeath()
        #DRAWING BULLET
        for b in bullets:
            b.move()
            b.bullettime()
            ellipse(b.x,b.y,b.r,b.r)
            #CHECK IF BULLET HAS COLLIDED WITH UFO
            for u in ufo:
                u.ufo_collision(b)
        #DRAW UFO BULLET
        for ub in ufo_bullets:
            ub.move()
            ub.bullettime()
            ellipse(ub.x,ub.y,ub.r,ub.r)
            #CHECK IF PLAYER IS INVICIBLE TO CHECK FOR COLLISION
            if player.playerinv == 0:
                Player(player.translationx + player.x, player.translationy + player.y,11,0,0,0).player_collision(ub)
        textSize(30)
        fill(255)
        #DISPLAYS PLAYERS SCORE
        text(player.score,25,35)
        fill(0)
        #DISPLAYS PLAYERS LIVES IN GRAPHICAL MANNER
        if player.lives >= 1:
            triangle(60,45,75,70,45,70)
            line(75, 70, 82, 83)
            line(45, 70, 38, 83)
        if player.lives >= 2:
            triangle(110,45,125,70,95,70)
            line(125, 70, 132, 83)
            line(95, 70, 88, 83)
        if player.lives == 3:
            triangle(160,45,175,70,145,70)
            line(175, 70, 182, 83)
            line(145, 70, 138, 83)
    #GAME OVER SCREEN
    if mode == 2:
        textSize(60)
        text("FINAL SCORE:",400,100)
        text(player.score,500,200)
        textSize(40)
        text("ENTER YOUR NAME:",400,400)
        text(name,500,500)
        textSize(30)
        text('(Press "Enter" to Return to Main Menu)',300,600)
    #HIGH SCORES SCREEN
    if mode == 3:
        textSize(60)
        text("High Scores",440,100)
        textSize(35)
        fill(0)
        rect(50,50,200,60)
        rect(900,50,200,60)
        fill(255)
        text("Main Menu",60,90)
        text("Reset", 940,90)
        #DISPLAYS HIGHSCORES OF ALL TIME
        if len (scores) >= 1:
            text(high_scores[0][1],425,270)
            text(high_scores[0][0],705,270)
        if len (scores) >= 2:
            text(high_scores[1][1],425,370)
            text(high_scores[1][0],705,370)
        if len (scores) >= 3:
            text(high_scores[2][1],425,470)
            text(high_scores[2][0],705,470)
        if len (scores) >= 4:
            text(high_scores[3][1],425,570)
            text(high_scores[3][0],705,570)
#MOUSE CLICKED
def mouseClicked():
    global mode,scores,high_scores
    #IF TITLE SCREEN
    if mode == 0:
        #TURN GAME MODE TO IN-GAME
        if 440 <= mouseX <= 740 and 300 <= mouseY <= 370:
            beat.loop()
            mode = 1
            reset()
        #TURN GAME MODE TO HIGHSCORES
        if 420 <= mouseX <= 770 and 405 <= mouseY <= 475:
            mode = 3
    #IF ON HIGH SCORES SCREEN
    if mode == 3:
        #BACK TO MAIN MENU
        if 50 <= mouseX <= 250 and 50 <= mouseY <= 110:
            mode = 0
        #RESET ALL SCORES BUTTON
        if 900 <= mouseX <= 1100 and 50 <= mouseY <= 110:
            with open("scores.txt", "w") as out_score:
                out_score.write("")
            scores = []
            high_scores = []
        
#KEYPRESSED                                
def keyPressed():
    global name,entered,mode,scores,high_scores
    #IF ON GAME OVER SCREEN
    if mode == 2:
        #ALLOWS USER TO ENTER NAME IN WITH SPACES ONLY ALPHANEUMERIC CHARACTERS AND HAS THE PLAYER PRESS ENTER WHEN DONE OR BACKSPACE TO REMOVE CHARACTERS
        if entered == False:
            if key == ENTER or key == RETURN:
                entered = True
            if key == BACKSPACE:
                name = name[0:-1]
            lk = ''
            if isinstance(key, basestring):
                if key.isalnum() or key == ' ':
                    lk = key
            name = name +lk
        #WHEN ENTERED
        if entered == True:
            #WRITES THE NEW SCORE TO FILE
            with open("scores.txt", "a") as out_score:
                out_score.write("%s" % (player.score) + "\n")
                out_score.write(name + "\n")
            entered = False
            #APPEND NEW SCORES TO SCORES AND HIGHSCORES SORTS ITSELF
            newplayer = [player.score,name]
            scores.append(newplayer)
            name = ''
            #BACK TO TITLE SCREEN
            mode = 0
            high_scores = (sorted(scores,key=lambda l:l[0], reverse=True))
    #IF IN GAME
    if mode == 1:
        #TURN LEFT
        if key == 'a' or keyCode == LEFT:
            player.rotthrust = -1
        #TURN RIGHT
        elif key == 'd' or keyCode == RIGHT:
            player.rotthrust = 1
        #GO FORWARD
        if key == 'w' or keyCode == UP:
            player.thrust = 1
        #BREAK
        if key == 's' or keyCode == DOWN:
            player.thrust = -1
    
def keyReleased():
    #IF IN GAME
    if mode == 1:
        #ALLOWS USER TO TELEPORT RANDOMLY
        if keyCode == SHIFT:
            player.x = random.randint(-550,550)
            player.y = random.randint(-350,350)
        #SLOW DOWN DR
        if key == 'a' or keyCode == LEFT:
            if player.rotthrust != 1:
                player.rotthrust = 0
        #SLOW DOWN DR
        elif key == 'd' or keyCode == RIGHT:
            if player.rotthrust != -1:
                player.rotthrust = 0
        #SLOWS DOWN THRUST ACCELERATION AND ASSIGNS THE LAST ROTATION PRIOR TO THRUST BEING TURNED OFF
        if key == 'w' or keyCode == UP:
            player.thrust = 0
            player.temprotation = player.rotation
        #STOPS THE BREAKING OF THE SHIP
        if key == 's' or keyCode == DOWN:
            player.thrust = 0
        #SHOOT PLAYER BULLET
        if key == ' ':
            #IF THE PLAYER HAS LESS THAN OR EQUAL TO 5 BULLETS IN ITS LIST THAN IT WILL ALLOW A NEW PLAYER BULLE TO BE CREATED
            if len (bullets) <= 5:
                player.create_bullet(7,bullets)
