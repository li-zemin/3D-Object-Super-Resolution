import numpy as np
import os 
def call(command):
    os.system('%s > /dev/null 2>&1' % command)

def voxel2mesh(voxels, threshold=0):
    cube_verts = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0],
                  [1, 1, 1]]  # 8 points

    cube_faces = [[0, 1, 2], [1, 3, 2], [2, 3, 6], [3, 7, 6], [0, 2, 6], [0, 6, 4], [0, 5, 1],
                  [0, 4, 5], [6, 7, 5], [6, 5, 4], [1, 7, 3], [1, 5, 7]]  # 12 face

    cube_verts = np.array(cube_verts)
    cube_faces = np.array(cube_faces) + 1

    scale = 0.01
    cube_dist_scale = 1.1
    verts = []
    faces = []
    curr_vert = 0
    a,b,c= np.where(voxels>threshold)
    for i,j,k in zip(a,b,c):
        try: 
            if voxels[i+1,j,k]<threshold or voxels[i-1,j,k]<threshold  or voxels[i,j+1,k]<threshold  or voxels[i,j-1,k]<threshold or voxels[i,j,k+1]<threshold or voxels[i,j,k-1]<threshold:
                verts.extend(scale * (cube_verts + cube_dist_scale * np.array([[i, j, k]])))
                faces.extend(cube_faces + curr_vert)
                curr_vert += len(cube_verts)
        except IndexError:
            verts.extend(scale * (cube_verts + cube_dist_scale * np.array([[i, j, k]])))
            faces.extend(cube_faces + curr_vert)
            curr_vert += len(cube_verts)
        
    

    return np.array(verts), np.array(faces)


def write_obj(filename, verts, faces):
    """ write the verts and faces on file."""
    with open(filename, 'w') as f:
        # write vertices
        f.write('g\n# %d vertex\n' % len(verts))
        for vert in verts:
            f.write('v %f %f %f\n' % tuple(vert))

        # write faces
        f.write('# %d faces\n' % len(faces))
        for face in faces:
            f.write('f %d %d %d\n' % tuple(face))


def voxel2obj(filename, pred, show='False', threshold=0.4):
    verts, faces = voxel2mesh(pred, threshold )
    
    write_obj(filename, verts, faces)
    call('meshlabserver -i ' + filename + ' -o ' + filename + ' -s scripts/mesh.mlx')
    call('meshlab ' + filename)