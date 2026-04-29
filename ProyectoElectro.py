"""
  COMO GUARDA INFORMACION UN DISCO DURO
  Materia: Electromagnetismo
  Integrantes: Kevin Andres Bayona Osma
               Juan Camilo Nunez Becerra
"""

import numpy as np
import matplotlib.pyplot as plt

mu_0 = 4 * np.pi * 1e-7   # constante del magnetismo en el vacío

print("=" * 52)
print("  ¿COMO GUARDA INFORMACION UN DISCO DURO?")
print("=" * 52)

print("""
La idea base es simple:
  Un disco duro guarda informacion usando MAGNETISMO.
  Cada pedacito del disco puede quedar magnetizado
  en dos direcciones distintas:

      ↑  hacia arriba  =  bit 1
      ↓  hacia abajo   =  bit 0

  Todo lo que guardas en un computador (fotos, videos,
  archivos) se convierte en millones de estos 1 y 0.
""")


# ESCRITURA: como se "graba" un bit?

print("─" * 52)
print("  ESCRITURA — Como se graba un bit?")
print("─" * 52)
print("""
  El disco tiene un "cabezal" que es basicamente
  un electroiman muy pequeno (una bobina con corriente).

  Cuando le metes corriente en una direccion →
  el iman apunta hacia arriba → graba un  1

  Cuando le metes corriente al reves →
  el iman apunta hacia abajo  → graba un  0

  La ecuacion que describe eso es la Ley de Ampere:

      B = μ₀ · (N/L) · I

  O sea: a mas corriente (I), mas campo magnetico (B),
  y ese campo es el que "deja marcado" el bit en el disco.
""")

N = 100       # numero de vueltas de la bobina
L = 0.005     # que tan larga es la bobina (5 mm)
n = N / L     # vueltas por metro

I_para_1 = +0.05   # corriente para grabar un "1"  (positiva)
I_para_0 = -0.05   # corriente para grabar un "0"  (negativa)

B_para_1 = mu_0 * n * I_para_1
B_para_0 = mu_0 * n * I_para_0

print(f"  Si mandamos I = +{I_para_1*1e3:.0f} mA  →  B = +{B_para_1*1e3:.2f} mT  →  graba '1' ↑")
print(f"  Si mandamos I = -{abs(I_para_0)*1e3:.0f} mA  →  B = {B_para_0*1e3:.2f} mT  →  graba '0' ↓")

corrientes = np.linspace(-0.1, 0.1, 400)
B_campo    = mu_0 * n * corrientes

# LECTURA: como se "lee" un bit?

print()
print("─" * 52)
print("  LECTURA — Como se detecta un bit?")
print("─" * 52)
print("""
  El disco gira muy rapido y el cabezal pasa por encima
  de cada bit grabado.

  Cuando hay un CAMBIO de bit (de 0 a 1, o de 1 a 0)
  el campo magnetico que siente el cabezal cambia,
  y ese cambio genera una pequena chispa de tension electrica.

  Eso lo describe la Ley de Faraday:

      ε = −N · dΦ/dt

  Es decir: si el flujo magnetico (Φ) cambia rápido,
  se genera una tension (ε) que el disco detecta como
  "aqui hay una transicion de bit".

  Si NO hay cambio → no hay tension → el bit sigue igual.

  Asi es exactamente como el disco "lee" tu informacion.
""")

bits     = [0, 0, 1, 0, 1, 1, 1, 0]
v_disco  = 20.0
lambda_b = 150e-9
t_bit    = lambda_b / v_disco

A_gap   = (50e-9)**2
B_disco = 0.3
Phi     = B_disco * A_gap

t_total = len(bits) * t_bit
t       = np.linspace(0, t_total, 2000)
fem     = np.zeros_like(t)
sigma   = t_bit * 0.08

for i in range(1, len(bits)):
    if bits[i] != bits[i-1]:
        tc    = i * t_bit
        signo = +1 if bits[i] == 1 else -1
        fem  += signo * 200e-6 * np.exp(-0.5 * ((t - tc) / sigma)**2)

print(f"  Velocidad del disco  : {v_disco} m/s")
print(f"  Duracion de un bit   : {t_bit*1e9:.2f} nanosegundos")
print(f"  Flujo por bit (Φ)    : {Phi:.2e} Wb")


# GRÁFICAS

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.patch.set_facecolor('#111827')

PANEL   = '#1f2937'
GRID    = '#374151'
TEXT    = '#f9fafb'
AZUL    = '#60a5fa'
VERDE   = '#34d399'
NARANJA = '#fb923c'
ROJO    = '#f87171'

