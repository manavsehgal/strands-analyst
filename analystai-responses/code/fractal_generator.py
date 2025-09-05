import numpy as np
import matplotlib.pyplot as plt
from numba import jit, prange
from matplotlib.colors import LinearSegmentedColormap
import time

# Use Numba's just-in-time compilation to significantly speed up the computation
@jit(nopython=True, parallel=True)
def mandelbrot(width, height, max_iters, x_min=-2.0, x_max=0.8, y_min=-1.4, y_max=1.4):
    """
    Compute the Mandelbrot fractal for a given height and width.
    Uses Numba for significant performance improvement.
    """
    # Create the pixel grid
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    
    # Create the output array
    output = np.zeros((height, width), dtype=np.int32)
    
    # Compute the Mandelbrot set
    for i in prange(width):
        for j in range(height):
            c = complex(real[i], imag[j])
            z = 0.0j
            for k in range(max_iters):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    output[j, i] = k
                    break
                    
    return output

@jit(nopython=True, parallel=True)
def julia(width, height, c, max_iters, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
    """
    Compute the Julia set for a given complex parameter c.
    Uses Numba for significant performance improvement.
    """
    # Create the pixel grid
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    
    # Create the output array
    output = np.zeros((height, width), dtype=np.int32)
    
    # Compute the Julia set
    for i in prange(width):
        for j in range(height):
            z = complex(real[i], imag[j])
            for k in range(max_iters):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    output[j, i] = k
                    break
                    
    return output

@jit(nopython=True, parallel=True)
def burning_ship(width, height, max_iters, x_min=-2.5, x_max=1.5, y_min=-1.8, y_max=1.8):
    """
    Compute the Burning Ship fractal.
    Uses Numba for significant performance improvement.
    """
    # Create the pixel grid
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    
    # Create the output array
    output = np.zeros((height, width), dtype=np.int32)
    
    # Compute the Burning Ship fractal
    for i in prange(width):
        for j in range(height):
            c = complex(real[i], imag[j])
            z = 0.0j
            for k in range(max_iters):
                z = complex(abs(z.real), abs(z.imag))**2 + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    output[j, i] = k
                    break
                    
    return output

def create_colormap(name="viridis_mod"):
    """Create a custom colormap for better visualization"""
    if name == "fire":
        colors = [(0, 0, 0), (0.5, 0, 0), (1, 0.5, 0), (1, 1, 0.5), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(name, colors)
    elif name == "electric":
        colors = [(0, 0, 0), (0, 0, 0.5), (0, 0.5, 1), (0.5, 1, 1), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(name, colors)
    elif name == "cosmic":
        colors = [(0, 0, 0), (0.3, 0, 0.5), (0.6, 0, 1), (0.9, 0.5, 1), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(name, colors)
    elif name == "viridis_mod":
        colors = [(0, 0, 0), (0, 0.1, 0.2), (0, 0.4, 0.4), (0.2, 0.6, 0.5), (0.5, 0.8, 0.5), (1, 1, 0.5)]
        return LinearSegmentedColormap.from_list(name, colors)
    elif name == "deep_sea":
        colors = [(0, 0, 0), (0, 0.05, 0.1), (0, 0.1, 0.2), (0, 0.15, 0.4), (0, 0.2, 0.6), (0, 0.4, 0.8), (0.5, 0.7, 1.0)]
        return LinearSegmentedColormap.from_list(name, colors)
    else:
        return plt.cm.viridis

def generate_fractal(fractal_type="mandelbrot", width=1000, height=1000, max_iters=100, 
                     cmap="viridis_mod", c=-0.7+0.27j, filename=None,
                     x_min=None, x_max=None, y_min=None, y_max=None):
    """
    Generate and display a fractal image.
    
    Parameters:
    - fractal_type: Type of fractal ("mandelbrot", "julia", "burning_ship")
    - width, height: Dimensions of the output image
    - max_iters: Maximum number of iterations for the fractal calculation
    - cmap: Colormap to use for visualization
    - c: Complex parameter for Julia sets
    - filename: If provided, save the image to this file
    - x_min, x_max, y_min, y_max: Custom view boundaries
    """
    start_time = time.time()
    
    # Set default boundaries if not provided
    if fractal_type == "mandelbrot":
        x_min = x_min if x_min is not None else -2.0
        x_max = x_max if x_max is not None else 0.8
        y_min = y_min if y_min is not None else -1.4
        y_max = y_max if y_max is not None else 1.4
        
        # Create the fractal data
        fractal_data = mandelbrot(width, height, max_iters, x_min, x_max, y_min, y_max)
        
    elif fractal_type == "julia":
        x_min = x_min if x_min is not None else -1.5
        x_max = x_max if x_max is not None else 1.5
        y_min = y_min if y_min is not None else -1.5
        y_max = y_max if y_max is not None else 1.5
        
        # Create the fractal data
        fractal_data = julia(width, height, c, max_iters, x_min, x_max, y_min, y_max)
        
    elif fractal_type == "burning_ship":
        x_min = x_min if x_min is not None else -2.5
        x_max = x_max if x_max is not None else 1.5
        y_min = y_min if y_min is not None else -1.8
        y_max = y_max if y_max is not None else 1.8
        
        # Create the fractal data
        fractal_data = burning_ship(width, height, max_iters, x_min, x_max, y_min, y_max)
        
    else:
        raise ValueError(f"Unknown fractal type: {fractal_type}")
    
    compute_time = time.time() - start_time
    print(f"Fractal computation time: {compute_time:.2f} seconds")
    
    # Create the figure and plot the fractal
    plt.figure(figsize=(10, 10))
    
    # Use custom colormap if specified
    if isinstance(cmap, str) and cmap in ["fire", "electric", "cosmic", "viridis_mod", "deep_sea"]:
        colormap = create_colormap(cmap)
    else:
        colormap = cmap
    
    plt.imshow(fractal_data, cmap=colormap, origin='lower')
    plt.axis('off')
    
    # Add title with fractal type and parameters
    if fractal_type == "julia":
        title = f"{fractal_type.capitalize()} Set (c={c})"
    else:
        title = f"{fractal_type.capitalize()} Set"
    
    title += f" - {width}x{height}, {max_iters} iterations"
    plt.title(title)
    
    # Save the image if a filename is provided
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved fractal image to {filename}")
    
    plt.tight_layout()
    plt.show()
    
    total_time = time.time() - start_time
    print(f"Total time (compute + plot): {total_time:.2f} seconds")
    
    return fractal_data

if __name__ == "__main__":
    print("Fractal Generator")
    print("Available fractal types: 'mandelbrot', 'julia', 'burning_ship'")
    print("Available colormaps: 'fire', 'electric', 'cosmic', 'viridis_mod', 'deep_sea'")
    
    # Example usage:
    # generate_fractal("mandelbrot", width=1200, height=1200, max_iters=200, cmap="cosmic", filename="mandelbrot.png")
    # generate_fractal("julia", width=1200, height=1200, max_iters=300, cmap="fire", c=-0.8+0.156j, filename="julia.png")
    # generate_fractal("burning_ship", width=1200, height=1200, max_iters=200, cmap="electric", filename="burning_ship.png")
    
    # Zoomed-in example:
    # generate_fractal("mandelbrot", width=1500, height=1500, max_iters=500, cmap="deep_sea", 
    #                  x_min=-0.748, x_max=-0.742, y_min=0.1, y_max=0.106, filename="mandelbrot_zoom.png")