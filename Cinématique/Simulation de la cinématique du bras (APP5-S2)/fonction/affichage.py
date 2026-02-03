# affichage.py
import matplotlib.pyplot as plt
import bras_robot

# ordre correct: base -> coude -> poignet -> bout
x = [bras_robot.p_w0[0,0], bras_robot.p_e1_w[0,0], bras_robot.p_e2_w[0,0], bras_robot.p_ee_w[0,0]]
y = [bras_robot.p_w0[1,0], bras_robot.p_e1_w[1,0], bras_robot.p_e2_w[1,0], bras_robot.p_ee_w[1,0]]
z = [bras_robot.p_w0[2,0], bras_robot.p_e1_w[2,0], bras_robot.p_e2_w[2,0], bras_robot.p_ee_w[2,0]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, linewidth=2)
ax.scatter(x, y, z)

# marqueurs base/bout
ax.scatter([bras_robot.p_w0[0,0]], [bras_robot.p_w0[1,0]], [bras_robot.p_w0[2,0]], s=80, marker='o', label="Base")
ax.scatter([bras_robot.p_ee_w[0,0]], [bras_robot.p_ee_w[1,0]], [bras_robot.p_ee_w[2,0]], s=80, marker='^', label="Bout")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_box_aspect([1,1,1])
plt.legend()
plt.show()

print("Angles (j1,j2,j3,j4) =", bras_robot.angles)
print("Bout effecteur calculé =\n", bras_robot.p_ee_w)
