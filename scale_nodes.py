import getopt
import sys

"""
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
"""


def write_pre_node_lines(inp_file_handle, new_inp_file_handle):
    """
    copy all lines form old inp file to new inp file
    stop when reaching the *Node section
    :param inp_file_handle: file handle object for old inp file
    :param new_inp_file_handle: file handle object for new inp file
    :return:
    """
    while True:
        try:
            line = inp_file_handle.next()
        except StopIteration:
            raise Exception("end of file reached without finding node line")
        new_inp_file_handle.write(line)
        if line.startswith('*Node\n'):
            break
    return


def write_node_lines(inp_file_handle,
                     new_inp_file_handle,
                     x_factor,
                     y_factor,
                     z_factor):
    """
    copy the lines of the node section from the old inp to the new inp,
    but scale the nodal coordinates in each direction by the specified factors
    :param inp_file_handle: file handle object of old inp file
    :param new_inp_file_handle: file handle object of new inp file
    :param x_factor: factor by which to multiply node x coordinates
    :param y_factor: factor by which to multiply node y coordinates
    :param z_factor: factor by which to multiply node z coordinates
    :return:
    """
    while True:
        try:
            line = inp_file_handle.next()
        except StopIteration:
            raise Exception("end of file reached without finding node line")
        if line.startswith('*'):
            new_inp_file_handle.write(line)
            break
        scaled_line = scale_node_line(line, x_factor, y_factor, z_factor)
        new_inp_file_handle.write(scaled_line)
    return


def write_post_node_lines(inp_file_handle, new_inp_file_handle):
    """
    copy all remaining lines from the old inp file to the new inp file
    :param inp_file_handle: file handle object for old inp file
    :param new_inp_file_handle: file handle object for new inp file
    :return:
    """
    while True:
        try:
            new_inp_file_handle.write(inp_file_handle.next())
        except StopIteration:
            break
    return


def scale_node_line(line, x_factor, y_factor, z_factor):
    """
    scale the three nodal coordinates in a given inp file line by the
    specified factors
    :param line: line of text defining nodes from an inp file
    :param x_factor: factor by which to multiply node x coordinates
    :param y_factor: factor by which to multiply node y coordinates
    :param z_factor: factor by which to multiply node z coordinates
    :return new_line: line of text with the nodal coordinates adjusted
    """
    line_parts = line.rstrip().split(',')
    node = line_parts[0]
    x = float(line_parts[1]) * x_factor
    y = float(line_parts[2]) * y_factor
    z = float(line_parts[3]) * z_factor
    new_line = '{0},{1},{2},{3}\n'.format(node, x, y, z)
    return new_line


def scale_inp(inp_file, new_inp_file, x_factor, y_factor, z_factor):
    """
    essentially the main function for this module.
    :param inp_file: path to the old inp file
    :param new_inp_file: path to the new inp file
    :param x_factor: factor by which to multiply node x coordinates
    :param y_factor: factor by which to multiply node y coordinates
    :param z_factor: factor by which to multiply node z coordinates
    :return:
    """
    with open(inp_file, 'r') as f:
        with open(new_inp_file, 'w') as g:
            write_pre_node_lines(f, g)
            write_node_lines(f, g, x_factor, y_factor, z_factor)
            write_post_node_lines(f, g)
    return


def main(argv):
    """
    parse command line arguments and call scale_inp()
    :param argv:
    :return:
    """
    # dummy values
    old_inp_file_path = ''
    new_inp_file_path = ''
    x_factor = 1
    y_factor = 1
    z_factor = 1
    try:
        opts, args = getopt.getopt(argv, "i:n:x:y:z:")
    except getopt.GetoptError:
        print("inp_editor.py -i <inp_file> -n <new_inp_file> -x "
              "<x_scaling_factor> -y <y_scaling_factor> -z <z_scaling_factor>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            old_inp_file_path = arg
        elif opt == '-n':
            new_inp_file_path = arg
        elif opt == '-x':
            x_factor = float(arg)
        elif opt == '-y':
            y_factor = float(arg)
        elif opt == '-z':
            z_factor = float(arg)
    scale_inp(old_inp_file_path,
              new_inp_file_path,
              x_factor,
              y_factor,
              z_factor)
    return


if __name__ == '__main__':
    default_old_inp_file = 'misaligned_large_geom1B.inp'
    default_new_inp_file = 'scale_test.inp'
    default_x_scale = .001
    default_y_scale = .001
    default_z_scale = .001
    if not sys.argv[1:]:
        cl_argv = ['-i', default_old_inp_file,
                   '-n', default_new_inp_file,
                   '-x', default_x_scale,
                   '-y', default_y_scale,
                   '-z', default_z_scale]
    else:
        cl_argv = sys.argv[1:]
    main(cl_argv)
