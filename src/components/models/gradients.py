from tkinter import *

class GradientFrame(Canvas):

    """
    This component draws a canvas object as a gradient.
    The object receives three parameters to the constructor: root, color1 and color2:
        root    -> The parent object
        color1  -> The first color of the gradient
        color2  -> The second color of the gradient
    """

    def __init__(self, root, color1, color2):
        Canvas.__init__(self, root)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event=None):
        """Draw a gradient using a tkinter canvas"""

        self.delete("gradient")

        width = self.winfo_width()
        limit = self.winfo_height()

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
            
        self.lower("gradient")

    def set_new_colors(self, color1, color2):
        """Setter method for attribute color1 and color2"""

        self.color1 = color1
        self.color2 = color2
        self.draw_gradient()