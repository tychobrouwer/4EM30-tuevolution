import pygame, numpy, TUEvolution.utils as utils

class Cycler:
    """
    A class to manage cycling through multiple graphs.
    """

    def __init__(self, *, left, top, width, height, border, font_size, graphs=[]):
        """
        Initialize a Cycler object.

        Parameters:
        left (int): The left position of the cycler.
        top (int): The top position of the cycler.
        width (int): The width of the cycler.
        height (int): The height of the cycler.
        border (int): The border size of the cycler.
        font_size (int): The font size used in the cycler.
        graphs (list): A list of graphs to cycle through.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border = border
        self.font_size = font_size
        self.graphs = graphs

        # Update the graph dimensions
        for graph in graphs:
            graph.left = left+border
            graph.top = top+border
            graph.width = width-2*border
            graph.height = height-2*border
            graph.border = border
            graph.font = pygame.font.SysFont('Arial', font_size)

        # Set the first graph as active
        self.active = -1 if len(graphs)==0 else 0
        self.bullet_radius = font_size//3
        bullets_width = font_size*len(graphs)
        self.bullet_centers = [numpy.array([self.left+(self.width-bullets_width)//2+i*font_size+font_size//2,self.top+self.height-self.border//2]) for i in range(len(graphs))]

    def next(self):
        """
        Cycle to the next graph.
        """
        self.active = (self.active+1)%len(self.graphs)

    def previous(self):
        """
        Cycle to the previous graph.
        """
        self.active = (self.active-1)%len(self.graphs)

    def get_hovered(self):
        """
        Get the index of the hovered bullet.

        Returns:
        int: The index of the hovered bullet, or -1 if no bullet is hovered.
        """
        mouse_position = numpy.array(pygame.mouse.get_pos())
        for bullet_number, bullet_center in enumerate(self.bullet_centers):
            if sum((mouse_position-bullet_center)**2)<(self.bullet_radius)**2:
                return bullet_number
        return -1

    def draw(self, screen):
        """
        Draw the cycler and the active graph on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        # background color for hovered bullet
        hovered = self.get_hovered()
        if hovered!=-1:
            pygame.draw.circle(screen, utils.color('darkgray'), self.bullet_centers[hovered], self.bullet_radius)

        # bullets
        for bullet_number, bullet_center in enumerate(self.bullet_centers):
            pygame.draw.circle(screen, utils.color('black'), bullet_center, self.bullet_radius, width=(bullet_number!=self.active))
        self.graphs[self.active].draw(screen)

        # tab icon
        if len(self.bullet_centers)>0:
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0]-self.bullet_radius*numpy.array([5,0]), self.bullet_centers[0]-self.bullet_radius*numpy.array([3,0]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0]-self.bullet_radius*numpy.array([3,1]), self.bullet_centers[0]-self.bullet_radius*numpy.array([3,-1]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0]-self.bullet_radius*numpy.array([3,0]), self.bullet_centers[0]-self.bullet_radius*numpy.array([4,1]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0]-self.bullet_radius*numpy.array([3,0]), self.bullet_centers[0]-self.bullet_radius*numpy.array([4,-1]), 1)

