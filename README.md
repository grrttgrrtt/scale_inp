# scale_nodes
Module for scaling nodal coordinates within an .inp file. Does not affect
other units within the .inp file, such as material properties. Only operates
on nodal coordinates. Useful to scale an entire model in one direction,
or implicitly change units by changing the size of the model.

To use as a standalone, change the following variables in the block at the 
end of the file:
    default_old_inp_file: the path of the inp file you wish to modify
    default_new_inp_file: the path where the new inp file will be created
    default_x_scale: scaling factor for the x direction
    default_y_scale: scaling factor for the y direction
    default_z_scale: scaling factor for the z direction
        
To use from the command line, call node_snap.py with the following options 
corresponding to the variables listed above:
    -i: old_inp_file
    -n: new_inp_file
    -x: x_scale
    -y: y_scale
    -z: z_scale
    
To use from another module, import and call the function scale_inp() with 
the above options as arguments.
