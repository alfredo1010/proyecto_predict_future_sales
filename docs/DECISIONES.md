# Bitácora de decisiones

Registro de las decisiones del proyecto: **qué** se decidió, **quién**, **en qué rama** y **por qué**.

## Reglas de uso

- **Solo agregar (append-only):** cada decisión nueva va **al final** del archivo. No se editan ni borran entradas anteriores.
- Si una decisión cambia, se agrega una entrada nueva con estado `Reemplaza a DEC-XXX`.
- Numeración consecutiva (`DEC-001`, `DEC-002`, …). Si dos ramas usan el mismo número al hacer merge, se renumera la última en integrarse.
- Registrar la decisión en el mismo commit en que se implementa.

## Plantilla

```markdown
### DEC-XXX — Título corto
- **Fecha:** AAAA-MM-DD
- **Autor:** correo@galileo.edu
- **Rama:** alfredo | mario | marco
- **Sección del enunciado:** N
- **Decisión:** qué se hará.
- **Justificación:** por qué (con datos/evidencia si aplica).
- **Alternativas descartadas:** qué otras opciones se consideraron y por qué no.
- **Estado:** Vigente | Reemplaza a DEC-XXX
```

---

## Decisiones

### DEC-001 — Estructura del proyecto con cookiecutter-data-science v2
- **Fecha:** 2026-11-05
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** main
- **Sección del enunciado:** 1
- **Decisión:** Usar la plantilla `cookiecutter-data-science` v2.3.0 (comando `ccds`) con: gestor `conda`,
  dependencias en `requirements.txt`, paquetes PyData básicos, `ruff` como linter, sin licencia, sin `mkdocs`,
  e incluyendo el paquete de código `predict_future_sales/`.
- **Justificación:** Lo pide el enunciado (1.a). Sin `mkdocs` para que `docs/` solo contenga la documentación
  del equipo. Sin licencia por ser un repositorio académico privado.
- **Alternativas descartadas:** opción `mkdocs` (agrega archivos de sitio web que no se usarán).
- **Estado:** Vigente

### DEC-002 — Entorno: Python 3.12, soporte conda y venv/pip
- **Fecha:** 2026-11-05
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** main
- **Sección del enunciado:** 1
- **Decisión:** Python 3.12. Entorno conda `predict_future_sales` vía `environment.yml`, que instala desde
  `requirements.txt` (fuente única de dependencias). Quien no use conda puede usar `venv` + `pip install -r requirements.txt`.
  Se agregan a las dependencias base: `seaborn`, `statsmodels` (ACF/PACF) e `ipykernel`.
- **Justificación:** 3.12 es estable y compatible con todas las librerías del proyecto. No todos los integrantes
  usan conda; con un solo archivo de dependencias ambos caminos quedan sincronizados.
- **Alternativas descartadas:** mantener `environment.yml` y `requirements.txt` con listas separadas (riesgo de desincronización).
- **Estado:** Vigente

### DEC-003 — Datos fuera del repositorio, estructura de carpetas sí versionada
- **Fecha:** 2026-11-05
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** main
- **Sección del enunciado:** 1.d
- **Decisión:** `.gitignore` excluye el contenido de `data/`, así como `*.csv` y `*.zip`, pero conserva las carpetas
  `data/raw`, `data/interim`, `data/processed` y `data/external` mediante `.gitkeep`.
- **Justificación:** Los datos de Kaggle pesan ~100 MB y no deben versionarse (1.d). Conservar las carpetas permite
  que quien clone el repo tenga `data/raw/` lista para colocar los archivos. (La plantilla original ignoraba `data/`
  completa, incluidas las carpetas.)
- **Alternativas descartadas:** ignorar `data/` completa (la plantilla original).
- **Estado:** Vigente

### DEC-004 — Flujo de trabajo: ramas por bloque y un notebook compartido
- **Fecha:** 2026-11-05
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** main
- **Sección del enunciado:** General
- **Decisión:** Tres ramas de trabajo (`feature/calidad-datos`, `feature/descriptivo-visualizaciones`,
  `feature/temporal-acf`) que se integran a `main` vía Pull Request. Un solo notebook
  `notebooks/01_exploratory_data_analysis.ipynb`; se avisa al equipo antes y después de modificarlo.
  Cada integrante hace sus commits desde su computadora con su propia identidad de git.
