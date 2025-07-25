# pylint: disable=too-many-arguments,too-many-positional-arguments,line-too-long
"""
平面を描画するスクリプト
"""
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D  # Not needed with modern matplotlib
from matplotlib.widgets import Slider


def compute_plane(x0, y0, z0, a, b, c):
    """
    平面のZ座標を計算する関数
    """
    d = -(a * x0 + b * y0 + c * z0)
    z = (-a * xx - b * yy - d) / c
    return z


def update(val):
    """
    スライダーの値が変更されたときに呼び出される関数
    """
    x0 = s_x0.val
    y0 = s_y0.val
    z0 = s_z0.val
    a = s_A.val
    b = s_B.val
    c = s_C.val if s_C.val != 0 else 0.01  # Cが0だと割り算エラーになるので対処

    # 平面削除
    for collection in ax.collections[:]:
        collection.remove()
    for artist in [artists['quiver'], artists['point']]:
        artist.remove()  # 矢印・点削除

    zz_update = compute_plane(x0, y0, z0, a, b, c)
    ax.plot_surface(xx, yy, zz_update, alpha=0.5, color='skyblue', edgecolor='gray')
    artists['quiver'] = ax.quiver(x0, y0, z0, a, b, c, length=2, color='red', linewidth=2)
    artists['point'] = ax.scatter(x0, y0, z0, color='black', s=50)
    fig.canvas.draw_idle()


# 初期値
init_x0, init_y0, init_z0 = 1, 2, 1
init_A, init_B, init_C = 2, -3, 1

# プロット作成
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.35)

# メッシュ作成
xx, yy = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))

# 最初のプロット
zz = compute_plane(init_x0, init_y0, init_z0, init_A, init_B, init_C)
plane = ax.plot_surface(xx, yy, zz, alpha=0.5, color='skyblue', edgecolor='gray')
artists = {
    'quiver': ax.quiver(init_x0, init_y0, init_z0, init_A, init_B, init_C, length=2, color='red', linewidth=2),
    'point': ax.scatter(init_x0, init_y0, init_z0, color='black', s=50)
}

# 軸設定
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_xlabel('X軸')
ax.set_ylabel('Y軸')
ax.set_zlabel('Z軸')
ax.set_title('平面と法線ベクトル（インタラクティブ）')

# スライダー位置定義
SLIDER_AX_COLOR = 'lightgoldenrodyellow'
ax_x0 = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)
ax_y0 = plt.axes([0.25, 0.21, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)
ax_z0 = plt.axes([0.25, 0.17, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)
ax_A = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)
ax_B = plt.axes([0.25, 0.09, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)
ax_C = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=SLIDER_AX_COLOR)

# スライダー作成
s_x0 = Slider(ax_x0, 'x0', -3.0, 3.0, valinit=init_x0)
s_y0 = Slider(ax_y0, 'y0', -3.0, 3.0, valinit=init_y0)
s_z0 = Slider(ax_z0, 'z0', -3.0, 3.0, valinit=init_z0)
s_A = Slider(ax_A, 'A', -5.0, 5.0, valinit=init_A)
s_B = Slider(ax_B, 'B', -5.0, 5.0, valinit=init_B)
s_C = Slider(ax_C, 'C', -5.0, 5.0, valinit=init_C)


# スライダーイベント接続
for s in [s_x0, s_y0, s_z0, s_A, s_B, s_C]:
    s.on_changed(update)

# 表示
plt.show()
