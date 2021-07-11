"""CS 108 Project

This module implements a model of shaped particles for a game.

@author: Brea-Koenes (bjk47)
@date: Summer, 2020
"""

from helpers import distance
from tkinter import PhotoImage

class Particle:
    """Particle models a single particle that may be rendered to a canvas"""

    def __init__(self, x=50, y=50, vel_x=10, vel_y=15, radius=40, color="red", bad = False):
        """Instantiate a particle object."""
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color
        self.bad = bad
        # Imports anteater image
        if self.bad:
            self.image = PhotoImage(file="anteater-medium.gif")

    def hits(self, other):
        """Determine if particles have collided with 'other'"""
        if self == other:
            return False
        return (
            self.radius + other.radius >=
            distance(self.x, self.y, other.x, other.y)
        )

    def bounce(self, other):
        """Handle elastic collisions between this particle and 'other'.
        Thanks to Dr. Paul Harper (Calvin Physics)
        """
        if not self.hits(other):
            return

        # Calculate masses (proportional to area)
        m1 = self.radius ** 2
        m2 = other.radius ** 2

        # Calculate velocity of center of mass
        v_cm_x = (m1 * self.vel_x + m2 * other.vel_x) / (m1 + m2)
        v_cm_y = (m1 * self.vel_y + m2 * other.vel_y) / (m1 + m2)

        # Calculate new velocities.
        # Note that the velocity of the center of mass is unchanged, and
        # that if the center of mass is not moving, the velocity just inverts.
        self.vel_x = 2 * v_cm_x - self.vel_x
        self.vel_y = 2 * v_cm_y - self.vel_y

        other.vel_x = 2 * v_cm_x - other.vel_x
        other.vel_y = 2 * v_cm_y - other.vel_y

        # Fix up the positions to ensure they're not stuck together.
        dist_x = self.x - other.x
        dist_y = self.y - other.y
        dist = (dist_x ** 2 + dist_y ** 2) ** 0.5
        dist_x_norm = dist_x / dist
        dist_y_norm = dist_y / dist
        intrusion_distance = (self.radius + other.radius - dist) / 2 + 1e-6

        self.x += intrusion_distance * dist_x_norm
        self.y += intrusion_distance * dist_y_norm
        other.x -= intrusion_distance * dist_x_norm
        other.y -= intrusion_distance * dist_y_norm
               
    def render(self, canvas):
        """Recieves canvas to draw 'bad' and 'good' particles"""
        if self.bad:
            canvas.create_image(self.x - self.radius,
               self.y - self.radius, image = self.image
               )
            
        else:
            canvas.create_oval(self.x - self.radius,
               self.y - self.radius,
               self.x + self.radius,
               self.y + self.radius,
               fill=self.color
               )
    
    def move(self, canvas):
        """Updates the x, y coordinates according to their velocities""" 
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x + self.radius > canvas.winfo_reqwidth() or self.x - self.radius < 0:
            self.vel_x = self.vel_x *-1
        if self.y + self.radius > canvas.winfo_reqheight() or self.y - self.radius < 0:
            self.vel_y = self.vel_y *-1


class Ant:
    
    def __init__(self, x=50, y=50, vel_x=5, vel_y=0, radius=22, color="black"):
        """Instantiate a particle object"""
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color

    def render(self, canvas):
        """Recieves canvas to draw an ant"""
        canvas.create_oval(self.x+10, self.y-10, self.x+20, self.y, fill = self.color)
        canvas.create_oval(self.x+20, self.y-10, self.x+30, self.y, fill = self.color)
        canvas.create_oval(self.x+30, self.y-10, self.x+40, self.y, fill = self.color)
        canvas.create_line(self.x+35, self.y-8, self.x+50, self.y-10)
        canvas.create_line(self.x+35, self.y-8, self.x+45, self.y-15)
                           
    def move_east(self):
        """Allows arrow key to move ant east"""
        self.x += self.vel_x
        
    def move_west(self):
        """Allows arrow key to move ant west"""
        self.x -= self.vel_x
    
    def hits(self, other):
        """Determine if ant collides with particles"""
        return (
            self.radius + other.radius >=
            distance(self.x, self.y, other.x, other.y)
        )


class AntHole:
    
    def __init__(self, x=50, y=50, vel_x=0, vel_y=0, radius=10, color="white", ant = None):
        """Instantiate an anthole object"""
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius
        self.color = color
        self.position = (0, 0)
        self.ant = ant
        
    
    def render(self, canvas):
        """Recieves a canvas to draw anthole"""
        canvas.create_oval(self.x+20, self.y-10, self.x+70, self.y, fill = self.color)

if __name__ == '__main__':

    a = Ant()
    assert a.x == 50
    assert a.y == 50
    assert a.vel_x == 5
    assert a.vel_y == 0

    print('all tests passed...')
