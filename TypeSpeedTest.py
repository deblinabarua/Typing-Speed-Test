import pygame
from pygame.locals import*
import sys
import time
import random

#Creating a class which contains all the functions for the typing speed test
class Game:
    def __init__(self):
        #Defining the properties of the class
        self.width = 1200
        self.height = 600
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0% wpm:0'
        self.wpm = 0
        self.end = False
        self.head_c = (183,113,64)
        self.text_c = (240,240,240)
        self.result_c = (255,70,70)

        pygame.init() #Initialize all imported pygame modules
        self.open_img = pygame.image.load(r"C:\Users\HP\Downloads\Loading.png")
        self.open_img = pygame.transform.scale(self.open_img,(self.width,self.height)) #Resizes the image to a new resolution

        self.bg = pygame.image.load(r"C:\Users\HP\Downloads\Background.png")
        self.bg = pygame.transform.scale(self.bg,(1200,600))

        self.screen=pygame.display.set_mode((self.width,self.height)) #Creates a window where the game will function
        pygame.display.set_caption('Typing Speed Test')

    def draw_text(self,screen,msg,y,fsize,color):
        font = pygame.font.Font(None,fsize) #Creates a new Font object from a file
        text = font.render(msg,1,color) #Draws text on a new surface
        text_rect = text.get_rect(center=(self.width/2,y)) #Gets the rectangular area of the surface
        screen.blit(text,text_rect) #Draws one image onto another
        pygame.display.update() #Updates what needs to be displayed

    def get_sentence(self):
        f = open("Sentences.txt").read()
        sentences = f.split('\n') #Puts the contents of the file into a list after every new line
        sentence = random.choice(sentences) #Returns a random element from the list
        return sentence

    def show_results(self,screen):
        if(not self.end):
            self.total_time = time.time() - self.time_start #Gets time in seconds since epoch which is platform dependent

            count = 0
            for i,c in enumerate(self.word): #Returns the index and its element pair from the iterable object
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time: ' + str(round(self.total_time)) + " secs    Accuracy:" + str(round(self.accuracy)) + "%    wpm: " + str(round(self.wpm))

            self.time_img = pygame.image.load(r"C:\Users\HP\Downloads\Reset.png")
            self.time_img = pygame.transform.scale(self.time_img,(150,150))
            screen.blit(self.time_img,(self.width/2-75,self.height-140))
            self.draw_text(screen,"Reset",self.height-70,26,(100,100,100))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()

        self.running = True
        while(self.running):
            clock = pygame.time.Clock() #Creates an object to help track time
            self.screen.fill((0,0,0),(300,250,650,50)) #Fills surface with a solid colour
            pygame.draw.rect(self.screen,self.head_c,(300,250,650,50),2)

            self.draw_text(self.screen,self.input_text,274,26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get(): #Gets events in a queue
                if event.type == QUIT: #Refering to the 'quit' in the opened window
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP: #Events related to the mouse
                    x,y = pygame.mouse.get_pos() #Gets the mouse cursor position
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    if(x>=525 and x<=650 and y>=460 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen,self.results,350,28,self.result_c)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img,(0,0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()
        if(not self.word):
            self.reset_game()

        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen,msg,80,80,self.head_c)

        pygame.draw.rect(self.screen,(255,192,25),(300,250,650,50),2)

        self.draw_text(self.screen,self.word,200,28,self.text_c)

        pygame.display.update()

Game().run()