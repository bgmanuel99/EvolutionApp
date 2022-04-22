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
        limit = int(self.winfo_height() / len(self.colors))
        
        rgb_colors = []
        for color in self.colors:
            r, g, b = self.winfo_rgb(color)
            rgb_colors.append((r, g, b))

        rgb_ratios = []
        for i in range(len(rgb_colors)-1):
            r_ratio = float(rgb_colors[i+1][0] - rgb_colors[i][0]) / limit
            g_ratio = float(rgb_colors[i+1][1] - rgb_colors[i][1]) / limit
            b_ratio = float(rgb_colors[i+1][2] - rgb_colors[i][2]) / limit
            rgb_ratios.append((r_ratio, g_ratio, b_ratio))

        start_limit = 0
        end_limit = limit
        multiplicator = 0
        for i in range(len(rgb_colors)-1):
            for j in range(start_limit, end_limit):
                nr = int(rgb_colors[i][0] + (rgb_ratios[i][0] * multiplicator))
                ng = int(rgb_colors[i][1] + (rgb_ratios[i][1] * multiplicator))
                nb = int(rgb_colors[i][2] + (rgb_ratios[i][2] * multiplicator))
                multiplicator += 1
                color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
                self.create_line(0, j, width, j, tags=("gradient",), fill=color)

            start_limit += limit
            end_limit += limit
            multiplicator = 0

        self.lower("gradient")

    def set_new_colors(self, *args):
        """Setter method for attribute color1 and color2"""

        self.colors = []

        for color in args:
            self.colors.append(color)

        self.draw_gradient()