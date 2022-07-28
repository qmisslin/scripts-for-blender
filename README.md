# scripts-for-blender
Repository to list the different python scripts I use in Blender to automate certain tasks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## utils_on_selection.py

In this file, you will find the Utils class which allows 3 actions on a whole selection of objects (each object is treated one by one). These actions can be activated or not in the script.

Here are the 3 actions:
- To place the origin at the ground level of the object
- To apply a transformation on an object.
- To export an object in GLTF format.

To enable or disable these actions, you can change the values to "True" or "False" in the file header as follows. 
The "export_to_gltf_copyright" field defines the copyright that is assigned to each file during multiple export (you can put your name in quotes here, for example "qmisslin").
```python

import bpy
import mathutils
import os

class Utils():
    
    # Define whether the action is active or not
    place_origin = True
    apply_transformation = True
    export_to_gltf = True
    export_to_gltf_copyright = ""
    
```

## How to use ?

You can import the python file directly into Blender (tested on Blender 3.1.2) or copy/paste all the code into the "Text Editor" panel of Blender.
