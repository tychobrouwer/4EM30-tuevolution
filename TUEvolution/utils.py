import numpy, matplotlib.colors

def color(color_name):
    """
    Convert a color name to an RGB tuple.

    Parameters:
    color_name (str): The name of the color.

    Returns:
    tuple: A tuple representing the RGB values of the color.
    """
    return tuple(int(255*v) for v in matplotlib.colors.to_rgb(color_name))

def orientation_vector(θ):
    """
    Calculate the orientation vector for a given angle.

    Parameters:
    θ (float): The angle in radians.

    Returns:
    numpy.ndarray: A numpy array representing the orientation vector.
    """
    return numpy.array([numpy.cos(θ),numpy.sin(θ)])