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

### DEC-013 — Indicadores netos y funciones reutilizables para el bloque 2

- **Fecha:** 2026-11-14
- **Autor:** marco.garcia@galileo.edu
- **Rama:** marco
- **Sección del enunciado:** 5, 6 y 7
- **Decisión:** Marco desarrolla el bloque 2; Mario el bloque 3. Se analizan unidades netas (item_cnt_day) e ingresos netos (item_price × item_cnt_day), conservando devoluciones y la limpieza DEC-009 a DEC-011. Las agregaciones por tienda, producto y mes se centralizan en predict_future_sales/features.py para reutilizarlas en las secciones 8 y 9. No se recortan extremos durante el EDA.
- **Justificación:** Mantiene trazabilidad con el procesamiento del bloque 1, permite comparar métricas y evita duplicación de código. Se incluye una normalización descriptiva por meses observados para comparar tiendas.
- **Alternativas descartadas:** Eliminar devoluciones, confundir ingresos con unidades, comparar tiendas únicamente por acumulados y eliminar outliers sin análisis.
- **Estado:** Vigente

### DEC-014 — Grupos de categoría en español para las visualizaciones del bloque 3
- **Fecha:** 2026-11-15
- **Autor:** 25005795@galileo.edu
- **Rama:** mario
- **Sección del enunciado:** 8, 9 y 10
- **Decisión:** Para gráficas y resúmenes, las 84 categorías se agrupan en 14 grupos con nombre en español
  (`GRUPOS_CATEGORIA_ES` y `agregar_grupo_categoria()` en `predict_future_sales/features.py`), tomando el prefijo
  del nombre ruso antes de " - " (p. ej. `Кино - DVD` → "Cine"). `item_categories.csv` no se modifica; las
  categorías individuales se siguen mostrando con su id y nombre original. La selección de series para ACF/PACF
  (sección 9) usa las de mayor volumen con historia suficiente: tiendas que venden los 34 meses, y productos y pares
  tienda-producto con ventas en al menos 30 meses (un par por producto).
- **Justificación:** 84 categorías en ruso no se leen en un heatmap; 14 grupos permiten ver la mezcla de ventas en
  el tiempo. Las series casi todas en ceros (productos de vida corta) no permiten interpretar la ACF/PACF.
- **Alternativas descartadas:** traducir las 84 categorías en un CSV de `references/` (acordado como pendiente en
  CLAUDE.md; esta agrupación no lo impide); seleccionar series solo por volumen total (los 3 pares serían la misma bolsa 20949).
- **Estado:** Vigente

### DEC-015 — Parte 2: cuadrícula mensual, partición temporal y lags seleccionados
- **Fecha:** 2026-11-23
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** Proyecto 2, punto 1.a (`02_feature_exploration.ipynb`)
- **Decisión:**
  - Se trabaja sobre una **cuadrícula mensual**: para cada mes 0-33, todas las tiendas × todos los productos con registros
    ese mes, con 0 donde no hubo ventas (DEC-008); los pares de `test.csv` se agregan como mes 34
    (`construir_cuadricula_mensual()`, 11,128,050 filas).
  - **Partición secuencial**: entrenamiento meses 0-26, validación 27-33, test 34 (`MES_FIN_ENTRENAMIENTO`). Todo parámetro
    aprendido de los datos se ajusta solo con los meses 0-26.
  - **Lags seleccionados** (`LAGS_SELECCIONADOS`, `agregar_lags()`): par tienda-producto 1, 2, 3 y 12; producto 1;
    tienda 1 y 12; categoría 1 y 12 (9 lags). Cada lag del mes *m* usa solo el mes *m − k* (sin fuga).
  - Variables adicionales sin fuga: `precio_previo` (último precio del producto en un mes anterior) y
    `meses_desde_primera_venta` (solo meses anteriores).
- **Justificación:** Correlación con `y` de 0.59 (lag 1) a 0.21 (lag 12). Regresión lineal, validación meses 27-33:
  predecir 0 = 1.116; lag 1 = 0.915; par 1-3 = 0.893; par 1-12 = 0.886; **selección = 0.880**; 24 candidatos = 0.876.
  En noviembre de 2014 la selección baja el RMSE de 1.127 (par 1-3) a 1.108 gracias a los lags 12 de tienda y categoría.
  Los lags de tienda y categoría están disponibles en ~97-100 % de los pares de test (los del par, en 47-78 %).
  **Limitación:** en cada mes solo entran productos con alguna venta ese mes, por lo que en el entrenamiento los productos
  nuevos siempre vendieron en su primer mes; en `test` no se sabe (363 productos nuevos). No es fuga, pero puede
  sobreestimar las ventas de productos nuevos: revisar en el notebook 04 el error con `item_sin_historia = 1`.
