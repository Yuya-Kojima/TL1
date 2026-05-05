import bpy
import os

class SpawnNames():
    # インデックス
    PROTOTYPE = 0    # プロトタイプのオブジェクト名
    INSTANCE = 1     # 量産時のオブジェクト名
    FILENAME = 2     # リソースファイル名

    names = {}
    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["Enemy"] = ("PrototypeEnemySpawn", "EnemySpawn", "enemy/enemy.obj")
    names["Player"] = ("PrototypePlayerSpawn", "PlayerSpawn", "player/player.obj")


# オペレータ 共通の出現ポイントシンボル読み込み関数
class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}
    
    # 呼び出し元から渡されるtype ("Player" または "Enemy") を受け取るプロパティ
    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        # 既にロード済みならそのまま使用、未ロードならload_obj()を呼ぶ
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])
        if spawn_object is None:
            self.load_obj(self.type)
            spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])
            if spawn_object is None:
                self.report({'ERROR'}, f"{self.type}のシンボルモデル読み込みに失敗しました。")
                return {'CANCELLED'}

        print(f"出現ポイントのシンボルを作成します: {self.type}")
        # オブジェクトを複製
        bpy.ops.object.select_all(action='DESELECT')
        duplicate_object = spawn_object.copy()
        bpy.context.collection.objects.link(duplicate_object)
        
        # 複製したオブジェクトをアクティブにする
        duplicate_object.select_set(True)
        bpy.context.view_layer.objects.active = duplicate_object
        
        return {'FINISHED'}

    def load_obj(self, type):
        print(f"{type}の出現ポイントのシンボルをImportします")
        
        addon_directory = os.path.dirname(__file__)
        relative_path = SpawnNames.names[type][SpawnNames.FILENAME]
        full_path = os.path.join(addon_directory, relative_path)
        
        # オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',
            filepath=full_path, display_type='THUMBNAIL',
            forward_axis='Z', up_axis='Y')
            
        # 回転を適用
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False, properties=False, isolate_users=False)
        
        object = bpy.context.active_object
        object.name = SpawnNames.names[type][SpawnNames.PROTOTYPE]
        object["type"] = SpawnNames.names[type][SpawnNames.INSTANCE]
        
        # 元のプロトタイプは非表示扱いとしてシーンから外す
        bpy.context.collection.objects.unlink(object)


# プレイヤー専用のオペレータ（メニュー用）
class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT', type="Player")
        return {'FINISHED'}


# 敵専用のオペレータ（メニュー用）
class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT', type="Enemy")
        return {'FINISHED'}
