import time

# ============================================================
# UTILIDAD DE MEDICIÓN (ya implementada — no modificar)
# ============================================================

def medir(funcion, *args, repeticiones: int = 5):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return resultado, sum(tiempos) / len(tiempos)

# ============================================================
# PARTE 1A – TRES VERSIONES DE FIBONACCI
# ============================================================

def fib_recursivo(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
    
    if n == 0:
        return 0
    if n == 1:
        return 1
        
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)

def fib_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
        
    if n < 0:
        raise ValueError("n debe ser >= 0")
        
    if n == 0:
        return 0
    if n == 1:
        return 1
        
    if n in memo:
        return memo[n]
        
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_bottom_up(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
        
    if n == 0:
        return 0
    if n == 1:
        return 1
        
    tabla = [0] * (n + 1)
    tabla[0] = 0
    tabla[1] = 1
    
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]
        
    return tabla[n]

# ============================================================
# PARTE 1B – ESCALANDO PELDAÑOS
# ============================================================

def escaleras_recursivo(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
        
    if n == 0:
        return 1
    if n == 1:
        return 1
        
    return escaleras_recursivo(n - 1) + escaleras_recursivo(n - 2)

def escaleras_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
        
    if n < 0:
        raise ValueError("n debe ser >= 0")
        
    if n == 0:
        return 1
    if n == 1:
        return 1
        
    if n in memo:
        return memo[n]
        
    memo[n] = escaleras_memo(n - 1, memo) + escaleras_memo(n - 2, memo)
    return memo[n]

def escaleras_bottom_up(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
        
    if n == 0:
        return 1
    if n == 1:
        return 1
        
    tabla = [0] * (n + 1)
    tabla[0] = 1
    tabla[1] = 1
    
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]
        
    return tabla[n]

# ============================================================
# EXPERIMENTOS — ejecuta este bloque para ver resultados
# ============================================================

if __name__ == "__main__":

    esperados_fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    print("=== Verificación Fibonacci ===")
    for i, esperado in enumerate(esperados_fib):
        r = fib_recursivo(i)
        m = fib_memo(i)
        b = fib_bottom_up(i)
        ok_r = "✓" if r == esperado else f"✗(esperado {esperado}, obtuvo {r})"
        ok_m = "✓" if m == esperado else f"✗(esperado {esperado}, obtuvo {m})"
        ok_b = "✓" if b == esperado else f"✗(esperado {esperado}, obtuvo {b})"
        print(f"  F({i:2d}) = {esperado:4d}  recursivo:{ok_r}  memo:{ok_m}  bottom_up:{ok_b}")

    esperados_esc = [1, 1, 2, 3, 5, 8, 13, 21]
    print("\n=== Verificación Escaleras ===")
    for i, esperado in enumerate(esperados_esc):
        r = escaleras_recursivo(i)
        m = escaleras_memo(i)
        b = escaleras_bottom_up(i)
        ok_r = "✓" if r == esperado else f"✗(esperado {esperado}, obtuvo {r})"
        ok_m = "✓" if m == esperado else f"✗(esperado {esperado}, obtuvo {m})"
        ok_b = "✓" if b == esperado else f"✗(esperado {esperado}, obtuvo {b})"
        print(f"  esc({i}) = {esperado:4d}  recursivo:{ok_r}  memo:{ok_m}  bottom_up:{ok_b}")

    print("\n=== Comparación de tiempos: Fibonacci ===")
    print(f"{'n':>5}  {'recursivo (s)':>16}  {'memo (s)':>12}  {'bottom_up (s)':>14}")
    for n in [10, 20, 30, 35]:
        _, t_r = medir(fib_recursivo, n)
        _, t_m = medir(fib_memo, n)
        _, t_b = medir(fib_bottom_up, n)
        print(f"  {n:3d}  {t_r:16.8f}  {t_m:12.8f}  {t_b:14.8f}")

    print("\n=== Escaleras vs Fibonacci ===")
    for n in range(1, 10):
        fib_n1 = fib_bottom_up(n + 1)
        esc_n  = escaleras_bottom_up(n)
        print(f"  escaleras({n}) = {esc_n:4d}   fib({n+1}) = {fib_n1:4d}  "
              f"{'¿iguales?' if esc_n == fib_n1 else 'DISTINTOS'}")
