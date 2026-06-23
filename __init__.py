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
    "name": "Import as Asset",
    "author": "tintwotin",
    "version": (1, 1),
    "blender": (5, 2, 0),
    "location": "Add > Import as Asset",
    "description": "Import movie, sound and image files as Assets",
    "warning": "",
    "doc_url": "",
    "category": "Sequencer",
}

import bpy
import os
from bpy.types import Operator, OperatorFileListElement
from bpy_extras.io_utils import ImportHelper
from bpy.props import CollectionProperty, StringProperty


class OPERATOR_OT_import_as_assets(Operator, ImportHelper):
    """Import movie, sound and image files as Assets"""

    bl_idname = "sequencer.import_as_asset"
    bl_label = "Import as Asset"
    bl_options = {"REGISTER", "UNDO"}

    directory: StringProperty(subtype='DIR_PATH')
    files: CollectionProperty(type=OperatorFileListElement)

    def draw(self, context):
        st = context.space_data
        params = st.params
        if params:
            params.use_filter = True
            params.use_filter_movie = True
            params.use_filter_sound = True
            params.use_filter_image = True

    def execute(self, context):
        # Resolve import directory path robustly
        dirname = self.directory if self.directory else os.path.dirname(self.filepath)

        for f in self.files:
            path = os.path.join(dirname, f.name)
            path = bpy.path.abspath(path)
            print(f"Importing: {path}")
            
            _, file_extension = os.path.splitext(path)
            file_extension = file_extension.lower()

            # --- SOUND FILES ---
            if file_extension in {
                ".wav", ".ogg", ".oga", ".mp3", ".mp2", ".ac3", ".aac",
                ".flac", ".wma", ".eac3", ".aif", ".aiff", ".m4a", ".mka",
            }:
                try:
                    my_sound = bpy.data.sounds.load(path)
                    my_sound.asset_mark()
                    my_sound.asset_generate_preview()
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to load sound: {f.name} ({e})")

            # --- IMAGE FILES ---
            if file_extension in {
                ".png", ".tga", ".bmp", ".jpg", ".jpeg", ".sgi", ".rgb",
                ".rgba", ".tif", ".tiff", ".tx", ".jp2", ".j2c", ".hdr",
                ".dds", ".dpx", ".cin", ".exr", ".psd", ".pdd", ".psb",
                ".webp",
            }:
                try:
                    my_image = bpy.data.images.load(path)
                    my_image.asset_mark()
                    my_image.asset_generate_preview()
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to load image: {f.name} ({e})")

            # --- MOVIE FILES ---
            if file_extension in {
                ".avi", ".flc", ".mov", ".movie", ".mp4", ".m4v", ".m2v",
                ".m2t", ".m2ts", ".mts", ".ts", ".mv", ".avs", ".wmv",
                ".ogv", ".ogg", ".r3d", ".dv", ".mpeg", ".mpg", ".mpg2",
                ".vob", ".mkv", ".flv", ".divx", ".xvid", ".mxf", ".webm",
            }:
                try:
                    my_movie = bpy.data.movieclips.load(path)
                    my_movie.asset_mark()
                    my_movie.asset_generate_preview()
                except Exception as e:
                    self.report({'WARNING'}, f"Failed to load movie clip: {f.name} ({e})")

        return {"FINISHED"}


def menu_append(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OPERATOR_OT_import_as_assets.bl_idname, icon="ASSET_MANAGER")


def register():
    bpy.utils.register_class(OPERATOR_OT_import_as_assets)
    bpy.types.SEQUENCER_MT_add.append(menu_append)


def unregister():
    bpy.utils.unregister_class(OPERATOR_OT_import_as_assets)
    bpy.types.SEQUENCER_MT_add.remove(menu_append)


if __name__ == "__main__":
    register()
