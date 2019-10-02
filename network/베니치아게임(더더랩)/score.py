import pygame
class Word():
    def __init__(self,word,cor):
        # word died or alive
        self.state = True
        self.word = f.render(word, True, (255,255,0)) 
        self.x, self.y = cor


# screen.blit(background, (0, 50))
li = ['a','b','c','d']
word_q = []
 
while True:
    for i in li:
    word_q.append

Track = f.render(, True, (255,255,0) )
Track = f.render("Track : ", True, (255,255,0) )
Track = f.render("Track : ", True, (255,255,0) )

xpos = 10
ypos = 10

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moveUp = True
            if event.key == pygame.K_s:
                moveDown = True
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True


    if moveDown:
        ypos += 1

