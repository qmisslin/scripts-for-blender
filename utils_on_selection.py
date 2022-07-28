# Copyright 2022 Quentin Misslin
# You may use, distribute and modify this code under the
# terms of the MIT license :
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following 
# conditions:
# The above copyright notice and this permission notice shall 
# be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.
#

import bpy
import mathutils
import os

class Utils():
    
    # Define whether the action is active or not
    place_origin = True
    apply_transformation = True
    export_to_gltf = True
    export_to_gltf_copyright = ""
    
    # Main function to make action on all selected objects
    def __init__(self):
        
        # Get all selected objects
        selected_objects = Utils.get_selected_objects()
        
        # Loop on all selected objects to set origin
        for object in selected_objects:
            
            # Unselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select only the relevant object
            object.select_set(True)    
            bpy.context.view_layer.objects.active = object
            
            # Execute actions on object
            if(self.apply_transformation):
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            if(self.place_origin):
                origin = Utils.compute_floor_origin(object)
                Utils.set_selected_object_origin(origin)
                
            if(self.export_to_gltf):
                if not Utils.export_selected_object_to_gltf(self.export_to_gltf_copyright):
                    
                    # Retrive previous selection before quit
                    Utils.set_selected_objects(selected_objects)
                    return
            
        # Return to the previous selection once all actions have been completed
        Utils.set_selected_objects(selected_objects)
        
        # Display final message
        Utils.display_message("Operation successfully completed", "Info")
        
    # Function to display message
    @staticmethod
    def display_message(message, title="Info", icon="MONKEY"):
        
        # Create callback function called by popup event
        callback = lambda self, context: self.layout.label(text=message)
        
        # Call popup event
        bpy.context.window_manager.popup_menu(callback, title=title, icon=icon)


    # Function to export selected object in GLTF
    @staticmethod
    def export_selected_object_to_gltf(copyright):
        
        # Get selected object
        object = bpy.context.view_layer.objects.active

        # Save object position
        location = object.location.copy()
        
        # Reset object position
        bpy.ops.object.location_clear(clear_delta=False)
        
        # Compute file path
        base_dir = bpy.path.abspath("//")
        if not base_dir:
            Utils.display_message("Cannot export elements because Blend file is not saved.", "Error", "ERROR")
            return False
        name = bpy.path.clean_name(object.name)
        out_dir = base_dir + "exported_items"
        print("Export item in " + out_dir)
        filepath = os.path.join(out_dir, name)
        
        # Create sub folder for all exported items
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)        
        
        # Export to GLTF
        bpy.ops.export_scene.gltf(
            filepath=filepath + '.gltf', 
            check_existing=True, 
            export_format='GLTF_EMBEDDED', 
            ui_tab='GENERAL', 
            export_copyright=copyright, 
            export_image_format='AUTO', 
            export_texture_dir='', 
            export_keep_originals=False, 
            export_texcoords=True, 
            export_normals=True, 
            export_draco_mesh_compression_enable=False, 
            export_draco_mesh_compression_level=6, 
            export_draco_position_quantization=14, 
            export_draco_normal_quantization=10, 
            export_draco_texcoord_quantization=12, 
            export_draco_color_quantization=10, 
            export_draco_generic_quantization=12, 
            export_tangents=False, 
            export_materials='EXPORT', 
            export_colors=True, 
            use_mesh_edges=False, 
            use_mesh_vertices=False, 
            export_cameras=False, 
            use_selection=True, 
            use_visible=False, 
            use_renderable=False, 
            use_active_collection=False, 
            export_extras=False, 
            export_yup=True, 
            export_apply=False, 
            export_animations=True, 
            export_frame_range=True, 
            export_frame_step=1, 
            export_force_sampling=True, 
            export_nla_strips=True, 
            export_def_bones=False, 
            optimize_animation_size=False, 
            export_current_frame=False, 
            export_skins=True, 
            export_all_influences=False, 
            export_morph=True, 
            export_morph_normal=True, 
            export_morph_tangent=False, 
            export_lights=False, 
            export_displacement=False, 
            will_save_settings=False, 
            filter_glob='*.glb;*.gltf')
            
        # Revert initial object position
        object.location = location
        
        return True

    # Function to set origin of an object
    @staticmethod
    def set_selected_object_origin(origin):
        
        # Placing 3D cursor
        bpy.context.scene.cursor.location = origin
        
        # Set origin of object
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')


    # Function to place origin in the center floor of object
    @staticmethod
    def compute_floor_origin(object):
        
        # Get local coordinates of object bounding box
        box_coords = [mathutils.Vector(v[:]) for v in object.bound_box]
        
        # Get middle coordinates of floor face in box (index 0, 3, 4 & 7)
        middle_floor = (box_coords[0] + box_coords[3] + box_coords[4] + box_coords[7]) / 4
        
        # Convert local coordinates to world coordinates
        origin = object.matrix_world @ middle_floor
        
        return origin

    # Function to get all selected objects
    @staticmethod
    def get_selected_objects(): 
        
        return [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
    # Function to select all object in a list
    @staticmethod
    def set_selected_objects(objects):
        
        [o.select_set(True) for o in objects]


execute = Utils()
