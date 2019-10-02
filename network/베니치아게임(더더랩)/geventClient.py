import socket,time
from random import randint
from threading import Thread
import pygame,time


# color
white = (255,255,255)
black = (0,0,0)
tomato = (255,99,71)
ivory = (226,222,216)
blueviolet = (138,43,226)
COLOR_INACTIVE = ivory
COLOR_ACTIVE = pygame.Color('purple')

TYPEDWORD = ''

# window
screen = pygame.display.set_mode((700, 850))

# background
background = pygame.image.load('./img/ubuntu.jpeg').convert()
background = pygame.transform.scale(background, (700, 700))
# screen.blit(background, (0, 50))
# pygame.display.flip()


class Word():
    def __init__(self,word,cor):
        pygame.font.init()
        self.f = pygame.font.Font("./myfont.ttf", 20) # Font type # Font style
        # word died or alive
        self.state = True
        self.str = word
        self.word = self.f.render(word, True, (255,255,0)) 
        self.x, self.y = cor

def move():
    global word_queue
    
    clock = pygame.time.Clock()
    input_box = InputBox(screen,0, 750, 700, 100)
    score_box = ScoreBox(screen)
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            input_box.handle_event(event)
        screen.blit(background, (0, 50))
        word_queue = [i for i in word_queue if i.state==True]
        for word in word_queue:
            if word.y> 750:
                score_box.update(screen,"life")
                word.state = False
                continue
            # print(word.str, TYPEDWORD)
            if word.str == TYPEDWORD: 
                word.state = False
                score_box.update(screen,'score')
                continue                
            word.y+=5
            screen.blit(word.word, (word.x, word.y))
            # pygame.display.flip()
        
        pygame.display.update()
        #update
        screen.fill(ivory,input_box)
        input_box.draw(screen)
        # (self, screen,flag):
        #draw
        # pygame.display.flip()
        clock.tick(30)


def run():
    global word_queue
    
    width = 700
    ip,port,bufsize = '127.0.0.1',8080,1024
    with socket.socket() as s:
        s.connect((ip,port))
        Thread(target=move).start()
        while True:
            word = s.recv(bufsize).decode()
            x = randint(0,width-50)
            word_queue.append(Word(word,(x,100)))
        

#@TODO: event handler해야된다.
class ScoreBox:
    def __init__(self,screen,life=6):
        self.life = life
        self.ubuntu = "UBUNTU"
        self.screen = screen
        self.score = 0
        # self.font = pygame.font.Font('./score.ttf', 20)
        self.font = pygame.font.Font(None,20)
        self.text_surface = self.font.render("SCORE:"+str(self.score)+"                   "+self.ubuntu,True,white)
        self.text_rect = self.text_surface.get_rect()
        self.rect = pygame.Rect(0,0,700,50)
        
        self.text_rect.midtop = (350,25)
        screen.blit(self.text_surface, self.text_rect)

    def update(self, screen,flag):
        if flag == "life": print("life-1");self.life -= 1;self.ubuntu = "UBUNTU"[:self.life]
        else: self.score += 1; print("score +1")
        # x,y는 위치
        
        pygame.draw.rect(screen,black,self.rect,2)
        # pygame.draw.rect(screen,black,self.rect,2)
        screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()


# https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame       
class InputBox:
    global word_queue
    
    def __init__(self,screen,x, y, w, h, text=''):
        pygame.font.init()
        self.FONT = pygame.font.Font('./myfont2.ttf', 40)
        self.screen = screen
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text,True, black)
        self.active = False
        self.rect = pygame.Rect(x,y,w,h)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # text를 word_Q에 보내주기
                    TYPEDWORD = self.text

                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, black)
                
                
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+285, self.rect.y+20))
        # Blit the rect.
        pygame.draw.rect(screen,self.color,self.rect,2)



if __name__ == '__main__':
    word_queue=[]
    run()













# q = []
# a,b = "photato","ddd"
# cor = (17,0)
# c = "age"
# q.append(Word(a,cor))
# q.append(Word(b,cor))
# q.append(Word(c,(9,12)))
# while True:
#     for i in q:
#         i.y+=1
#         print(str(i.y)+',',end="")
#     print()
#     time.sleep(1)
    