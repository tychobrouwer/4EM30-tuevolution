import pygame
import numpy
import TUEvolution.utils as utils


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
            graph.left = left + border
            graph.top = top + border
            graph.width = width - 2 * border
            graph.height = height - 2 * border
            graph.border = border
            graph.font = pygame.font.SysFont('Arial', font_size)

        # Set the first graph as active
        self.active = -1 if len(graphs) == 0 else 0
        self.bullet_radius = font_size // 3
        bullets_width = font_size * len(graphs)
        self.bullet_centers = [numpy.array([self.left + (self.width - bullets_width) // 2 + i * font_size + font_size // 2, self.top + self.height - self.border // 2 + 15]) for i in range(len(graphs))]

    def next(self):
        """
        Cycle to the next graph.
        """
        self.active = (self.active + 1) % len(self.graphs)

    def previous(self):
        """
        Cycle to the previous graph.
        """
        self.active = (self.active - 1) % len(self.graphs)

    def get_hovered(self):
        """
        Get the index of the hovered bullet.

        Returns:
        int: The index of the hovered bullet, or -1 if no bullet is hovered.
        """
        mouse_position = numpy.array(pygame.mouse.get_pos())
        for bullet_number, bullet_center in enumerate(self.bullet_centers):
            if sum((mouse_position - bullet_center)**2) < (self.bullet_radius)**2:
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
        if hovered != -1:
            pygame.draw.circle(screen, utils.color('darkgray'), self.bullet_centers[hovered], self.bullet_radius)

        # bullets
        for bullet_number, bullet_center in enumerate(self.bullet_centers):
            pygame.draw.circle(screen, utils.color('black'), bullet_center, self.bullet_radius, width=(bullet_number != self.active))
        self.graphs[self.active].draw(screen)

        # tab icon
        if len(self.bullet_centers) > 0:
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0] - self.bullet_radius * numpy.array([5, 0]), self.bullet_centers[0] - self.bullet_radius * numpy.array([3, 0]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0] - self.bullet_radius * numpy.array([3, 1]), self.bullet_centers[0] - self.bullet_radius * numpy.array([3, -1]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0] - self.bullet_radius * numpy.array([3, 0]), self.bullet_centers[0] - self.bullet_radius * numpy.array([4, 1]), 1)
            pygame.draw.line(screen, utils.color('darkgray'), self.bullet_centers[0] - self.bullet_radius * numpy.array([3, 0]), self.bullet_centers[0] - self.bullet_radius * numpy.array([4, -1]), 1)


class Hist:
    """
    A class to represent a histogram.
    """

    def __init__(self, *, left=None, top=None, width=None, height=None, border=None, xlabel, ylabel, barcolor, fontsize):
        """
        Initialize a Histogram object.

        Parameters:
        left (int, optional): The left position of the histogram. Defaults to None.
        top (int, optional): The top position of the histogram. Defaults to None.
        width (int, optional): The width of the histogram. Defaults to None.
        height (int, optional): The height of the histogram. Defaults to None.
        border (int, optional): The border size of the histogram. Defaults to None.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        barcolor (tuple): The color of the bars in the histogram.
        fontsize (int): The font size used in the histogram.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border = border

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.barcolor = barcolor

        self.xmin = 0
        self.xmax = 1

        self.data = []
        self.font = pygame.font.SysFont('Arial', fontsize)

    def add(self, value):
        """
        Add a data value to the histogram.

        Parameters:
        value (int or float): The value to add to the histogram.
        """

        if isinstance(value, int):
            self.data.append(value)

            self.xmin = min(self.data)
            self.xmax = max(self.data)

    def clear(self):
        """
        Clear the current data of the histogram
        """

        self.data = []

    def draw_grid(self, screen, bin_edges, hist_values):
        """
        Draw the grid for the histogram and display axis values.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        bin_edges (numpy.ndarray): The edges of the bins.
        hist_values (numpy.ndarray): The values for each bin.
        """
        pygame.draw.rect(screen, utils.color('black'), (self.left + self.border, self.top + self.border, self.width - 2 * self.border, self.height - 2 * self.border), 3)

        # x and y axis labels
        label = self.font.render(self.xlabel, True, (0, 0, 0))
        screen.blit(label, (self.left + (self.width - label.get_width()) // 2, self.top + self.height - self.border + 20))

        label = self.font.render(self.ylabel, True, (0, 0, 0))
        label = pygame.transform.rotate(label, 90)
        screen.blit(label, (self.left + self.border - label.get_width() - 30, self.top + (self.height - label.get_height()) // 2))

        # Draw x-axis values using the provided xmin and xmax
        bins = len(bin_edges) - 1
        bin_edges = numpy.linspace(self.xmin, self.xmax, bins)

        for i, edge in enumerate(bin_edges):
            label = self.font.render(f'{int(edge)}', True, (0, 0, 0))
            x_pos = self.left + self.border + (i + 0.5) * (self.width - 2 * self.border) // bins - label.get_width() // 2
            y_pos = self.top + self.height - self.border
            screen.blit(label, (x_pos, y_pos))

        num_y_labels = min(5, len(self.data))

        # Draw y-axis values
        max_height = max(hist_values) if hist_values.any() else 1
        for i in range(num_y_labels):  # Draw 5 evenly spaced y-axis labels
            y_val = int((i / num_y_labels) * max_height)
            label = self.font.render(f'{y_val}', True, (0, 0, 0))
            x_pos = self.left + self.border - label.get_width() - 5
            y_pos = self.top + self.height - self.border - (i * (self.height - 2 * self.border) // 4) - label.get_height() // 2
            screen.blit(label, (x_pos, y_pos))

    def draw(self, screen):
        """
        Draw the histogram on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        if not self.data:
            return

        bins = self.xmax - self.xmin + 1

        # Convert data to a NumPy array and ensure numeric type
        numeric_data = numpy.array(self.data, dtype=float)
        hist_values, bin_edges = numpy.histogram(numeric_data, bins=bins, range=(self.xmin, self.xmax))
        bin_width = (self.width - 2 * self.border) / bins
        max_height = max(hist_values) if hist_values.any() else 1

        self.draw_grid(screen, bin_edges, hist_values)

        for i in range(bins):
            bar_height = (hist_values[i] / max_height) * (self.height - 2 * self.border)
            bar_rect = pygame.Rect(
                self.left + self.border + i * bin_width,
                self.top + self.height - self.border - bar_height,
                bin_width - 2,
                bar_height
            )
            pygame.draw.rect(screen, self.barcolor, bar_rect)


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

        self.needs_update = True
        self.cached_grid = None

    def add(self, point):
        """
        Add a data point to the graph.

        Parameters:
        point (tuple): A tuple representing the data point (x, y).
        """
        self.data = numpy.append(
            self.data, numpy.array(point).reshape(1, 2), axis=0)
        self.needs_update = True

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

        scale = numpy.array([(self.width - 2 * self.border) / (xlim[1] - xlim[0]),
                             (self.height - 2 * self.border) / (ylim[0] - ylim[1])])
        offset = numpy.array([self.left + self.border, self.top + self.height - self.border])
        return scale * data + offset

    def get_lim_and_ticks(self, axis):
        """
        Get the limits and ticks for the specified axis.

        Parameters:
        axis (int): The axis (0 for x-axis, 1 for y-axis).

        Returns:
        tuple: A tuple containing the limits and ticks for the axis.
        """
        if axis == 0:
            ticks = self.xticks
        else:
            ticks = self.yticks

        if isinstance(ticks, int):
            max = 0
            if self.data.shape[0] > 0:
                max = numpy.maximum(int(numpy.round(1.1 * numpy.max(self.data[:, axis]))), 0)
            max += (ticks - max % ticks)
            lim = [0, max]
            ticks = numpy.arange(lim[0], lim[1] + 1, (lim[1] - lim[0]) // ticks)
        else:
            lim = [numpy.min(ticks), numpy.max(ticks)]

        return lim, ticks

    def draw_grid(self, screen):
        """
        Draw the grid for the graph.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        if self.cached_grid is None or self.needs_update:
            self.cached_grid = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.rect(self.cached_grid, utils.color('black'), (self.left + self.border, self.top + self.border, self.width - 2 * self.border, self.height - 2 * self.border), 3)

            xlim, xticks = self.get_lim_and_ticks(0)
            ylim, yticks = self.get_lim_and_ticks(1)

            # Draw grid lines and tick markers
            for i, xtick in enumerate(xticks):
                x = int(self.left + self.border + (xtick - xlim[0]) / (xlim[1] - xlim[0]) * (self.width - 2 * self.border))
                pygame.draw.line(self.cached_grid, utils.color('gray'), (x, self.top + self.border), (x, self.top + self.height - self.border), 1)
                if i % 5 == 0:
                    label = self.font.render(f'{int(xtick)}', True, (0, 0, 0))
                    self.cached_grid.blit(label, (x - label.get_width() // 2, self.top + self.height - self.border))

            for i, ytick in enumerate(yticks):
                y = int(self.top + self.height - self.border - (ytick - ylim[0]) / (ylim[1] - ylim[0]) * (self.height - 2 * self.border))

                pygame.draw.line(self.cached_grid, utils.color('gray'), (self.left + self.border, y), (self.left + self.width - self.border, y), 1)
                if i % 5 == 0:
                    label = self.font.render(f'{int(ytick)}', True, (0, 0, 0))
                    self.cached_grid.blit(label, (self.left + self.border - label.get_width() - 5, y - label.get_height() // 2))

            # x and y axis labels
            label = self.font.render(self.xlabel, True, (0, 0, 0))
            self.cached_grid.blit(label, (self.left + (self.width - label.get_width()) // 2, self.top + self.height - self.border + 20))

            label = self.font.render(self.ylabel, True, (0, 0, 0))
            label = pygame.transform.rotate(label, 90)
            self.cached_grid.blit(label, (self.left + self.border - label.get_width() - 30, self.top + (self.height - label.get_height()) // 2))

        screen.blit(self.cached_grid, (0, 0))

    def draw(self, screen):
        """
        Draw the graph on the screen.

        Parameters:
        screen (pygame.Surface): The screen to draw on.
        """
        self.draw_grid(screen)

        if self.data.shape[0] > 1:
            screen_coords = self.to_screen_coordinates(self.data)
            pygame.draw.aalines(screen, self.linecolor, False, screen_coords, 2)

        self.needs_update = False