- **Justificación:** Separar el trabajo por bloque del enunciado; el historial de commits evidencia la participación
  de cada integrante.
- **Alternativas descartadas:** notebooks borrador por integrante (se acordó evaluarlo internamente).
- **Estado:** Vigente

### DEC-005 — Ramas por integrante en lugar de ramas por bloque
- **Fecha:** 2026-11-05
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** General
- **Decisión:** Las ramas de trabajo pasan a ser una por integrante: `alfredo`, `mario` y `marco`
  (renombradas desde `feature/calidad-datos`, `feature/descriptivo-visualizaciones` y `feature/temporal-acf`).
  Cada integrante trabaja en su rama el bloque que se le asigne y se integra a `main` vía Pull Request.
  El resto de DEC-004 (un solo notebook compartido, avisar antes/después de modificarlo, commits propios) sigue vigente.
- **Justificación:** La asignación de bloques a personas aún no está definida; una rama por integrante
  facilita que cada uno trabaje y evidencie su participación sin depender de esa asignación.
- **Alternativas descartadas:** ramas por bloque (DEC-004).
- **Estado:** Reemplaza parcialmente a DEC-004 (nombres de ramas)

### DEC-006 — Conversión de tipos en sales_train: `date` a datetime e `item_cnt_day` a entero
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 3.a y 3.b
- **Decisión:** `date` se convierte a `datetime64` con el formato explícito `%d.%m.%Y` (función `convertir_fecha()`);
  `item_cnt_day` se convierte a `int64` (función `convertir_cantidad_entera()`). Ambas funciones están en
  `predict_future_sales/dataset.py`, fallan con error si encuentran fechas inválidas o cantidades con decimales,
  y devuelven una copia (no modifican el DataFrame original).
- **Justificación:** `date` viene como texto `dd.mm.aaaa`; sin formato explícito pandas podría confundir día y mes.
  `item_cnt_day` se lee como `float64`, pero no tiene nulos ni decimales (rango -22 a 2,169) y representa unidades.
  Tenerlas como funciones garantiza que los tres integrantes conviertan los datos igual.
- **Alternativas descartadas:** dejar que pandas infiera el formato de fecha (riesgo de invertir día/mes);
  mantener `item_cnt_day` como `float64`.
- **Estado:** Vigente

### DEC-007 — Frecuencia de agregación: mensual (`date_block_num`)
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 3.c
- **Decisión:** El análisis por tienda, producto y tienda-producto se agrega a nivel **mensual** usando `date_block_num`.
  La frecuencia **diaria** se usa solo para la serie de ventas totales (ACF/PACF diaria, sección 9) y para ciclos por
  día de la semana (sección 6).
- **Justificación:** La variable objetivo es mensual. `date_block_num` coincide con la fecha en el 100 % de las filas
  (0 inconsistencias). Sobre los 424,124 pares tienda-producto con historial, solo el 0.67 % de las combinaciones
  tienda-producto-día tiene ventas (3.69 % semanal, 11.16 % mensual): a nivel diario la serie es casi toda ceros.
  Las semanas cruzan entre meses y no se alinean con el objetivo.
- **Alternativas descartadas:** diaria (demasiado dispersa); semanal (dispersa y desalineada con el objetivo mensual).
- **Estado:** Vigente

### DEC-008 — Valores nulos: no requieren tratamiento
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 4.a
- **Decisión:** No se imputa ni elimina nada por nulos. Al agregar a nivel mensual, las combinaciones
  tienda-producto-mes sin registros se interpretan como **ventas = 0**, no como datos faltantes.
- **Justificación:** Ninguna columna de ninguna de las 5 tablas tiene nulos (0 %) ni textos vacíos.
- **Alternativas descartadas:** —
- **Estado:** Vigente

