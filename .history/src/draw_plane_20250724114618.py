import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# 初期値
init_x0, init_y0, init_z0 = 1, 2, 1
init_A, init_B, init_C = 2, -3, 1

# プロット作成
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.35)

# メッシュ作成
xx, yy = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))


# 平面のZを計算する関数
def compute_plane(x0, y0, z0, A, B, C):
    D = -(A * x0 + B * y0 + C * z0)
    zz = (-A * xx - B * yy - D) / C
    return zz

# 最初のプロット
zz = compute_plane(init_x0, init_y0, init_z0, init_A, init_B, init_C)
plane = ax.plot_surface(xx, yy, zz, alpha=0.5, color='skyblue', edgecolor='gray')
quiver = ax.quiver(init_x0, init_y0, init_z0, init_A, init_B, init_C, length=2, color='red', linewidth=2)
point = ax.scatter(init_x0, init_y0, init_z0, color='black', s=50)

# 軸設定
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_xlabel('X軸')
ax.set_ylabel('Y軸')
ax.set_zlabel('Z軸')
ax.set_title('平面と法線ベクトル（インタラクティブ）')

# スライダー位置定義
slider_ax_color = 'lightgoldenrodyellow'
ax_x0 = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=slider_ax_color)
ax_y0 = plt.axes([0.25, 0.21, 0.65, 0.03], facecolor=slider_ax_color)
ax_z0 = plt.axes([0.25, 0.17, 0.65, 0.03], facecolor=slider_ax_color)
ax_A  = plt.axes([0.25, 0.13, 0.65, 0.03], facecolor=slider_ax_color)
ax_B  = plt.axes([0.25, 0.09, 0.65, 0.03], facecolor=slider_ax_color)
ax_C  = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=slider_ax_color)

# スライダー作成
s_x0 = Slider(ax_x0, 'x₀', -3.0, 3.0, valinit=init_x0)
s_y0 = Slider(ax_y0, 'y₀', -3.0, 3.0, valinit=init_y0)
s_z0 = Slider(ax_z0, 'z₀', -3.0, 3.0, valinit=init_z0)
s_A  = Slider(ax_A,  'A',  -5.0, 5.0, valinit=init_A)
s_B  = Slider(ax_B,  'B',  -5.0, 5.0, valinit=init_B)
s_C  = Slider(ax_C,  'C',  -5.0, 5.0, valinit=init_C)

# 更新関数
def update(val):
    x0 = s_x0.val
    y0 = s_y0.val
    z0 = s_z0.val
    A = s_A.val
    B = s_B.val
    C = s_C.val if s_C.val != 0 else 0.01  # Cが0だと割り算エラーになるので対処

    ax.collections.clear()  # 平面削除
    for artist in [quiver, point]:
        artist.remove()  # 矢印・点削除

    zz = compute_plane(x0, y0, z0, A, B, C)
    ax.plot_surface(xx, yy, zz, alpha=0.5, color='skyblue', edgecolor='gray')
    global quiver, point
    quiver = ax.quiver(x0, y0, z0, A, B, C, length=2, color='red', linewidth=2)
    point = ax.scatter(x0, y0, z0, color='black', s=50)
    fig.canvas.draw_idle()

# スライダーイベント接続
for s in [s_x0, s_y0, s_z0, s_A, s_B, s_C]:
    s.on_changed(update)

# 表示
plt.show()
