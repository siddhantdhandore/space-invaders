import pygame
import random
import math
import time
from pygame import mixer

pygame.init()
running=True
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
backgroundImg=pygame.image.load('bg.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)
clock=pygame.time.Clock()
#score 
myFont=pygame.font.Font("freesansbold.ttf",40)

def showScore():
	textSurf=myFont.render(f"Score : {score}",True,(0,255,255))
	screen.blit(textSurf,(10,10))
#player
playerImg=pygame.image.load('rocket.png')
playerX=WIDTH//2-playerImg.get_width()//2
playerY=HEIGHT-150
playerX_change=0
def player(x,y):
	screen.blit(playerImg,(playerX,playerY))




#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
numberOfEnemies=6

def enemy(x,y,i):
	screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))
def drawEnemies():
	for i in range(numberOfEnemies):
		enemyImg.append(pygame.image.load('enemy.png'))
		enemyX.append(random.randint(0,736))
		enemyY.append(random.randint(50,150))
		enemyX_change.append(1.5)
		enemyY_change.append(0)
		enemy(enemyX,enemyY,i)
drawEnemies()
#bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=playerX
bulletY=playerY
bulletX_change=0
bulletY_change=5
bulletState="ready"

def fire_bullet(x,y):
	global bulletState
	bulletState="fire"
	screen.blit(bulletImg,(x,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
	if distance<=enemyImg[0].get_height():
		return True
	return False
score=0

def reset():
	score=0
	playerX=WIDTH//2-playerImg.get_width()//2
	playerY=HEIGHT-150
	bulletState="ready"
	bulletX=playerX
	bulletY=playerY
	bulletX_change=0
	bulletY_change=5
	numberOfEnemies=6
	drawEnemies()
def gameOver():
	myFont=pygame.font.Font("freesansbold.ttf",115)
	textSurf=myFont.render("GAME OVER...!!!",True, (0,255,255))
	textRect=textSurf.get_rect()
	textRect.center=((WIDTH/2),(HEIGHT/2))
	screen.blit(textSurf,textRect)
	pygame.display.update()
	time.sleep(2)
while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
			pygame.quit()
			quit()
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT:
				playerX_change=-2
			if event.key==pygame.K_RIGHT:
				playerX_change=2
			if event.key==pygame.K_SPACE:
				if bulletState=="ready":
					bulletSound=mixer.Sound('explode.wav')
					bulletSound.play()
					bulletX=playerX
					fire_bullet(bulletX,bulletY)


		if event.type==pygame.KEYUP:
			if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
				playerX_change=0

	screen.blit(backgroundImg,(0,0))
	playerX+=playerX_change
	if playerX<=0:
		playerX=0
	elif playerX>=WIDTH-64:
		playerX=WIDTH-64
	player(playerX,playerY)

	
	#enemy movement
	for i in range(numberOfEnemies):
		enemyX[i]+=enemyX_change[i]
		if enemyX[i]<=0:
			enemyX_change[i]=1.5
			enemyY[i]+=40

		if enemyX[i]>734:
			enemyX_change[i]=-1.5
			enemyY[i]+=40
		if enemyY[i]>=400:
			reset()
			gameOver()
			break
			

		collided=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collided:
			bulletY=playerY
			bulletState="ready"
			enemyX[i]=random.randint(0,736)
			enemyY[i]=random.randint(50,200)
			score+=1

			print(score)
			
		enemy(enemyX,enemyY,i)
	if score==15:
		numberOfEnemies=8
		drawEnemies()
	if score==30:
		numberOfEnemies=12
		drawEnemies()
	#bullet movement

	if bulletY<=0:
		bulletState="ready"
		bulletY=playerY

	if bulletState=="fire":
		fire_bullet(bulletX,bulletY)
		bulletY-=bulletY_change


	#collision

	showScore()
	clock.tick(120)
	pygame.display.update()
