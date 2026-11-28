# CLAUDE.md — Contexto del proyecto para Claude Code

Este archivo lo lee Claude Code automáticamente al abrir el proyecto. Contiene el **enunciado completo**
de las dos fases del proyecto (fuente oficial, transcrita de los PDF del curso) y las **reglas de trabajo del equipo**:
- **Proyecto #1 — EDA:** secciones 2 a 4 de este archivo (terminado).
- **Proyecto #2 — Pipeline de ML:** secciones 5 y 6 de este archivo (en curso).
Todo el equipo trabaja con Claude Code dentro de VSCode, cada integrante en su propia rama.

Archivos de contexto del proyecto:

| Archivo | Para quién | Contenido |
|---|---|---|
| `CLAUDE.md` | La IA (y el equipo) | Enunciado completo + reglas de trabajo |
| `README.md` | Personas | Descripción, integrantes, instalación del entorno, datos, entregables |
| `docs/DECISIONES.md` | Ambos | Bitácora de decisiones (qué se decidió, quién, por qué) |

**Antes de proponer un tratamiento de datos o un cambio de enfoque, revisa `docs/DECISIONES.md`**
y no contradigas una decisión registrada sin señalarlo explícitamente.

---

## 1. Reglas de trabajo del equipo

### Idioma
- Todo el contenido (markdown del notebook, interpretaciones, comentarios, commits, documentación) en **español**.
- Nombres de variables y funciones en código pueden ir en inglés o español, pero de forma consistente.

### Git y ramas
- **Nunca trabajar directamente en `main`.** `main` solo recibe cambios vía Pull Request.
- Ramas de trabajo (una por integrante; ver DEC-005):
  - `alfredo` → Alfredo
  - `mario` → Mario
  - `marco` → Marco
- Cada integrante trabaja **solo en su rama** el bloque que se le asigne (ver sección 3).
  La sección 10 (conclusiones) la redacta el responsable del bloque 3, y los otros dos la revisan y aportan antes de integrarla (DEC-012).
- **Antes de cada commit y push, validar la rama actual** (`git branch --show-current`).
- **Cada integrante hace sus propios commits desde su propia computadora**, con su nombre y correo
  configurados en git (`git config --global user.name` / `user.email`). El historial de commits
  es la **evidencia de que los tres trabajaron**; no hacer commits en nombre de otro integrante.
- Hacer `git pull` de `main` (y merge a la rama propia) antes de empezar a trabajar cada día.
- Commits pequeños y descriptivos en español, p. ej. `Sección 4: análisis de duplicados en sales_train`.

### Notebook compartido
- Proyecto #1: el entregable es **un solo notebook**: `notebooks/01_exploratory_data_analysis.ipynb`, con secciones
  ya creadas para los 10 puntos del enunciado.
- Proyecto #2: un notebook por punto (`02_feature_exploration`, `03_feature_creation`, `04_model_training_n_tunning`,
  `05_inference_calculation`); ver sección 5.
- Los `.ipynb` generan conflictos de merge difíciles. Regla del equipo: **avisar al grupo antes y después
  de modificar el notebook**, editar solo las celdas de la sección propia y no reordenar/borrar celdas ajenas.
- Funciones reutilizables (carga de datos, limpieza, gráficas comunes) van al paquete `predict_future_sales/`
  (`dataset.py`, `features.py`, `plots.py`) y se importan desde el notebook, para reducir conflictos.

### Archivos de contexto (CLAUDE.md, README.md, docs/DECISIONES.md)
- `docs/DECISIONES.md` es **solo-agregar (append-only)**: cada decisión es una entrada nueva al final.
  No se editan ni borran entradas anteriores; si una decisión cambia, se agrega una entrada nueva que la reemplaza
  y se referencia la anterior. Así casi nunca habrá conflictos de merge.
- Los cambios a `CLAUDE.md` se hacen en **PRs pequeños y separados**, y se avisa al equipo.
- Cuando se tome una decisión de tratamiento de datos (nulos, duplicados, outliers, agregación, selección de series, etc.),
  **registrarla en `docs/DECISIONES.md`** en el mismo commit en que se implementa.

