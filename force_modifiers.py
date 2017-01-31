#! /usr/bin/env python3
# -*- coding: utf-8 -*-

bl_info = {
    "name": "Force Modifiers",
    "author": "Squeaky",
    "version": (1 ,0),
    "blender": (2, 70, 0),
    "location": "3D View > Tools > Other > Force Modifiers",
    "description": "Applies modifiers on meshes with shape keys",
    "warning": "Applies the whole modifier stack; does not discriminate modifiers; does not work properly on objects with malformed (ie. spam.001) names.",
    "wiki_url": "",
    "category": "Object",
}

import bpy


def main(context):
    # Initialize variables, then copy object
    
    keyList = context.selected_objects[0].data.shape_keys.key_blocks.keys()
    ind = 1
    keys = []
    obName = context.selected_objects[0].name
    keyCount = len(keyList)
    
    while (ind != keyCount):
        keys.append(context.selected_objects[0].data.shape_keys.key_blocks[ind].name)
        ind = ind + 1
        
    dup = 1
    
    while (dup != keyCount):
        bpy.ops.object.duplicate_move()
        dup = dup + 1
        
    # Delete unneeded shapes
    
    dup = 0
    ind = 0
    ind2 = 0
    
    while (dup < keyCount):
        if (dup == 0):
            ob = obName
        elif (dup < 10):
            ob = obName + ".00" + str(dup)
        elif (dup < 100):
            ob = obName + ".0" + str(dup)
        else:
            ob = obName + str(dup)

        context.scene.objects.active = bpy.data.objects[ob]
        
        while (ind < keyCount):
            if (ind2 > dup):
                bpy.data.objects[ob].active_shape_key_index = ind2
                bpy.ops.object.shape_key_remove(all=False)
            else:
                ind2 = ind2 + 1
                
            ind = ind + 1
            
        ind = 0
        ind2 = 0
        
        while (ind < keyCount):
            if (ind < dup):
                bpy.data.objects[ob].active_shape_key_index = 0
                bpy.ops.object.shape_key_remove(all=False)
            elif (ind == dup):
                print("Done")

            ind = ind + 1

        ind = 0
        ind2 = 0
            
        dup = dup + 1

        
    dup = 1
    
    bpy.data.objects[obName].select = True
    context.scene.objects.active = bpy.data.objects[obName]
    
    ind2 = 1
    ind3 = 2
    
    #Merge shapes
    
    while (dup != keyCount):
        if (dup < 10):
            ob = obName + ".00" + str(dup)
        elif (dup < 100):
            ob = obName + ".0" + str(dup)
        else:
            ob = obName + str(dup)
        
        sh = keys[ind]
        
        ind = ind + 1
        
        bpy.data.objects[ob].name = sh
        bpy.data.objects[sh].select = True
        
        bpy.ops.object.convert(target = 'MESH')
        

        
        bpy.ops.object.join_shapes()

        
        bpy.data.objects[sh].select = False
        context.scene.objects.active = bpy.data.objects[obName]

        sh = ""
        dup = dup + 1
        
    while (ind3 < keyCount):
        bpy.data.objects[obName].active_shape_key_index = ind2

        bpy.ops.object.shape_key_remove(all=False)

        ind2 = ind2 + 1
        
        ind3 = ind3 + 1
    
    ind = 0
    dup = 1
    bpy.data.objects[obName].select = False
    
    while (dup < keyCount):
        sh = keys[ind]
        bpy.data.objects[sh].select = True
        context.scene.objects.active = bpy.data.objects[sh]
        bpy.ops.object.delete(use_global = False)
        ind = ind + 1
        dup = dup + 1

class mPanel(bpy.types.Panel):
    bl_label = "Force Modifiers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        self.layout.operator("object.force_modifiers", "Apply")

class ModForce(bpy.types.Operator):
    """Force Modifiers"""
    bl_idname = "object.force_modifiers"
    bl_label = "Force Modifiers"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ModForce)
    bpy.utils.register_class(mPanel)

def unregister():
    bpy.utils.unregister_class(ModForce)
    bpy.utils.unregister_class(mPanel)

if __name__ == "__main__":
    register()
