from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation


"""
Basic vector processor testing
SO - 28/09/2026

"""
def angle_between(v1, v2):
    dot = np.dot(v1, v2)
    v1_mag = np.linalg.norm(v1)
    v2_mag = np.linalg.norm(v2)
    denom = v1_mag*v2_mag
    arg = np.clip(dot/denom, -1.0, 1.0)
    return np.arccos(arg)

def plot_vector(ax, v, color):
    return ax.quiver(0,0,0,v[0],v[1],v[2], color = color)

def plot_arc(ax, v1, v2, color='r', N = 150):
    u1 = v1/np.linalg.norm(v1)
    u2 = v2/np.linalg.norm(v2)
    theta = angle_between(v1,v2)
    nrm = np.cross(u1, u2)
    nrm /= np.linalg.norm(nrm)
    tang = np.cross(nrm,u1)

    points = np.linspace(0, theta, N)
    arc = 0.2*np.max([v1,v2]) * (np.outer(np.cos(points), u1) + np.outer(np.sin(points), tang))
    ax.plot(arc[:,0], arc[:,1], arc[:,2], 'm', linewidth=1, color=color)

    mid = arc[N//2]
    ax.text(mid[0], mid[1], mid[2], f'{np.degrees(theta):.1f}°')

def get_polyFaces(v1, v2, v3):
    if np.dot(v1, np.cross(v2,v3))==0:
        print("Vectors are not linearly independent!")

    v1_v2 = v1 + v2
    v1_v3 = v1 + v3
    v2_v3 = v2 + v3
    v1_v2_v3 = v1_v2 + v3

    faces = [
        [np.array([0, 0, 0]), v1, v1_v2, v2],
        [np.array([0, 0, 0]), v1, v1_v3, v3],
        [np.array([0, 0, 0]), v2, v2_v3, v3],
        [v1, v1_v2, v1_v2_v3, v1_v3],
        [v2, v1_v2, v1_v2_v3, v2_v3],
        [v3, v1_v3, v1_v2_v3, v2_v3],
    ]
    # poly = Poly3DCollection(
    #     faces,
    #     facecolors = 'skyblue',
    #     edgecolor = 'k',
    #     alpha = 0.3
    # )
    return faces

def vector_transform(v0, v1, frames):
    t = np.linspace(0,1,frames)
    return np.outer(v0,(1-t)) + np.outer(v1, t)

    

def main():
    plt.close('all')

    num_frames = 201
    # PLOTTING
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Input vectors
    A = np.array([1, 0, 0])
    B = np.array([0, 1, 0])
    C = np.array([0, 0, 1])
    vec = np.array([A,B,C])

    # init
    p1 = plot_vector(ax, A, 'r')
    p2 = plot_vector(ax, B, 'b')
    p3 = plot_vector(ax, C, 'g')
    ps = [p1, p2, p3]
    faces = get_polyFaces(A, B, C)
    poly = Poly3DCollection(
        faces,
        facecolors = 'skyblue',
        edgecolor = 'k',
        alpha = 0.3)
    ax.add_collection3d(poly)
    
    A1 = np.array([0, 1, 0.5])
    B1 = np.array([-0.5, 0.7, 0.7])
    C1 = np.array([-1, -0.3, 0])
    vec1 = np.array([A1,B1,C1])

    At = vector_transform(A,A1, num_frames)
    Bt = vector_transform(B,B1, num_frames)
    Ct = vector_transform(C,C1, num_frames)

    def update(frame):
        nonlocal ps
        # print(frame)
        A = At[:,frame]
        B = Bt[:,frame]
        C = Ct[:,frame]
        # for p in ps:
        #     p.remove()
        # ps = [
        # plot_vector(ax, A, 'r'),
        # plot_vector(ax, B, 'b'),
        # plot_vector(ax, C, 'g')
        # ]
        faces = get_polyFaces(A,B,C)
        poly.set_verts(faces)


    # Plot elements
    # plot_vector(ax, vec[0,:], 'r')
    # plot_vector(ax, vec[1,:], 'b')
    # plot_vector(ax, vec[2,:], 'g')
    # plot_arc(ax, A, B)
    # plot_arc(ax, B, C)
    # plot_arc(ax, C, A)
    # lim = plot_scalProd(ax, A, B, C)


    # # Plot Formatting
    # # lim = np.max(abs(vec))*1.25
    # ax.set_xlim(-lim, lim)
    # ax.set_ylim(-lim, lim)
    # ax.set_zlim(-lim, lim)
    # ax.set_box_aspect([1, 1, 1])
    # ax.set_proj_type('ortho')

    animation = FuncAnimation(
        fig,
        update,
        num_frames,
        interval=25,
        blit = False,
        repeat = True,

    )

    plt.show()
    
if __name__ == "__main__":
    main()