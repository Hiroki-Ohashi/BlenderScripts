import bpy
import mathutils
import gpu
import gpu_extras.batch
import copy

#コライダー描画
class DrawCollider:
    #描画ハンドル
    handle = None
    #3Dビューに登録する描画関数
    def draw_collider():
        #頂点データ
        vertices = {"pos":[]}
        #インデックスデータ
        indices = []
        #各頂点のオブジェクト中心からのオフセット
        offsets = [
            [-0.5, -0.5, -0.5],
            [+0.5, -0.5, -0.5],
            [-0.5, +0.5, -0.5],
            [+0.5, +0.5, -0.5],
            [-0.5, -0.5, +0.5],
            [+0.5, -0.5, +0.5],
            [-0.5, +0.5, +0.5],
            [+0.5, +0.5, +0.5],
        ]
        #立方体のX,Y,Z方向サイズ
        size = [2,2,2]
        #現在のシーンのオブジェクトリストを走査
        for object in bpy.context.scene.objects:
            #コライダープロパティがなければ、描画をスキップ
            if not "collider" in object:
                continue

            #中心点、サイズの変数を宣言
            center = mathutils.Vector((0,0,0))
            size = mathutils.Vector((2,2,2))

            #プロパティから値を取得
            center[0]=object["collider_center"][0]
            center[1]=object["collider_center"][1]
            center[2]=object["collider_center"][2]
            size[0]=object["collider_size"][0]
            size[1]=object["collider_size"][1]
            size[2]=object["collider_size"][2]

            #追加前の頂点数
            start = len(vertices["pos"])

            #BOXの8頂点分回す
            for offset in offsets:
                #オブジェクトの中心座標をコピー
                pos = copy.copy(center)
                #中心点を基準に各頂点ごとにずらす
                pos[0]+=offset[0]*size[0]
                pos[1]+=offset[1]*size[1]
                pos[2]+=offset[2]*size[2]
                #ローカル座標からワールド座標に変換
                pos = object.matrix_world @ pos
                #頂点データリストに座標を追加
                vertices['pos'].append(pos)
                #前面を構成する辺の頂点インデックス
                indices.append([start+0,start+1])
                indices.append([start+2,start+3])
                indices.append([start+0,start+2])
                indices.append([start+1,start+3])
                 #奥面を構成する辺の頂点インデックス
                indices.append([start+4,start+5])
                indices.append([start+6,start+7])
                indices.append([start+4,start+6])
                indices.append([start+5,start+7])
                 #前と頂点を繋ぐ辺の頂点インデックス
                indices.append([start+0,start+4])
                indices.append([start+1,start+5])
                indices.append([start+2,start+6])
                indices.append([start+3,start+7])

        #ビルトインのシェーダーを取得
        shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        #パッチを作成(引数：シェーダー、トロポジー、頂点データ、インデックスデータ)
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices = indices)
        #シェーダーのパラメータ設定
        color = [0.5, 1.0, 1.0, 1.0]
        shader.bind()
        shader.uniform_float("color", color)
        #描画
        batch.draw(shader)

#オペレータ カスタムプロパティ['collider']追加
class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_collider"
    bl_label = "コライダー 追加"
    bl_description = "['collider']カスタムプロパティを追加します"
    bl_option = {"REGISTER", "UNDO"}

    def execute(self, context):
        #['collider']カスタムプロパティを追加
        context.object["collider"] = "BOX"
        context.object["collider_center"] = mathutils.Vector((0,0,0))
        context.object["collider_size"] = mathutils.Vector((2,2,2))

        return {"FINISHED"}

#パネル コライダー
class OBJECT_PT_collider(bpy.types.Panel):
    bl_idname = "OBJECT_PT_collider"
    bl_label = "Collider"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニューの追加
    def draw(self, context):
        #パネルに項目を追加
        if "collider" in context.object:
            #既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object, '["collider"]', text="Type")
            self.layout.prop(context.object, '["collider_center"]', text="Center")
            self.layout.prop(context.object, '["collider_size"]', text="Size")
        else:
            #プロパティがなければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_collider.bl_idname)