"""CS 108 Project

This module implements a GUI controller for an ant particle simulation game.

@author: Brea-Koenes (bjk47)
@date: Summer, 2020
"""
from tkinter import *
from random import randint
from particle import Particle, Ant, AntHole
from helpers import get_random_color


class ParticleSimulation:
    """Runs a simulation of multiple particles interacting
    on a single canvas.
    """
        
    def __init__(self, window, width=1000, height=400):
        """Instantiate the simulation GUI window."""
        self.window = window
        self.window.bind('<Key>', self.process_key_event)
        self.width = width
        self.height = height
        self.delay = 10
        self.animationrunning = True
        
        # Imports a white canvas
        self.canvas = Canvas(self.window, bg='white',
                             width=self.width, height=self.height)
        self.canvas.pack()
        
        # Adds welcome message
        self.label = StringVar()
        self.label.set("Please enter name below")
        label = Label(window, textvariable=self.label, bg = '#7fff00', fg = 'black', font = 'Verdana')
        label.pack()
        
        # Adds an entry box
        self.username_entry_box = StringVar()
        self.username_entry_box.set('')
        username_entry_box = Entry(window, textvariable=self.username_entry_box)
        username_entry_box.pack()
        
        # Initiates list and particle loop
        self.p_list = []
        for i in range(8):
            self.add_particle(bad = True)
        for i in range(30):
            self.add_particle()
        self.ant = Ant(x = 0, y = self.height)
        self.anthole = AntHole(x = 930, y = self.height, ant = self.ant)
        print(self.p_list)

        # Instantiate and display score label
        self.score = 0
        self.scorevar = StringVar()
        self.scorevar.set(self.score)
        self.score_label = Label(window, textvariable = self.scorevar, width = 20)
        self.score_label.pack()
        
        # Adds highest score label
        self.message = StringVar()
        self.message.set("")
        score_label = Label(window, textvariable = self.message, width = 20)
        score_label.pack()
        
        # Schedule the first animation frame
        self.window.after(0, self.animation)
        
    def add_particle(self, bad = False):
        """Randomizes colors and sizes of particles into the simulation"""
        radius = randint(5, 25)
        x = randint(25, self.width-25)
        y = randint(25, self.height-25)
        vel_x = randint(-radius//10, radius // 10)
        vel_y = randint(-radius//10, radius // 10)
        color = get_random_color()
            
        p = Particle(x, y, vel_x, vel_y, radius, color, bad = bad)
        self.p_list.append(p)
    
    def animation(self):
        """Enables particles to move and bounce off objects and window walls,
        along with adjusting the score"""
        
        # Deducts or adds points to score when it hits particles
        self.canvas.delete(ALL)
        if self.animationrunning:
            for p in self.p_list:
                p.move(self.canvas)
            for p in self.p_list:
                if self.ant.hits(p):
                    if p.bad:
                        self.score -= 1
                    else:
                        self.score += 1
                    self.p_list.remove(p)
            self.scorevar.set(self.score)
            
            # Allows particles to bounce off objects
            for i in range(len(self.p_list)):
                for j in range(i):
                    self.p_list[i].bounce(self.p_list[j])
            for p in self.p_list:
                p.render(self.canvas)
            
            # Reads top score and name into textfiles
            leaderboard = open('leaderboard.txt')
            contents = leaderboard.read()
            contents = int(contents)
            
            leaderboard_name = open('leaderboard_name.txt')
            name = leaderboard_name.read()
            name = str(name)
            
            if self.score > contents:
                f = open('leaderboard.txt', 'w')
                f.write(str(self.score))
                f.close()
                
                f = open('leaderboard_name.txt', 'w')
                f.write(self.username_entry_box.get())
                f.close()
                
            # Ends stimulation when ant reaches anthole
            if self.ant.hits(self.anthole):
                self.animationrunning = False
                self.label.set("Play again soon!")
                self.scorevar.set("Your score: " + str(self.score))
                self.message.set(name + "'s highest score: " + str(contents))
        
        # Renders ant and anthole
        self.ant.render(self.canvas)
        self.anthole.render(self.canvas)
        self.canvas.after(self.delay, self.animation)
                    
    def process_key_event(self, event):
        """Move ant based on arrow keys"""
        if event.keysym == 'Right':
            self.ant.move_east()
        elif event.keysym == 'Left':
            self.ant.move_west()
        
if __name__ == '__main__':
    root = Tk()
    root.title('Particle Simulation')    
    app = ParticleSimulation(root)
    root.mainloop()