### Entorno y dependencias
- Python **3.12**. Entorno conda llamado `predict_future_sales` (también se soporta `venv` + `pip`; ver README).
- `requirements.txt` es la **fuente única de dependencias**. `environment.yml` instala desde él.
  Para agregar una librería: añadirla a `requirements.txt`, reinstalar, y avisar al equipo. No instalar
  paquetes "por fuera" que el notebook necesite sin registrarlos.
- La versión instalada de pandas es 3.x (copy-on-write activo y dtype `str` por defecto para texto):
  no depender de comportamientos de pandas 1.x/2.x como modificar un DataFrame vía encadenamiento.

### Datos
- Los CSV de Kaggle van en `data/raw/` y **nunca se suben al repositorio** (~100 MB; ya excluidos en `.gitignore`).
- `data/raw/` es inmutable: no modificar los archivos originales. Datos transformados → `data/interim/` o `data/processed/`.
- Rutas: usar las constantes de `predict_future_sales/config.py` (`RAW_DATA_DIR`, `PROCESSED_DATA_DIR`, `FIGURES_DIR`, …),
  no rutas absolutas.
- Gráficas que se quieran conservar fuera del notebook → `reports/figures/`.

### Estructura del proyecto (cookiecutter-data-science v2)
```
├── CLAUDE.md                <- Este archivo
├── README.md                <- Documentación para personas
├── docs/DECISIONES.md       <- Bitácora de decisiones
├── environment.yml          <- Entorno conda (instala desde requirements.txt)
├── requirements.txt         <- Dependencias (fuente única)
├── pyproject.toml           <- Metadatos del paquete y config de ruff
├── Makefile                 <- Comandos útiles (make requirements, make lint, make format)
├── data/
│   ├── raw/                 <- CSV originales de Kaggle (no versionados)
│   ├── interim/             <- Datos intermedios
│   ├── processed/           <- Datos finales para modelado
│   └── external/            <- Datos de terceros
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb   <- Notebook entregable del EDA (Proyecto #1)
│   ├── 02_feature_exploration.ipynb         <- Proyecto #2, punto 1: selección de lags y transformaciones
│   ├── 03_feature_creation.ipynb            <- Proyecto #2, punto 2: pipeline de preprocesamiento (.pkl)
│   ├── 04_model_training_n_tunning.ipynb    <- Proyecto #2, punto 3 (pendiente)
│   └── 05_inference_calculation.ipynb       <- Proyecto #2, punto 4 (pendiente)
├── reports/figures/         <- Figuras exportadas
├── references/              <- Diccionarios de datos, material de apoyo
├── models/                  <- Proyecto #2: archivos .pkl de los pipelines
└── predict_future_sales/    <- Paquete Python con código reutilizable
    ├── config.py            <- Rutas del proyecto
    ├── dataset.py           <- Carga / preparación de datos
    ├── features.py          <- Construcción de variables
    ├── plots.py             <- Funciones de visualización
    ├── transformers.py      <- Proyecto #2: transformadores propios del pipeline (Mapper, etc.)
    └── modeling/            <- (etapas futuras) entrenamiento y predicción
```

---

## 2. Enunciado del Proyecto #1 — EDA (transcripción completa del PDF)

### PROYECTO #1 — Exploratory Data Analysis (EDA)
**Dataset:** Predict Future Sales (Kaggle)

Para completar el EDA el grupo deberá desarrollar los siguientes pasos, trabajando sobre el dataset
**Predict Future Sales** de Kaggle. El dataset contiene las ventas diarias de una cadena de tiendas rusas
(1C Company) y el objetivo final de la competencia es predecir las ventas **mensuales** de cada par
tienda-producto para noviembre de 2015. Este EDA prepara el terreno para esa etapa de *forecasting*.

> **Uso de IA:** se permite utilizar herramientas de inteligencia artificial para desarrollar este proyecto,
> específicamente **Claude Code dentro de VSCode**.

> **Descarga del dataset:** kaggle.com/competitions/competitive-data-science-predict-future-sales/data
> (requiere cuenta gratuita de Kaggle). Los archivos se colocan en `data/raw/` y **no se suben al repositorio**.

#### Archivos del dataset

