from tkinter import *

class VariousDimensionGradient(Canvas):

    """
    This component draws a canvas object as a gradient.
    The object receives a two parameters to the constructor: root and a tuple with the different colors to be drawn:
        root    -> The parent object
        *args   -> Colors for the gradient
    """

    def __init__(self, root, *args):
        Canvas.__init__(self, root)

        self.colors = []

        for color in args:
            self.colors.append(color)

        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event=None):
        """Draw a gradient using a tkinter canvas"""

        self.delete("gradient")

        width = self.winfo_width()
        limit = self.winfo_height()

        # CHANGE THIS PART FOR THE NEW GRADIENT ALGORITHM
        #------------------------------------------------------
        (r1,g1,b1) = self.winfo_rgb(self.color1)
        (r2,g2,b2) = self.winfo_rgb(self.color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)

        #------------------------------------------------------
            
        self.lower("gradient")

    def set_new_colors(self, *args):
        """Setter method for attribute color1 and color2"""

        self.colors = []

        for color in args:
            self.colors.append(color)

        self.draw_gradient()