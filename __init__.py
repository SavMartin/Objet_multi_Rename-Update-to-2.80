# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "MultiRename",
    "author": "Maximilian Eham , (Port to 2.80 by Sav Martin)",
    "version": (0,2),
    "blender": (2, 80, 0),
    "api": 33588,
    "location": "View3D > Tools > MultiRename",
    "description": "Provides a find & replace function for renaming multiple objects and bones",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}


import re, fnmatch

import bpy

class VIEW3D_PT_tools_multiobjectrename(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_label = "Renamer"
    bl_category = "Renamer"
    

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("object.multi_object_rename")


class VIEW3D_PT_tools_multibonerename(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "armature_edit"
    bl_label = "Renamer"
    bl_category = "Renamer"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("object.multi_object_rename")


class VIEW3D_PT_tools_multiposebonerename(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "posemode"
    bl_label = "Renamer"
    bl_category = "Renamer"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("object.multi_object_rename")

def doSingleObjectRename(object, eraseString, replacementString, trimStart, trimEnd, newPrefix, newSuffix):
    temp = object.name[trimStart:]
    if trimEnd > 0:
        temp = temp[:-trimEnd]
    temp = re.sub(eraseString, replacementString, temp)
    temp = newPrefix + temp + newSuffix
    object.name = temp[:]
    

def doMultiObjectRename(context, eraseString, replacementString, trimStart, trimEnd, newPrefix, newSuffix):

# eliminar wildcards con regex:
    if "." in eraseString:
        regexRule = '(^.*)(\.[0-9]*?)$'
        resultado = re.search(regexRule, eraseString)
        if resultado:
            eraseString = resultado.group(1)


    if context.mode == 'EDIT_ARMATURE':
        for bone in context.selected_bones:
            doSingleObjectRename(bone, eraseString, replacementString, trimStart, trimEnd, newPrefix, newSuffix)

    elif context.mode == 'OBJECT':
        for obj in bpy.context.selected_objects:
            doSingleObjectRename(obj, eraseString, replacementString, trimStart, trimEnd, newPrefix, newSuffix)
        
    elif context.mode == 'POSE':
        for bone in context.selected_pose_bones:
            doSingleObjectRename(bone, eraseString, replacementString, trimStart, trimEnd, newPrefix, newSuffix)


class OBJECT_OT_MultiObjectRename(bpy.types.Operator):
    '''Find & Replace-functionality for names'''
    bl_idname = "object.multi_object_rename"
    bl_label = "Rename Objects"
    bl_description = "Find & Replace-functionality for object names and bone names"
    bl_options = {'REGISTER', 'UNDO'}

    eraseString : bpy.props.StringProperty(name="Find String",
        description = "The string to look for in the object names (shell wildcards supported)",
        )

    replacementString : bpy.props.StringProperty(name = "Replace with",
        description = "The replacement for the string given above",
        )
    
    trimStart : bpy.props.IntProperty(name="Trim Start:",
        description = "Erases the specified number of characters from the beginning of the object names",
        min = 0,
        max = 50,
        default = 0,
        )

    trimEnd : bpy.props.IntProperty(name="Trim End:",
        description = "Erases the specified number of characters from the end of the object names",
        min = 0,
        max = 50,
        default = 0,
        )

    newPrefix : bpy.props.StringProperty(name = "Prefix with",
        description = "Adds the specified characters to the beginning of the object names",
        )

    newSuffix : bpy.props.StringProperty(name = "Suffix with",
        description = "Adds the specified characters to the end of the object names",
        )

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects != []

    def execute(self, context):
        doMultiObjectRename(context, self.eraseString, self.replacementString,
            self.trimStart, self.trimEnd,
            self.newPrefix, self.newSuffix)
        return {'FINISHED'}

classes = (
    OBJECT_OT_MultiObjectRename,
    VIEW3D_PT_tools_multiposebonerename,
    VIEW3D_PT_tools_multibonerename,
    VIEW3D_PT_tools_multiobjectrename
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    pass

def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    pass
if __name__ == "__main__":
    register()