| Archivo | Contenido | Columnas |
|---|---|---|
| `sales_train.csv` | Ventas diarias históricas (train): una fila por producto vendido en una tienda un día | `date`, `date_block_num`, `shop_id`, `item_id`, `item_price`, `item_cnt_day` |
| `items.csv` | Catálogo de productos | `item_name`, `item_id`, `item_category_id` |
| `item_categories.csv` | Catálogo de categorías | `item_category_name`, `item_category_id` |
| `shops.csv` | Catálogo de tiendas (sucursales) | `shop_name`, `shop_id` |
| `test.csv` | Pares tienda-producto a predecir (nov 2015) | `ID`, `shop_id`, `item_id` |

**Nota:** `date_block_num` es el número de mes consecutivo (0 = enero 2013, 33 = octubre 2015) e
`item_cnt_day` es la cantidad vendida en el día (los valores negativos representan devoluciones).
El dataset no trae una columna de ventas en dinero: el grupo deberá construirla como
`item_price x item_cnt_day`.

#### 1. Estructura del proyecto y repositorio
- a. Descargar la plantilla de **cookiecutter** (Data Science) para definir la estructura del proyecto.
- b. Crear el notebook `01_exploratory_data_analysis.ipynb`.
- c. Crear un repositorio local con **git**.
- d. Agregar la configuración necesaria en el archivo `.gitignore` (los datos de Kaggle pesan ~100 MB y no deben versionarse).
- e. Publicar el repositorio en **GitHub**.
- f. Cada miembro del equipo deberá mostrar un *screenshot* donde hace un *pull* del repositorio para trabajar de forma local en su computadora.

#### 2. Comprensión inicial del dataset
- a. Cargar los archivos del dataset y visualizar las primeras filas de cada uno.
- b. Mostrar el tamaño de cada tabla (número de filas y columnas).
- c. Describir brevemente qué representa cada columna (`date`, `date_block_num`, `shop_id`, `item_id`,
  `item_price`, `item_cnt_day`, `item_name`, `item_category_id`, `item_category_name`, `shop_name`)
  y cuál es la variable objetivo.
- d. Identificar el rango temporal de los datos (fecha mínima y máxima) y el número de meses cubiertos.

#### 3. Validación de la estructura de los datos
- a. Verificar los tipos de datos de cada variable (fecha, numérica, categórica).
- b. Confirmar que la columna `date` esté correctamente formateada como tipo *datetime* (en el archivo original
  viene como texto con formato `dd.mm.aaaa`).
- c. Validar la frecuencia temporal: los datos son transacciones diarias, por lo que se debe revisar si existen
  días sin ventas y si `date_block_num` es consistente con la fecha. Concluir a qué frecuencia conviene agregar
  (diaria, semanal o mensual).

#### 4. Análisis de valores faltantes y duplicados
- a. Identificar columnas con valores nulos y el porcentaje de datos faltantes.
- b. Definir la estrategia para tratarlos (eliminación, imputación, etc.). Revisar además valores inválidos que no
  son nulos, como **precios menores o iguales a cero** y **cantidades negativas** (devoluciones).
- c. Verificar y justificar cómo se manejarán los registros duplicados. Revisar también si existen
  **tiendas repetidas** en `shops.csv` (mismo nombre con distinto ID).

#### 5. Análisis descriptivo general
- a. Calcular métricas estadísticas básicas: media, mediana, mínimo, máximo y desviación estándar de
  `item_price`, `item_cnt_day` y de los ingresos.
- b. Analizar la distribución de ventas por:
  - i. Producto (y categoría de producto)
  - ii. Sucursal (tienda)
  - iii. Periodo de tiempo (día, semana, mes, año)

#### 6. Exploración temporal
- a. Graficar la evolución de las ventas a lo largo del tiempo.
- b. Identificar patrones de:
  - i. Tendencia
  - ii. Estacionalidad
  - iii. Picos o caídas abruptas
  - iv. Analizar si hay ciclos por días de la semana o meses del año.

#### 7. Análisis comparativo entre sucursales y productos
- a. Identificar los productos (y categorías) más vendidos y menos vendidos.
- b. Comparar el desempeño entre sucursales.
- c. Detectar *outliers* o comportamientos anómalos por sucursal o producto (por ejemplo, transacciones con
  cantidades o precios extremadamente altos).

