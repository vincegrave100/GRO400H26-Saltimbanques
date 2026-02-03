import math
import numpy as np
from donnees import Donnees

# -----------------------------
# Rotations (même style que toi)
# -----------------------------
def Rz(theta):
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ])

def Ry(theta):
    return np.array([
        [ math.cos(theta), 0,  math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0,  math.cos(theta)]
    ])

# -----------------------------
# Base et cible
# -----------------------------
p_w0 = np.array([[Donnees.wx],
                 [Donnees.wy],
                 [Donnees.wz]])

p_ee_cible = np.array([[Donnees.x_cible],
                       [Donnees.y_cible],
                       [Donnees.z_cible]])

L1, L2, L3 = Donnees.L1, Donnees.L2, Donnees.L3

# Sens de l'outil (perpendiculaire au sol)
sens = Donnees.sens_outil  # -1 vers le sol, +1 vers le haut

# ---------------------------------------------------------
# IK : on vise le POIGNET (p_e2) puis on impose j4
# Si l'outil est vertical, le vecteur poignet->bout vaut:
#   [0, 0, sens*L3] en world
# donc: p_e2 = p_ee - [0,0,sens*L3]
# ---------------------------------------------------------
p_e2_cible = p_ee_cible - np.array([[0], [0], [sens * L3]])

# vecteur base -> poignet
d = p_e2_cible - p_w0
dx, dy, dz = d[0, 0], d[1, 0], d[2, 0]

# 1) yaw
j1 = math.atan2(dy, dx)

# distance radiale dans XY
r = math.sqrt(dx*dx + dy*dy)

# Plan 2D après yaw : (r, z_plan)
# Avec notre Ry, z devient négatif quand l'angle pitch est positif,
# donc on prend z_plan = -dz pour utiliser les formules standard.
z_plan = -dz

D = math.sqrt(r*r + z_plan*z_plan)

# atteignabilité
if D > (L1 + L2) + 1e-9 or D < abs(L1 - L2) - 1e-9:
    raise ValueError(
        f"Cible hors atteinte: D={D:.3f} m, portée [{abs(L1-L2):.3f}, {(L1+L2):.3f}] m"
    )

# loi des cosinus pour j3
c3 = (D*D - L1*L1 - L2*L2) / (2*L1*L2)
c3 = max(-1.0, min(1.0, c3))

# coude haut/bas
if Donnees.config_coude.lower() == "haut":
    j3 = -math.acos(c3)   # elbow-up
else:
    j3 = math.acos(c3)    # elbow-down

phi = math.atan2(z_plan, r)
beta = math.atan2(L2 * math.sin(j3), L1 + L2 * math.cos(j3))

# pitch base
j2 = phi - beta

# 3) pitch poignet pour outil vertical:
# j2 + j3 + j4 = sens*pi/2
j4 = sens * (math.pi / 2) - (j2 + j3)

# ---------------------------------------------------------
# FK : positions des joints / points (base, coude, poignet, bout)
# ---------------------------------------------------------
r_aw = Rz(j1)
r_ba = Ry(j2)
r_cb = Ry(j3)
r_ec = Ry(j4)

r_bw = r_aw @ r_ba
r_cw = r_bw @ r_cb
r_ew = r_cw @ r_ec  # orientation outil finale

# vecteurs (en x local)
v_0e1_b = np.array([[L1], [0], [0]])   # base->coude exprimé dans B
v_e1e2_c = np.array([[L2], [0], [0]])  # coude->poignet exprimé dans C
v_e2ee_e = np.array([[L3], [0], [0]])  # poignet->bout exprimé dans E (outil)

p_e1_w = p_w0 + (r_bw @ v_0e1_b)
p_e2_w = p_e1_w + (r_cw @ v_e1e2_c)
p_ee_w = p_e2_w + (r_ew @ v_e2ee_e)

# Axe outil (x local) dans le world: doit être ~[0,0,±1]
x_tool_w = r_ew @ np.array([[1], [0], [0]])

# expose variables
angles = (j1, j2, j3, j4)

# debug utile
if __name__ == "__main__":
    print("BASE p_w0 =", p_w0.ravel())
    print("CIBLE bout p_ee_cible =", p_ee_cible.ravel())
    print("CALC bout p_ee_w =", p_ee_w.ravel())
    print("Axe outil x_tool_w =", x_tool_w.ravel())
    print("Angles (j1,j2,j3,j4) =", angles)