- **Alternativas descartadas:** cuadrícula completa de 22,170 productos × 57 tiendas × 34 meses (~43 millones de filas);
  usar los 12 lags del par (más columnas, menos mejora); usar el precio del propio mes (fuga: no existe para el mes 34).
- **Estado:** Vigente

### DEC-016 — Parte 2: operaciones de ingeniería de características y mapeos
- **Fecha:** 2026-11-23
- **Autor:** alfredo.mux@galileo.edu
- **Rama:** alfredo
- **Sección del enunciado:** Proyecto 2, puntos 1.b y 1.c (`02_feature_exploration.ipynb`)
- **Decisión:**
  - **i. Imputación numérica:** lags y `meses_desde_primera_venta` → 0 (sin registro = sin ventas), con bandera
    `item_sin_historia`; `precio_previo` → mediana del precio de su categoría en los meses 0-26 (respaldo: mediana global).
  - **ii. Imputación categórica (forzada, 5 % al azar, semilla 42):** constante `"Desconocido"` en `ciudad` y
    `grupo_categoria`.
  - **iii. Codificación:** one-hot de `grupo_categoria` (14, `oh_grupo_*`) y `tipo_tienda` (3, `oh_tipo_*`); frecuencia de
    `ciudad` (meses 0-26); `shop_id` e `item_category_id` como identificadores numéricos (variables exógenas).
    `item_id` **no entra** como variable: el producto se representa con sus lags, categoría, grupo, precio y antigüedad.
  - **iv. Outliers:** objetivo recortado a [0, 20] (12,378 meses-par, 0.113 %); `precio_previo` con tope en el p99.9 del
    entrenamiento (22,990). Completa lo que DEC-009 y DEC-013 dejaron para la etapa de modelado.
  - **v. Transformación:** `log1p` **solo** en `precio_previo`; los lags quedan en unidades.
  - **vi. Escalado:** `StandardScaler` ajustado con los meses 0-26 en las variables numéricas continuas.
  - **Mapeos:** tienda → ciudad (`MAPEO_CIUDAD_ES`), tienda → tipo (`TIENDAS_EN_LINEA` = {12, 55}, `TIENDAS_EVENTO` = {9, 20}),
    categoría → grupo (DEC-014), ciudad → frecuencia y categoría → mediana de precio (aprendidos en los meses 0-26).
  - **Cambio en el tiempo** (medias de validación desplazadas en la antigüedad y los lags 12): no se transforma; se
    recomienda **reentrenar el modelo ganador con los meses 0-33** antes de predecir el mes 34 (notebook 04).
  - Resultado: 32 variables de entrada; la lista completa y el orden de los pasos para el notebook 03 están en la sección 1.c.
- **Justificación:** Kaggle evalúa con las predicciones recortadas a [0, 20]. La mediana por categoría da un precio
  realista a los productos nuevos (7.12 % de los pares de test). `"Desconocido"` evita sesgar hacia la moda (Moscú, 22 % de
  las filas). `log1p` baja la asimetría del precio de 8.69 a 0.47. El escalado permite comparar modelos lineales y de
  árboles con el mismo preprocesamiento en el notebook 04. Comprobaciones con regresión lineal y árboles
  (`HistGradientBoostingRegressor`), entrenando con los meses 0-26 y validando con los meses 27-33 (RMSE):
  - `log1p` en los lags: lineal de 0.8730 a 0.9276 (peor); árboles sin cambio (0.8210).
  - `item_id` como variable: árboles de 0.8210 a 0.8346 (peor); `shop_id` e `item_category_id` mejoran (0.8279 → 0.8210).
  - Cambio en el tiempo: ventana 12-26 (0.8225), tope de 12 meses a la antigüedad (0.8254) o quitarla (0.8252) no mejoran;
    reentrenar hasta el mes 32 para predecir el 33 baja el RMSE de 0.9140 a 0.8895.
- **Alternativas descartadas:** imputar lags con la media (inventa ventas); moda en las categóricas; one-hot de `ciudad`
  (30 columnas dispersas) o de `item_id` (22,170); `item_id` como número; `log1p` en los lags; tope a la antigüedad;
  entrenar solo con los meses 12-26; eliminar solo el precio de 307,980 (no llega a la cuadrícula).
- **Estado:** Vigente
