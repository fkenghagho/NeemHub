#!/usr/bin/env python3
import open3d as o3d



def load():
    #Load the mesh from a file
    mesh = o3d.io.read_triangle_mesh("../TRACEBOT-NEEMS/Canister.obj")
    
    #check if the mesh has vertex normals and compute them if missing
    if not mesh.has_vertex_normals():
      mesh.compute_vertex_normals()
    """
    #Load the texture image
    texture_image1 = o3d.io.read_image("../TRACEBOT-NEEMS/canister_blue.png")
    
    #Assign the texture image to mesh
    mesh.textures = [texture_image,texture_image,texture_image]
    """
    #Display the mesh before applying any texture
    o3d.visualization.draw_geometries([mesh], mesh_show_wireframe=True)

if __name__ == '__main__':
    load()