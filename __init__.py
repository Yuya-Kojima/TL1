import bpy

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "Level Editor",
    "author": "Yuya Kojima",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "Level Editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# -----------------
# 各モジュールのインポート
# -----------------
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .export_scene import MYADDON_OT_export_scene
from .add_filename import MYADDON_OT_add_filename
from .add_collider import MYADDON_OT_add_collider
from .file_name import OBJECT_PT_file_name
from .collider import OBJECT_PT_collider
from .my_menu import TOPBAR_MT_my_menu
from .draw_collider import DrawCollider
from .disabled import MYADDON_OT_add_disabled, OBJECT_PT_disabled
from .spawn import MYADDON_OT_spawn_import_symbol
from .spawn import MYADDON_OT_spawn_create_symbol

# -----------------
# Blenderに登録するクラスリスト
# -----------------
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
    OBJECT_PT_file_name,
    MYADDON_OT_add_filename, 
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    MYADDON_OT_add_disabled,
    OBJECT_PT_disabled,
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
)

# アドオン有効化時コールバック
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")
    print("レベルエディタが有効化されました。")

# アドオン無効化時コールバック
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました。")

if __name__ == "__main__":
    register()
