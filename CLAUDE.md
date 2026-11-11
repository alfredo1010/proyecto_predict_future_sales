# CLAUDE.md — Contexto del proyecto para Claude Code

Este archivo lo lee Claude Code automáticamente al abrir el proyecto. Contiene el **enunciado completo**
del proyecto (fuente oficial, transcrita del PDF del curso) y las **reglas de trabajo del equipo**.
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
- El entregable es **un solo notebook**: `notebooks/01_exploratory_data_analysis.ipynb`, con secciones
  ya creadas para los 10 puntos del enunciado.
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
│   └── 01_exploratory_data_analysis.ipynb   <- Notebook entregable del EDA
├── reports/figures/         <- Figuras exportadas
├── references/              <- Diccionarios de datos, material de apoyo
├── models/                  <- (etapas futuras) modelos entrenados
└── predict_future_sales/    <- Paquete Python con código reutilizable
    ├── config.py            <- Rutas del proyecto
    ├── dataset.py           <- Carga / preparación de datos
    ├── features.py          <- Construcción de variables
    ├── plots.py             <- Funciones de visualización
    └── modeling/            <- (etapas futuras) entrenamiento y predicción
```

---

## 2. Enunciado del proyecto (transcripción completa del PDF)

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

## 3. División del trabajo (en orden de secciones; DEC-012; bloques 2 y 3 aún no asignados a personas)

| Bloque | Tema | Secciones del enunciado |
|---|---|---|
| 1 | Comprensión y calidad de los datos | 2, 3 y 4 |
| 2 | Estadísticas, exploración temporal y comparación de tiendas/productos | 5, 6 y 7 |
| 3 | Visualizaciones clave, ACF/PACF y conclusiones | 8, 9 y 10 |

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

> Si un integrante le pide a Claude "ponte al día" o "qué se ha hecho", Claude debe leer esta sección,
> `docs/DECISIONES.md` y el notebook, y resumir: qué está terminado, qué funciones usar y qué queda pendiente.

| Secciones | Estado | Responsable | Rama |
|---|---|---|---|
| 1 — Estructura y repositorio | ✅ Terminado (falta 1.f: screenshots del pull de cada integrante) | Alfredo | `main` |
| 2, 3, 4 — Bloque 1 (comprensión, validación, faltantes/duplicados) | ✅ Terminado y ejecutado en el notebook | Alfredo | `alfredo` |
| 5, 6, 7 — Bloque 2 (descriptivo, temporal, comparación) | ⏳ Pendiente | (por asignar) | — |
| 8, 9, 10 — Bloque 3 (visualizaciones, ACF/PACF, conclusiones) | ⏳ Pendiente (10 revisada por los tres) | (por asignar) | — |

### Cómo empezar a trabajar sobre los datos limpios (bloques 2 y 3)

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

**Reglas que ya están decididas (no cambiarlas sin una nueva entrada en DECISIONES.md):**
- Frecuencia de análisis **mensual** con `date_block_num`; diaria solo para la serie total (sección 9) y día de la semana (sección 6) — DEC-007.
- Las **devoluciones se conservan** (restan de las ventas netas) — DEC-009.
- Meses sin registros = **ventas 0**, no nulos — DEC-008.
- `ingreso = item_price × item_cnt_day` (aún no está creada; se construye en la sección 5).
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
- **7.c (outliers):** cantidad máxima de 2,169 unidades en un día; revisar precios y cantidades extremos.
  Tiendas especiales: **9** (`Выездная Торговля`, venta itinerante: 14 días con ventas en 742) y **20**
  (`Москва "Распродажа"`, liquidación: 9 días en 368) son tiendas de evento; **12** es tienda en línea; **36** abrió el 18-10-2015.
- **6 (temporal):** transacciones por día entre 1,123 y 9,434 (mediana ~2,590): hay picos marcados.
- **10.b:** `test` es una cuadrícula completa de 42 tiendas × 5,100 productos; calcular el % de pares con historial en train.
- **Memoria:** `sales_train` ocupa ~290 MB; si un equipo tiene poca RAM, considerar tipos más livianos (registrar decisión).
- **Notebook:** con las gráficas crecerá de tamaño; acordar que una sola persona re-ejecute el notebook completo antes de cada integración a `main`.