class XY:
    """
    A class to represent an XY graph.
    """

    def __init__(self, *, left=None, top=None, width=None, height=None, border=None, xlabel, ylabel, xticks, yticks, linecolor, fontsize):
        """
        Initialize an XY graph object.

        Parameters:
        left (int, optional): The left position of the graph. Defaults to None.
        top (int, optional): The top position of the graph. Defaults to None.
        width (int, optional): The width of the graph. Defaults to None.
        height (int, optional): The height of the graph. Defaults to None.
        border (int, optional): The border size of the graph. Defaults to None.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        xticks (int or list): The ticks for the x-axis.
        yticks (int or list): The ticks for the y-axis.
        linecolor (tuple): The color of the line in the graph.
        fontsize (int): The font size used in the graph.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border = border

        self.xlabel = xlabel
        self.ylabel = ylabel

        self.xticks = xticks
        self.yticks = yticks

        self.linecolor = linecolor

        self.data = numpy.zeros(shape=(0, 2), dtype=int)
        self.font = pygame.font.SysFont('Arial', fontsize)

    def add(self, point):
        """
        Add a data point to the graph.

        Parameters:
        point (tuple): A tuple representing the data point (x, y).
        """
        self.data = numpy.append(
            self.data, numpy.array(point).reshape(1, 2), axis=0)

    def to_screen_coordinates(self, data):
        """
        Convert data coordinates to screen coordinates.

        Parameters:
        data (numpy.ndarray): The data points.

        Returns:
        numpy.ndarray: The screen coordinates.
        """
        xlim, xticks = self.get_lim_and_ticks(0)
        ylim, yticks = self.get_lim_and_ticks(1)

        scale = numpy.array(
            [(self.width-2*self.border)/(xlim[1]-xlim[0]), (self.height-2*self.border)/(ylim[0]-ylim[1])])
        offset = numpy.array([self.left+self.border, self.top+self.height-self.border])
        return scale*data+offset

    def get_lim_and_ticks(self, axis):
        """
        Get the limits and ticks for the specified axis.

        Parameters:
        axis (int): The axis (0 for x-axis, 1 for y-axis).

        Returns:
        tuple: A tuple containing the limits and ticks for the axis.
        """
        if axis==0:
            ticks = self.xticks
        else:
            ticks = self.yticks

        if isinstance(ticks, int):
            max = 0
            if self.data.shape[0]>0:
                max = numpy.maximum(int(numpy.round(1.1*numpy.max(self.data[:,axis]))),0)
            max += (ticks-max%ticks)
            lim = [0,max]
            ticks = numpy.arange(lim[0], lim[1]+1, (lim[1]-lim[0])//ticks)
        else:
            lim = [numpy.min(ticks), numpy.max(ticks)]

        return lim, ticks

    def draw_grid(self, screen):
        """
        Draw the grid for the graph.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        # box
        pygame.draw.rect(screen, utils.color('black'), (self.left+self.border, self.top+self.border, self.width-2*self.border, self.height-2*self.border), 3)

        # update limits
        xlim, xticks = self.get_lim_and_ticks(0)
        ylim, yticks = self.get_lim_and_ticks(1)

        # vertical grid lines
        for xtick in xticks[1:-1]:
            pygame.draw.line(screen, utils.color('gray'), self.to_screen_coordinates(numpy.array(
                [xtick, ylim[0]])), self.to_screen_coordinates(numpy.array([xtick, ylim[1]])), 1)

        # horizontal grid lines
        for ytick in yticks[1:-1]:
            pygame.draw.line(screen, utils.color('gray'), self.to_screen_coordinates(numpy.array(
                [xlim[0], ytick])), self.to_screen_coordinates(numpy.array([xlim[1], ytick])), 1)

        # xlim[0]
        label = self.font.render(f'{xlim[0]}', True, (0, 0, 0))
        screen.blit(label, (self.left+self.border, self.top+self.height-self.border))

        # xlim[1]
        label = self.font.render(f'{xlim[1]}', True, (0, 0, 0))
        screen.blit(label, (self.left-self.border+self.width -
                    label.get_width(), self.top+self.height-self.border))

        # ylim[0]
        label = self.font.render(f'{ylim[0]}', True, (0, 0, 0))
        screen.blit(label, (self.left+self.border-label.get_width(),
                    self.top+self.height-label.get_height()-self.border))

        # ylim[1]
        label = self.font.render(f'{ylim[1]}', True, (0, 0, 0))
        screen.blit(label, (self.left+self.border-label.get_width(), self.top+self.border))

        # xlabel
        label = self.font.render(f'{self.xlabel}', True, (0, 0, 0))
        screen.blit(
            label, (self.left+(self.width-label.get_width())//2, self.top+self.height-self.border))

        # ylabel
        label = self.font.render(f'{self.ylabel}', True, (0, 0, 0))
        label = pygame.transform.rotate(label, 90)
        screen.blit(label, (self.left+self.border-label.get_width(),
                    self.top+(self.height-label.get_height())//2))

    def draw(self, screen):
        """
        Draw the graph on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        self.draw_grid(screen)

        if self.data.shape[0]>1:
            pygame.draw.lines(screen, self.linecolor, False,
                              self.to_screen_coordinates(self.data), 3)
