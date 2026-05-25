"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Parte 2 – Contando caminos en una cuadrícula
"""

import time

# ============================================================
# UTILIDAD DE MEDICIÓN (ya implementada — no modificar)
# ============================================================

def medir(funcion, *args, repeticiones: int = 5):
    """Ejecuta funcion(*args) 'repeticiones' veces. Retorna (resultado, t_promedio)."""
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return resultado, sum(tiempos) / len(tiempos)


# ============================================================
# PARTE 2A – CAMINOS SIN OBSTÁCULOS
# ============================================================

def caminos_recursivo(m: int, n: int) -> int:
    """Cuenta los caminos de (0,0) a (m-1, n-1) — versión recursiva."""
    # PASO 1 – Casos base
    if m == 1 or n == 1:
        return 1
    
    # PASO 2 – Caso recursivo
    return caminos_recursivo(m - 1, n) + caminos_recursivo(m, n - 1)


def caminos_memo(m: int, n: int, memo: dict = None) -> int:
    """Cuenta los caminos de (0,0) a (m-1, n-1) — versión memoización."""
    # 1. Inicializa memo si es None
    if memo is None:
        memo = {}
        
    # 2. Casos base
    if m == 1 or n == 1:
        return 1
        
    # 3. Revisa caché
    if (m, n) in memo:
        return memo[(m, n)]
        
    # 4. Calcula recursivamente, guarda en memo y devuelve
    memo[(m, n)] = caminos_memo(m - 1, n, memo) + caminos_memo(m, n - 1, memo)
    return memo[(m, n)]


def caminos_bottom_up(m: int, n: int) -> tuple:
    """Cuenta los caminos de (0,0) a (m-1, n-1) — versión tabulación."""
    # PASO 1 – Crea la tabla de m filas × n columnas llena de ceros.
    tabla = [[0] * n for _ in range(m)]

    # PASO 2 – Inicializa la primera fila.
    for j in range(n):
        tabla[0][j] = 1

    # PASO 3 – Inicializa la primera columna.
    for i in range(m):
        tabla[i][0] = 1

    # PASO 4 – Doble bucle de llenado.
    for i in range(1, m):
        for j in range(1, n):
            tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]

    # PASO 5 – Devuelve (total_caminos, tabla).
    return (tabla[m-1][n-1], tabla)


def imprimir_tabla(tabla: list, titulo: str = "Tabla DP") -> None:
    """Imprime la tabla DP con formato alineado."""
    # PASO 1 – Encuentra el valor máximo para calcular el ancho
    max_val = max(max(fila) for fila in tabla)
    ancho = len(str(max_val)) + 1
    
    # PASO 2 – Imprime el título
    print(f"{titulo}:")
    
    # PASO 3 – Recorre las filas e imprime alineado
    for fila in tabla:
        print(" ".join(str(val).rjust(ancho) for val in fila))


# ============================================================
# PARTE 2B – CAMINOS CON OBSTÁCULOS
# ============================================================

def caminos_con_obstaculos(grid: list) -> int:
    """Cuenta los caminos de (0,0) a (m-1, n-1) evitando obstáculos."""
    # PASO 1 – Verifica si el inicio o el destino están bloqueados.
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return 0

    # PASO 2 – Crea la tabla de ceros.
    tabla = [[0] * n for _ in range(m)]

    # PASO 3 – Inicializa la primera fila considerando obstáculos.
    for j in range(n):
        if grid[0][j] == 1:
            break  # Bloquea el resto de la fila
        tabla[0][j] = 1

    # PASO 4 – Inicializa la primera columna considerando obstáculos.
    for i in range(m):
        if grid[i][0] == 1:
            break  # Bloquea el resto de la columna
        tabla[i][0] = 1

    # PASO 5 – Llena el interior (doble bucle desde i=1, j=1).
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 0:
                tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]
            else:
                tabla[i][j] = 0

    # PASO 6 – Retorna el resultado.
    return tabla[m-1][n-1]


# ============================================================
# EXPERIMENTOS
# ============================================================

if __name__ == "__main__":

    # --- Verificación con casos conocidos ---
    print("=== Verificación de correctitud ===")
    casos = [(1, 1, 1), (2, 2, 2), (3, 3, 6), (3, 7, 28), (4, 4, 20)]
    for m, n, esperado in casos:
        r = caminos_recursivo(m, n)
        memo_r = caminos_memo(m, n)
        bu_result = caminos_bottom_up(m, n)
        bu = bu_result[0] if isinstance(bu_result, tuple) else bu_result
        ok = lambda v: "✓" if v == esperado else f"✗(esperado {esperado}, obtuvo {v})"
        print(f"  caminos({m}×{n}) = {esperado:4d}  recursivo:{ok(r)}  memo:{ok(memo_r)}  bottom_up:{ok(bu)}")

    # --- Visualización de la tabla ---
    print("\n=== Tabla DP para cuadrícula 5×5 ===")
    resultado_bu = caminos_bottom_up(5, 5)
    if isinstance(resultado_bu, tuple):
        total, tabla = resultado_bu
        imprimir_tabla(tabla, "Caminos 5×5")
        print(f"  Caminos totales: {total}")
    else:
        print("  (implementa caminos_bottom_up para ver la tabla)")

    # --- Experimento de tiempo ---
    print("\n=== Comparación de tiempos ===")
    print(f"{'cuadrícula':>12}  {'recursivo (s)':>16}  {'memo (s)':>12}  {'bottom_up (s)':>14}")
    # Nota: No probamos recursivo puro con valores muy altos porque tardaría demasiado.
    for dim in [5, 10, 12, 15]:
        _, t_r = medir(caminos_recursivo, dim, dim)
        _, t_m = medir(caminos_memo, dim, dim)
        bu_fn = lambda d=dim: caminos_bottom_up(d, d)
        _, t_b = medir(bu_fn)
        print(f"  {dim:3d}×{dim:<3d}     {t_r:16.8f}  {t_m:12.8f}  {t_b:14.8f}")

    # --- Prueba con obstáculos ---
    print("\n=== Cuadrícula con obstáculos ===")
    grid_ejemplo = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    print("  Grid:")
    for fila in grid_ejemplo:
        print("    ", fila)
    resultado_obs = caminos_con_obstaculos(grid_ejemplo)
    print(f"  Caminos evitando obstáculos: {resultado_obs}  (esperado: 4)")