for ax in axes:
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    ax.tick_params(colors=TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.grid(True, color=GRID, linestyle='--', linewidth=0.5)

# Gráfica 1: Mas corriente = mas campo
ax = axes[0]
ax.plot(corrientes * 1e3, B_campo * 1e3, color=AZUL, lw=2.5)
ax.axvline(0, color=GRID, lw=1)
ax.axhline(0, color=GRID, lw=1)
ax.scatter([I_para_1*1e3], [B_para_1*1e3], color=VERDE, s=120, zorder=5)
ax.scatter([I_para_0*1e3], [B_para_0*1e3], color=ROJO,  s=120, zorder=5)
ax.annotate("graba '1' ↑\ncorriente positiva",
            xy=(I_para_1*1e3, B_para_1*1e3), xytext=(20, 0.7),
            textcoords=('data','data'), color=VERDE, fontsize=8,
            arrowprops=dict(arrowstyle='->', color=VERDE))
ax.annotate("graba '0' ↓\ncorriente negativa",
            xy=(I_para_0*1e3, B_para_0*1e3), xytext=(-98, -0.7),
            textcoords=('data','data'), color=ROJO, fontsize=8,
            arrowprops=dict(arrowstyle='->', color=ROJO))
ax.set_xlabel("Corriente en la bobina [mA]")
ax.set_ylabel("Campo magnetico generado [mT]")
ax.set_title("Escritura de bits\nB = μ₀·(N/L)·I", color=TEXT, fontweight='bold')

# Grafica 2: Asi se ven los bits en el disco
ax = axes[1]
ax.set_title("Bits guardados en el disco\n↑ = 1   |   ↓ = 0", color=TEXT, fontweight='bold')
ax.set_xlim(-0.5, len(bits) - 0.5)
ax.set_ylim(-2, 2)
ax.set_xticks(range(len(bits)))
ax.set_xticklabels([str(b) for b in bits], color=TEXT, fontsize=14, fontweight='bold')
ax.set_yticks([])
ax.set_xlabel("Bits guardados uno al lado del otro en la pista")

for i, bit in enumerate(bits):
    color = VERDE if bit == 1 else ROJO
    flecha = '↑' if bit == 1 else '↓'
    rect = plt.Rectangle((i - 0.45, -1.3), 0.9, 2.6,
                          facecolor=color, alpha=0.2,
                          edgecolor=color, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(i, 0, flecha, ha='center', va='center',
            fontsize=22, color=color, fontweight='bold')

ax.annotate("", xy=(3.5, 1.75), xytext=(3.5, 1.3),
            arrowprops=dict(arrowstyle='-[,widthB=3', color=NARANJA, lw=2))
ax.text(3.5, 1.9, "cabezal", ha='center', color=NARANJA, fontsize=8)

# Grafica 3: Señal que "lee" los bits
ax = axes[2]
ax.plot(t * 1e9, fem * 1e6, color=VERDE, lw=2)
ax.axhline(0, color=GRID, lw=1)
ax.set_xlabel("Tiempo [nanosegundos]")
ax.set_ylabel("Tension detectada [μV]")
ax.set_title("Lectura de bits — Ley de Faraday\nε = −N · dΦ/dt", color=TEXT, fontweight='bold')

for i in range(1, len(bits)):
    if bits[i] != bits[i-1]:
        tc = i * t_bit * 1e9
        ax.axvline(tc, color=NARANJA, linestyle=':', lw=1.2, alpha=0.7)
        ax.text(tc, 210, f"{bits[i-1]}→{bits[i]}",
                color=NARANJA, fontsize=7.5, ha='center')

ax.text(0.73, 0.15,
        "Sin cambio de bit\n= sin tension\n= mismo bit",
        transform=ax.transAxes, color='#9ca3af', fontsize=8, ha='center',
        bbox=dict(facecolor=PANEL, edgecolor=GRID, boxstyle='round,pad=0.4'))

fig.suptitle(
    "¿Cómo guarda informacion un disco duro?\n"
    "Escritura con Ley de Ampere  ·  Lectura con Ley de Faraday",
    color=TEXT, fontsize=12, fontweight='bold', y=1.01
)

plt.tight_layout()
plt.savefig("hdd_electromagnetismo.png", dpi=150,
            bbox_inches='tight', facecolor='#111827')
plt.show()

print()
print("✅ Listo. La imagen se guardo como 'hdd_electromagnetismo.png'")