#### 8. Visualizaciones clave (obligatorias)
- a. Serie de tiempo de ventas totales.
- b. Gráfico de barras comparando ventas por sucursal.
- c. Gráfico de barras comparando ventas por producto (top N) y por categoría.
- d. *Heatmap* o matriz para visualizar el comportamiento de las ventas en el tiempo y por sucursal/categoría.

#### 9. Autocorrelación (ACF) y autocorrelación parcial (PACF)
Para cada serie temporal específica: **ventas totales**, **ventas por sucursal**, **ventas por producto** y
**ventas por sucursal-producto**. Dado que el dataset tiene 60 tiendas y más de 21,000 productos, se trabajará
con una selección representativa (por ejemplo, las series con más ventas). Se recomienda agregar a nivel mensual
(34 observaciones) y, para la serie total, también a nivel diario.
- a. Aplicar:
  - i. Gráfico de Autocorrelación (ACF): muestra la dependencia entre la serie y sus rezagos.
  - ii. Gráfico de Autocorrelación Parcial (PACF): ayuda a identificar la cantidad de términos AR (autorregresivos)
    que deben incluirse.
- b. Interpretar:
  - i. ¿Existen correlaciones significativas a diferentes rezagos?
  - ii. ¿Se observa estacionalidad reflejada en patrones repetitivos?

#### 10. Insights y conclusiones del EDA
- a. Identificar variables que afectan directamente las ventas.
- b. Detectar patrones útiles para el modelo de *forecasting* (incluyendo qué porcentaje de los pares
  tienda-producto de `test.csv` tiene historial en el train).
- c. Concluir sobre la calidad y preparación del dataset para las etapas siguientes del proyecto.

#### Entregables
1. Enlace al repositorio de GitHub con la estructura de cookiecutter.
2. Notebook `01_exploratory_data_analysis.ipynb` ejecutado, con gráficas e interpretaciones escritas.
3. Screenshots del *pull* de cada integrante del equipo.

---

## 3. División del trabajo (en orden de secciones; DEC-012)

| Bloque | Tema | Secciones del enunciado |
|---|---|---|
| 1 | Comprensión y calidad de los datos | 2, 3 y 4 |
| 2 | Estadísticas, exploración temporal y comparación de tiendas/productos (Marco) | 5, 6 y 7 |
| 3 | Visualizaciones clave, ACF/PACF y conclusiones (Mario) | 8, 9 y 10 |

La sección 10 la redacta el responsable del bloque 3; los otros dos integrantes la revisan y aportan antes de
integrarla a `main`.

Ramas por integrante: `alfredo`, `mario`, `marco`. Cada uno desarrolla en su rama el bloque que le toque
e integra a `main` vía Pull Request.

Dependencias entre bloques: los bloques 2 y 3 dependen de las decisiones de limpieza del bloque 1
(precios ≤ 0, devoluciones, duplicados, tiendas repetidas), ya registradas en `docs/DECISIONES.md` (DEC-006 a DEC-011).
El bloque 3 depende además del bloque 2: las agregaciones que se construyan en las secciones 5-7 (ventas mensuales,
ingreso, ventas por tienda/categoría) deben quedar como funciones en `predict_future_sales/features.py` para que
las secciones 8 y 9 las reutilicen sin reimplementarlas.

---

## 4. Estado del avance (actualizar al terminar cada bloque)

