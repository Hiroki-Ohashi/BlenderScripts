import bpy

# モジュールのインポート
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .ico_sphere import MYADDON_OT_create_ico_sphere
from .collider import MYADDON_OT_add_collider
from .collider import OBJECT_PT_collider
from .collider import DrawCollider
from .file import MYADDON_OT_add_filename
from .file import OBJECT_PT_file_name
from .scene import MYADDON_OT_export_scene
from .my_menu import TOPBAR_MT_my_menu
from .disabled import MYADDON_OT_add_disabled
from .disabled import OBJECT_PT_disabled
from .spawn import MYADDON_OT_spawn_point_symbol
from .spawn import MYADDON_OT_create_spawn_point_symbol
from .spawn import MYADDON_OT_create_player_spawn_point_symbol
from .spawn import MYADDON_OT_create_enemy_spawn_point_symbol

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Hiroki Ohashi",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    MYADDON_OT_add_disabled,
    TOPBAR_MT_my_menu,
    OBJECT_PT_file_name,
    OBJECT_PT_collider,
    OBJECT_PT_disabled,
    MYADDON_OT_spawn_point_symbol,
    MYADDON_OT_create_spawn_point_symbol,
    MYADDON_OT_create_player_spawn_point_symbol,
    MYADDON_OT_create_enemy_spawn_point_symbol,
)

# アドオン有効化時コールバック
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)
    # メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")
    print("レベルエディタが有効化されました。")

# アドオン無効化時コールバック
def unregister():
    # メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました。")
    
# テスト実行用コード
if __name__ == "__main__":
    register()