### DEC-009 — Precio inválido y devoluciones
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 4.b
- **Decisión:**
  - Precios ≤ 0 (1 fila: precio -1, tienda 32, producto 2973, 15-05-2013) se reemplazan por la **mediana del precio
    del mismo producto en la misma tienda y mes** (respaldo: mediana del producto en el mes). Resultado: 1,874.
  - Las cantidades negativas (devoluciones, 7,356 filas = 0.25 %) **se conservan**.
  - Los meses tienda-producto con total neto negativo (915) se dejan así en el EDA; recortarlos a 0 se decide en modelado.
  - Implementado en `limpiar_sales_train()` (`predict_future_sales/dataset.py`).
- **Justificación:** La venta con precio -1 sí ocurrió (cantidad 1); reemplazar el precio evita perderla.
  Las devoluciones son transacciones reales (98.6 % son -1, en 54 tiendas) y restan de las ventas netas;
  eliminarlas inflaría las ventas.
- **Alternativas descartadas:** eliminar la fila del precio -1 (impacto equivalente, pero pierde la venta);
  eliminar devoluciones o convertirlas a positivas.
- **Estado:** Vigente

### DEC-010 — Duplicados en sales_train
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 4.c
- **Decisión:** Se eliminan las **6 filas duplicadas exactas** (todas las columnas iguales). Se **conservan** los 22 grupos
  con el mismo producto, tienda y día pero distinto precio. Implementado en `limpiar_sales_train()`.
- **Justificación:** Cada fila ya es el total diario de un producto en una tienda a un precio, por lo que una fila idéntica
  duplicaría ventas. Las filas con precio distinto son ventas legítimas a precios distintos (descuentos o cambios en el día).
- **Alternativas descartadas:** conservar los duplicados exactos; eliminar también los registros con distinto precio.
- **Estado:** Vigente

### DEC-011 — Unificación de tiendas duplicadas: 0→57, 1→58, 11→10
- **Fecha:** 2026-11-09
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** 4.c
- **Decisión:** En `sales_train` se reemplaza `shop_id` 0 por 57, 1 por 58 y 11 por 10 (se conserva el id presente en
  `test.csv`). Queda en `MAPEO_TIENDAS_DUPLICADAS` y se aplica en `limpiar_sales_train()`. Las tiendas 23/24 y 39/40
  **no** se unifican. `shops.csv` no se modifica (sigue teniendo 60 filas); el análisis trabaja con 57 tiendas.
- **Justificación:** Nombres casi idénticos (0/57 y 1/58: mismo nombre con `!` y sufijo "фран"; 10/11: `39м?` vs `39м²`)
  y periodos de venta complementarios sin ningún mes en común (0 y 1 venden en los meses 0-1; 57 y 58 desde el mes 2;
  a la 10 le falta justo el mes 25, único mes de la 11). 23/24 (pabellones distintos) y 39/40 venden en los mismos meses.
- **Alternativas descartadas:** no unificar (fragmentaría la historia de 3 tiendas que están en test);
  unificar también 23/24 y 39/40.
- **Estado:** Vigente

### DEC-012 — División del trabajo en orden de secciones: bloque 2 = 5, 6, 7 y bloque 3 = 8, 9, 10
- **Fecha:** 2026-11-11
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** General
- **Decisión:** Los bloques siguen el orden del enunciado: bloque 1 = secciones 2, 3 y 4 (terminado);
  bloque 2 = 5, 6 y 7 (descriptivo, temporal y comparación); bloque 3 = 8, 9 y 10 (visualizaciones, ACF/PACF y
  conclusiones). La sección 10 la redacta el responsable del bloque 3 y los otros dos la revisan y aportan antes
  de integrarla a `main`. Las agregaciones de las secciones 5-7 se dejan como funciones en
  `predict_future_sales/features.py` para que el bloque 3 las reutilice. Los bloques 2 y 3 aún no están asignados.
- **Justificación:** Trabajar en orden facilita seguir el notebook y que cada bloque parta del anterior.
- **Alternativas descartadas:** división temática anterior (bloque 2 = 5, 7, 8; bloque 3 = 6, 9; sección 10 los tres).
- **Estado:** Reemplaza la división de bloques descrita en CLAUDE.md sección 3 (sin número de decisión previo)