**Parte 1 (EDA) terminada e integrada a `main`** (PR #2, #3 y #4; commit `aa152a4`). El notebook se ejecuta completo sin errores.

> Si un integrante le pide a Claude "ponte al día" o "qué se ha hecho", Claude debe leer esta sección,
> `docs/DECISIONES.md` y el notebook, y resumir: qué está terminado, qué funciones usar y qué queda pendiente.

| Secciones | Estado | Responsable | Rama |
|---|---|---|---|
| 1 — Estructura y repositorio | ✅ Terminado (incluye 1.f: screenshots del pull de cada integrante) | Alfredo | `main` |
| 2, 3, 4 — Bloque 1 (comprensión, validación, faltantes/duplicados) | ✅ Terminado (PR #2) | Alfredo | `alfredo` |
| 5, 6, 7 — Bloque 2 (descriptivo, temporal, comparación) | ✅ Terminado (PR #3, DEC-013) | Marco | `marco` |
| 8, 9, 10 — Bloque 3 (visualizaciones, ACF/PACF, conclusiones) | ✅ Terminado (PR #4, DEC-014) | Mario | `mario` |

### Cómo trabajar sobre los datos limpios

El notebook ya deja la variable `sales_train` **limpia** al final de la sección 4. Para trabajar fuera del notebook
o reconstruirla desde cero, usar las funciones de `predict_future_sales/dataset.py` (no reimplementar la limpieza):

| Función / constante | Qué hace | Decisión |
|---|---|---|
| `cargar_datos()` | Lee los 5 CSV crudos de `data/raw/` en un dict (`sales_train`, `items`, `item_categories`, `shops`, `test`) | — |
| `convertir_cantidad_entera(df)` | `item_cnt_day` → `int64` | DEC-006 |
| `convertir_fecha(df)` | `date` (texto `dd.mm.aaaa`) → `datetime64` | DEC-006 |
| `limpiar_sales_train(df)` | Elimina 6 duplicados exactos, corrige el precio -1, unifica tiendas 0→57, 1→58, 11→10 | DEC-009, 010, 011 |
| `cargar_ventas_limpias()` | Atajo: todo lo anterior en un paso → `sales_train` limpio (2,935,843 filas, 57 tiendas) | — |
| `MAPEO_TIENDAS_DUPLICADAS` | `{0: 57, 1: 58, 11: 10}` | DEC-011 |

Agregaciones y utilidades de los bloques 2 y 3 (`predict_future_sales/features.py` y `plots.py`):

| Función | Qué hace | Decisión |
|---|---|---|
| `preparar_ventas(df)` | Agrega `ingresos = item_price × item_cnt_day` (netos, con devoluciones) | DEC-013 |
| `resumen_ventas(df, dims)` | Unidades netas, ingresos netos y registros por las dimensiones indicadas | DEC-013 |
| `ventas_por_periodo(df, frecuencia)` | Totales de la cadena por día (`D`), semana (`W-SUN`), mes (`MS`) o año (`YS`) | DEC-013 |
| `ventas_mensuales_por(df, dims)` | Ventas por `date_block_num` y dimensiones (representación dispersa, sin ceros) | DEC-007 |
| `serie_mensual(df, shop_id=, item_id=)` | Serie de 34 meses con ceros para una tienda, producto o par | DEC-008 |
| `agregar_grupo_categoria(item_categories)` | Agrega `grupo_categoria` (14 grupos en español, `GRUPOS_CATEGORIA_ES`) | DEC-014 |
| `matriz_mensual(df, dimension)` | Matriz dimensión × mes (0-33) para heatmaps | DEC-008 |
| `cobertura_test(test, df)` | Clasifica los pares de `test` por historial en train | — |
| `resumen_autocorrelacion(serie, nlags)` | Rezagos significativos de ACF/PACF y p-valor ADF | DEC-014 |
| `plots.py` | Colores, `barras_horizontales`, `graficar_acf_pacf`, `guardar_figura` (escribe en `reports/figures/`) | — |

**Reglas que ya están decididas (no cambiarlas sin una nueva entrada en DECISIONES.md):**
- Frecuencia de análisis **mensual** con `date_block_num`; diaria solo para la serie total (sección 9) y día de la semana (sección 6) — DEC-007.
- Las **devoluciones se conservan** (restan de las ventas netas) — DEC-009.
- Meses sin registros = **ventas 0**, no nulos — DEC-008.
- `ingresos = item_price × item_cnt_day`, netos (con devoluciones); se crea con `preparar_ventas()` — DEC-013.
- No se recortan extremos durante el EDA; recortar (p. ej. a [0, 20]) se decide en modelado — DEC-009, DEC-013.
- `shops.csv` sigue teniendo 60 filas: al cruzar con nombres de tienda, las tiendas 0, 1 y 11 ya no aparecen en `sales_train`.

### Datos clave del dataset (resultados del bloque 1)
- `sales_train`: 2,935,849 filas crudas → 2,935,843 limpias; 01-01-2013 a 31-10-2015 (1,034 días, 34 meses, `date_block_num` 0-33, 100 % consistente con la fecha).
- Catálogos: 22,170 productos, 84 categorías, 60 tiendas (57 tras unificar). `test`: 214,200 pares.
- Sin nulos. 7,356 devoluciones (0.25 %). Dispersión tienda-producto: 0.67 % diaria, 3.69 % semanal, 11.16 % mensual.
- Solo 32 de 60 tiendas venden en los 34 meses; 15 abrieron después de ene-2013 y 16 dejaron de vender antes de oct-2015.

### Hallazgos pendientes para otras secciones
- **5 / 7 / 8 (nombres en ruso, bloques 2 y 3):** está acordado (aún no hecho) traducir **solo** categorías (84) y tiendas (60) en
  `references/traduccion_categorias.csv` y `references/traduccion_tiendas.csv` (con `grupo`/`subgrupo` y `ciudad`),
  revisadas por el equipo; los productos (22,170) no se traducen salvo el top N de las gráficas. Requiere agregar
  `!references/*.csv` al `.gitignore` y registrar la decisión (será DEC-013). Los originales en ruso nunca se modifican.
- ✅ **7.c (outliers):** resuelto en 7.c y 8.b (p99.9 de cantidad = 22, máximo 2,169; tiendas de evento 9 y 20, en línea 12, nueva 36).
- ✅ **6 (temporal):** resuelto en 6 y 8.a (picos de diciembre, ciclo semanal).
- ✅ **10.b:** resuelto: 52.04 % de los pares de `test` tiene historial, 40.84 % producto conocido en par nuevo, 7.12 % producto nuevo.
- **Memoria:** `sales_train` ocupa ~290 MB; si un equipo tiene poca RAM, considerar tipos más livianos (registrar decisión).
- **Notebook:** con las gráficas crecerá de tamaño; acordar que una sola persona re-ejecute el notebook completo antes de cada integración a `main`.

---

## 5. Enunciado del Proyecto #2 — Pipeline de Machine Learning (transcripción completa del PDF)

### PROYECTO #2 — Pipeline de Machine Learning
**Ingeniería de características, entrenamiento e inferencia** · Dataset: Predict Future Sales (Kaggle)

Esta fase continúa el proyecto anterior (EDA). El grupo deberá utilizar toda la información que recabó y desarrolló
en la fase previa para construir el **pipeline completo de preprocesamiento, entrenamiento e inferencia** sobre el
dataset **Predict Future Sales** de Kaggle. Antes de iniciar, se recomienda fuertemente investigar cómo funcionan
los modelos de *forecasting* que utilizan variables externas o de segregación, de modo que los valores de **tienda y
producto** se manejen como **variables exógenas** y parte de la estructura del modelo.

> **Uso de IA:** se permite utilizar herramientas de inteligencia artificial para desarrollar este proyecto,
> específicamente **Claude Code dentro de VSCode**.

> **Variable objetivo:** `item_cnt_month`, es decir, las unidades vendidas por mes para cada par tienda-producto (se
> obtiene agregando `item_cnt_day` por `date_block_num`). El archivo `test.csv` contiene los pares tienda-producto de
> **noviembre de 2015** (`date_block_num = 34`), un mes que el modelo no ha visto. La métrica de la competencia es el **RMSE**.

#### Resumen de la fase

| Notebook | Contenido | Salida |
|---|---|---|
| `02_feature_exploration.ipynb` | Análisis y selección de las operaciones de ingeniería de características y de los *lags* | Lista escrita de variables y transformaciones |
| `03_feature_creation.ipynb` | Pipeline de sklearn con los pasos de ingeniería de características | Archivo `.pkl` del pipeline de preprocesamiento |
| `04_model_training_n_tunning.ipynb` | Entrenamiento, ajuste y selección de modelos (RMSE) | Archivo `.pkl` del pipeline completo (preprocesamiento + modelo ganador) |
| `05_inference_calculation.ipynb` | Inferencia sobre `test.csv` | Archivo `.csv` con las predicciones |

#### 1. Notebook `02_feature_exploration.ipynb`
Cree el notebook para el análisis y la selección del proceso de ingeniería de características y realice los siguientes pasos:
- a. Cargar el dataset definido en los notebooks anteriores y, utilizando la investigación desarrollada sobre las
  relaciones entre las ventas y las demás variables, determinar qué **lags** son los más adecuados para desarrollar
  modelos de *forecasting*. Se recomienda trabajar a nivel mensual por par tienda-producto, rellenando con cero
  los meses sin ventas.
- b. Aplicar **al menos una operación** de cada uno de los procesos de ingeniería de características, indicando el
  **criterio de selección** de la operación. Si el dataset está completo o no es necesario aplicar alguno de estos
  procesos, se deberá **forzar** que sea posible aplicarlos (por ejemplo, eliminando algunos datos de forma
  aleatoria). Lo importante es aplicar al menos una transformación de cada proceso. No es necesario crear
  ningún operador, ya que se definirá en la siguiente fase. Los procesos son:
  - i. Imputación de variables numéricas.
  - ii. Imputación de variables categóricas.
  - iii. Codificación de variables categóricas (por ejemplo, tienda, categoría de producto o ciudad extraída del nombre de la tienda).
  - iv. Tratamiento de *outliers* (por ejemplo, cantidades o precios extremos detectados en el EDA).
  - v. Transformación de variables numéricas.
  - vi. Escalado de características.
- c. Al finalizar, listar con palabras el proceso: definir la **lista de variables** a las que se aplicará cada
  transformación, así como los **mecanismos de mapeo** que se consideren necesarios (similares a los vistos en clase).

> **Cuidado con la fuga de información:** cada *lag* debe construirse únicamente con meses anteriores al mes que se
> predice. Para el mes 34 del test, los *lags* se obtienen de los meses 33, 32, 31, etc.

#### 2. Notebook `03_feature_creation.ipynb`
- a. Crear el proceso de elaboración del **pipeline de ingeniería de características** para el preprocesamiento de los
  datos del modelo, usando la información generada en el paso anterior.
- b. Es necesario crear el pipeline con **sklearn**. De ser necesario, puede usar el operador **Mapper** definido durante
  las sesiones de clase.
- c. Como resultado, el notebook debe generar un archivo `.pkl` donde se establezcan todos los pasos de ingeniería
  de características definidos en la fase anterior.

#### 3. Notebook `04_model_training_n_tunning.ipynb`
Defina todo el proceso de entrenamiento y selección de modelos:
- a. Utilizar **al menos 5 modelos distintos**.
- b. Optimizar hiperparámetros probando **al menos 3 configuraciones** distintas por modelo, en los casos en que
  sea posible. En total, deberán entrenarse **15 modelos**.
- c. Utilizar el **RMSE** como métrica para la selección del modelo.
- d. El modelo ganador deberá predecir las ventas (`item_cnt_month`) considerando los valores de **tienda y
  producto como variables exógenas o banderas**. Este modelo se agrega como **paso final** del pipeline de
  preprocesamiento.
- e. Como salida, el notebook deberá generar un archivo `.pkl` con el **pipeline completo**, incluyendo los pasos de
  preprocesamiento y el modelo ganador.

> **Nota importante:** para medir la eficiencia de un modelo de *forecasting* es necesario definir un set de entrenamiento y
> un set de validación, pero en este tipo de modelos se utiliza el **primer 80 % de los datos para entrenamiento y el 20 %
> restante para validación**, seleccionados de forma **secuencial y no aleatoria** (a diferencia de los modelos de regresión
> o clasificación). Con los 34 meses del dataset, esto equivale aproximadamente a entrenar con los meses `0 a 26` y validar
> con los meses `27 a 33`.

#### 4. Notebook `05_inference_calculation.ipynb`
- a. Como paso final, crear un notebook que haga uso del **pipeline completo** (archivo `.pkl` del paso anterior) para
  generar predicciones de un dataset que el modelo no ha visto anteriormente: `test.csv`.
- b. Como salida, generar un archivo `.csv` con las predicciones correspondientes al dataset de testing, con las
  columnas `ID` e `item_cnt_month` (formato de envío de Kaggle).

#### Entregables
1. Repositorio de GitHub actualizado con los notebooks `02` a `05` ejecutados, con sus explicaciones escritas.
2. Archivo `.pkl` del pipeline de ingeniería de características.
3. Archivo `.pkl` del pipeline completo (preprocesamiento + modelo ganador).
4. Archivo `.csv` con las predicciones sobre el dataset de testing.

---

## 6. Estado del avance — Proyecto #2 (actualizar al terminar cada punto)

| Punto | Notebook | Estado | Responsable | Decisiones |
|---|---|---|---|---|
| 1 | `02_feature_exploration.ipynb` | ✅ Terminado y ejecutado | Alfredo | DEC-015, DEC-016 |
| 2 | `03_feature_creation.ipynb` | ✅ Terminado y ejecutado → `models/pipeline_preprocesamiento.pkl` | Alfredo | DEC-017 |
| 3 | `04_model_training_n_tunning.ipynb` | ⏳ Pendiente | (por asignar) | — |
| 4 | `05_inference_calculation.ipynb` | ⏳ Pendiente | (por asignar) | — |

**Rama del Proyecto #2: `proyecto_2_pipeline_predict`.** Todo el trabajo de los puntos 1 a 4 se sube a esta rama y,
por ahora, **no se integra a `main`**. Validar con `git branch --show-current` antes de cada commit y push.

### Resultado del punto 1 (lo que necesitan los puntos 2, 3 y 4)
La **receta completa** está en la sección **1.c** de `02_feature_exploration.ipynb`. Resumen:
- **Datos:** cuadrícula mensual tienda × producto con ceros (`construir_cuadricula_mensual()`, 11,128,050 filas) con los
  pares de `test` como mes 34. **Partición:** entrenamiento 0-26, validación 27-33, test 34 (`MES_FIN_ENTRENAMIENTO`).
- **Objetivo:** `y = item_cnt_month` recortado a [0, 20] (`LIMITES_OBJETIVO`).
- **Lags** (`LAGS_SELECCIONADOS`, `agregar_lags()`, sin fuga): par 1, 2, 3, 12 · producto 1 · tienda 1, 12 · categoría 1, 12.
- **Otras variables:** `precio_previo` (`precio_previo_item()`), `meses_desde_primera_venta` (`antiguedad_item()`) y la
  bandera `item_sin_historia`; `ciudad` y `tipo_tienda` (`agregar_info_tienda()`); `grupo_categoria` (DEC-014).
- **Transformaciones:** imputación (lags y antigüedad → 0; precio → mediana de la categoría; categóricas → "Desconocido"),
  tope p99.9 al precio, `log1p` **solo** al precio (no a los lags), one-hot de grupo y tipo de tienda, frecuencia de ciudad,
  `StandardScaler`. Todo lo aprendido se ajusta **solo con los meses 0-26**.
- **32 variables de entrada.** `item_id` **no** entra como variable (empeora el modelo de árboles); sí `shop_id` e
  `item_category_id`.
- **Para el notebook 04:** reentrenar el modelo ganador con los meses 0-33 antes de predecir el mes 34 (cambio en el tiempo).
- Referencia rápida del punto 1 en validación (meses 27-33): regresión lineal RMSE 0.8730; `HistGradientBoostingRegressor`
  sin ajustar RMSE 0.8210; predecir siempre 0 = 1.116.
- El notebook 02 tarda ~8 minutos en ejecutarse completo (las comprobaciones adicionales entrenan modelos con ~9 millones de filas).

### Resultado del punto 2 (lo que necesitan los puntos 3 y 4)
- **Pipeline ajustado (meses 0-26):** `models/pipeline_preprocesamiento.pkl` (cargar con `joblib.load`). Recibe la tabla de
  `construir_tabla_modelo(ventas, items, test)` y devuelve las **32 variables**; descarta `item_id`, `date_block_num`,
  `item_cnt_month` e `y`. El objetivo es `tabla["y"]` (no entra al pipeline).
- **Clases propias** en `predict_future_sales/transformers.py` (`Mapper`, `IndicadorNulo`, `ImputadorMedianaPorGrupo`,
  `TopeCuantil`, `CodificadorFrecuencia`): el paquete debe estar instalado (`pip install -e .`) para abrir el `.pkl`.
- **Referencia en validación (27-33):** lineal 0.8730 · `HistGradientBoostingRegressor` sin ajustar 0.8237.
- **Para el notebook 04:** `Pipeline([("preprocesamiento", <pkl>), ("modelo", modelo)])`; para la predicción final,
  `sklearn.base.clone()` del pipeline completo y reajustar con los meses 0-33.
- El notebook 03 tarda ~1.5 minutos en ejecutarse.
