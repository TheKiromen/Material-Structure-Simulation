import os

import microstructpy.meshing
import numpy as np
from PIL import Image
from matplotlib import image as mpim
from matplotlib import pyplot as plt

import microstructpy as msp


def generateMesh():
    # Read in image
    image_basename = 'output/mesh_src.png'
    image_path = os.path.dirname(__file__)
    # Create full image path
    image_filename = os.path.join(image_path, image_basename)
    # Read the image
    image = mpim.imread(image_filename)
    # Get image brightness values from Red channel
    im_brightness = image[:, :, 0]

    # Binary thresholds
    br_bins = [0.00, 0.50, 1.00]

    # Create empty copy of image
    bin_nums = np.zeros_like(im_brightness, dtype='int')
    # Bin the pixels
    for i in range(len(br_bins) - 1):
        # Get upper and lower bounds
        lb = br_bins[i]
        ub = br_bins[i + 1]
        # Check pixel value
        mask = np.logical_and(im_brightness >= lb, im_brightness <= ub)
        # Set pixel to 0 or 1
        bin_nums[mask] = i

    # Define the phases
    phases = [{'color': c, 'material_type': 'amorphous'} for c in ('C0', 'C1')]

    # Create the polygon mesh
    # Get image dimensions
    m, n = bin_nums.shape
    # Create x component
    x = np.arange(n + 1).astype('float')
    # Create y component
    y = m + 1 - np.arange(m + 1).astype('float')
    # Create coordinate maps
    xx, yy = np.meshgrid(x, y)
    # Create list of points in the image
    pts = np.array([xx.flatten(), yy.flatten()]).T
    # Get point indexes
    kps = np.arange(len(pts)).reshape(xx.shape)

    # Get number of edges?
    n_facets = 2 * (m + m * n + n)
    # Get number of elements/pixels
    n_regions = m * n
    # Generate edges array
    facets = np.full((n_facets, 2), -1)
    # Generate regions array
    regions = np.full((n_regions, 4), 0)
    # Generate phase of each region
    region_phases = np.full(n_regions, 0)

    # Generate face edges
    facet_top = np.full((m, n), -1, dtype='int')
    facet_bottom = np.full((m, n), -1, dtype='int')
    facet_left = np.full((m, n), -1, dtype='int')
    facet_right = np.full((m, n), -1, dtype='int')

    # Number of edges and regions
    k_facets = 0
    k_regions = 0
    # Iterate through the image
    for i in range(m):
        for j in range(n):
            # Get points of each face
            kp_top_left = kps[i, j]
            kp_bottom_left = kps[i + 1, j]
            kp_top_right = kps[i, j + 1]
            kp_bottom_right = kps[i + 1, j + 1]

            # left facet
            if facet_left[i, j] < 0:
                fnum_left = k_facets
                facets[fnum_left] = (kp_top_left, kp_bottom_left)
                k_facets += 1

                if j > 0:
                    facet_right[i, j - 1] = fnum_left
            else:
                fnum_left = facet_left[i, j]

            # right facet
            if facet_right[i, j] < 0:
                fnum_right = k_facets
                facets[fnum_right] = (kp_top_right, kp_bottom_right)
                k_facets += 1

                if j + 1 < n:
                    facet_left[i, j + 1] = fnum_right
            else:
                fnum_right = facet_right[i, j]

            # top facet
            if facet_top[i, j] < 0:
                fnum_top = k_facets
                facets[fnum_top] = (kp_top_left, kp_top_right)
                k_facets += 1

                if i > 0:
                    facet_bottom[i - 1, j] = fnum_top
            else:
                fnum_top = facet_top[i, j]

            # bottom facet
            if facet_bottom[i, j] < 0:
                fnum_bottom = k_facets
                facets[fnum_bottom] = (kp_bottom_left, kp_bottom_right)
                k_facets += 1

                if i + 1 < m:
                    facet_top[i + 1, j] = fnum_bottom
            else:
                fnum_bottom = facet_bottom[i, j]

            # Create region from edges
            region = (fnum_top, fnum_left, fnum_bottom, fnum_right)
            # Add region to list
            regions[k_regions] = region
            # Assign phase to the region
            region_phases[k_regions] = bin_nums[i, j]
            # Increase current number of regions
            k_regions += 1

    # Generate mesh from acquired points, edges and regions.
    pmesh = msp.meshing.PolyMesh(pts, facets, regions,
                                 seed_numbers=range(n_regions),
                                 phase_numbers=region_phases)

    # Create the triangle mesh from polygon mesh
    tmesh = msp.meshing.TriMesh.from_polymesh(pmesh, phases=phases, min_angle=20)

    # Graph configuration for plotting the result
    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    fig.add_axes(ax)

    # Get faces and phases from the mesh
    fcs = [phases[region_phases[r]]['color'] for r in tmesh.element_attributes]
    # Plot the mesh
    tmesh.plot(facecolors=fcs, edgecolors='k', lw=0.2)

    # Plot the polymesh
    # pmesh.plot(edgecolors='k')

    # Configure both plot axis
    plt.axis('square')
    plt.xlim(x.min(), x.max())
    plt.ylim(y.min(), y.max())
    plt.axis('off')

    # Save plot and copy input file
    plot_basename = 'output/mesh.png'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    # Get final image path
    filename = os.path.join(file_dir, plot_basename)
    dirs = os.path.dirname(filename)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # Save the plot image
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)

    # Resize mesh image to fit GUI
    mesh_img = Image.open(r"output/mesh.png")
    mesh_img = mesh_img.resize((300, 300))
    mesh_img.save(r"output/mesh.png")

    # Save data to abaqus format
    filename = os.path.join(file_dir, 'output/abaqus_input.inp')
    tmesh.write(filename, 'abaqus', None, pmesh)

    # TODO load the file, delete ext surfaces, override the file
