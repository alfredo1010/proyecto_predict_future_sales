# Predict Future Sales — Proyecto #1: EDA

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Análisis exploratorio de datos (EDA) del dataset **Predict Future Sales** de Kaggle: ventas diarias de una
cadena de tiendas rusas (1C Company). El objetivo final de la competencia es predecir las ventas **mensuales**
de cada par tienda-producto para noviembre de 2015; este EDA prepara el terreno para esa etapa de *forecasting*.

**Curso:** Product Development

## Integrantes

- alfredo.mux@galileo.edu
- marco.garcia@galileo.edu
- 25005795@galileo.edu

## División del trabajo

| Bloque | Tema | Secciones | Rama |
|---|---|---|---|
| 1 | Comprensión y calidad de los datos | 2, 3 y 4 | `feature/calidad-datos` |
| 2 | Estadísticas, comparación de tiendas/productos y visualizaciones | 5, 7 y 8 | `feature/descriptivo-visualizaciones` |
| 3 | Comportamiento temporal y autocorrelaciones | 6 y 9 | `feature/temporal-acf` |
| Los tres | Conclusiones, interpretación y validación final | 10 | — |

La asignación de bloques a integrantes está pendiente de definir. El enunciado completo está en [CLAUDE.md](CLAUDE.md).

---

## Requisitos

| Herramienta | Para qué |
|---|---|
| [Git](https://git-scm.com/) + cuenta de GitHub (con acceso al repo) | Control de versiones |
| Python **3.12** | Lenguaje del proyecto |
| Conda (Anaconda / Miniconda) **o** `venv` + `pip` | Gestor de entorno (cualquiera de los dos) |
| VSCode + extensiones **Python** y **Jupyter** | Editor y notebooks |
| Claude Code (extensión de VSCode) | Asistente de IA permitido en el proyecto |
| Cuenta gratuita de Kaggle | Descargar el dataset |

## Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/alfredo1010/proyecto_predict_future_sales.git
cd proyecto_predict_future_sales
```

### 2. Configurar tu identidad en git (una sola vez por computadora)

Cada integrante hace sus commits con **su propio nombre y correo**; el historial es la evidencia del trabajo de cada uno.

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@galileo.edu"
```

### 3. Crear el entorno

**Opción A — Conda (recomendado):**

```bash
conda env create -f environment.yml
conda activate predict_future_sales
```

**Opción B — venv + pip** (requiere Python 3.12 instalado):

```bash
python3.12 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Ambas opciones instalan las mismas librerías (`environment.yml` instala desde `requirements.txt`) y el
paquete del proyecto `predict_future_sales` en modo editable.

> Para agregar una librería: añadirla a `requirements.txt`, reinstalar
> (`conda env update -f environment.yml --prune` o `pip install -r requirements.txt`) y avisar al equipo.

### 4. Descargar los datos

1. Ir a <https://www.kaggle.com/competitions/competitive-data-science-predict-future-sales/data>
   (iniciar sesión y aceptar las reglas de la competencia).
2. Descargar y descomprimir los archivos en **`data/raw/`**:
   `sales_train.csv`, `items.csv`, `item_categories.csv`, `shops.csv`, `test.csv`.

Los datos **no se suben al repositorio** (están excluidos en `.gitignore`).

### 5. Verificar

En VSCode abrir `notebooks/01_exploratory_data_analysis.ipynb`, seleccionar el kernel del entorno
`predict_future_sales` (o `.venv`) y ejecutar las primeras celdas de carga de datos.

---

## Flujo de trabajo en equipo

1. Antes de empezar: `git checkout main && git pull`, luego cambiar a tu rama y traer los cambios de `main`.
2. Trabajar en la rama del bloque (`feature/...`); **nunca directamente en `main`**.
3. Avisar al equipo antes y después de modificar el notebook compartido.
4. Registrar cada decisión de tratamiento de datos en [docs/DECISIONES.md](docs/DECISIONES.md) (solo agregar entradas al final).
5. Hacer commit y push desde **tu propia computadora** y abrir un Pull Request hacia `main`.

## Entregables

- [ ] Enlace al repositorio de GitHub con la estructura de cookiecutter.
- [ ] Notebook `01_exploratory_data_analysis.ipynb` ejecutado, con gráficas e interpretaciones escritas.
- [ ] Screenshots del *pull* de cada integrante del equipo.

---

## Organización del proyecto

```
├── CLAUDE.md              <- Contexto para Claude Code: enunciado completo y reglas de trabajo
├── README.md              <- Este archivo
├── Makefile               <- Comandos útiles (make requirements, make lint, make format)
├── environment.yml        <- Entorno conda (instala desde requirements.txt)
├── requirements.txt       <- Dependencias del proyecto
├── pyproject.toml         <- Metadatos del paquete predict_future_sales y configuración de ruff
├── data
│   ├── external           <- Datos de fuentes externas
│   ├── interim            <- Datos intermedios transformados
│   ├── processed          <- Datos finales para modelado
│   └── raw                <- Datos originales de Kaggle (inmutables, no versionados)
├── docs
│   └── DECISIONES.md      <- Bitácora de decisiones del equipo
├── models                 <- Modelos entrenados (etapas futuras)
├── notebooks
│   └── 01_exploratory_data_analysis.ipynb  <- Notebook entregable del EDA
├── references             <- Diccionarios de datos y material de apoyo
├── reports
│   └── figures            <- Gráficas exportadas
└── predict_future_sales   <- Código fuente reutilizable
    ├── __init__.py
    ├── config.py          <- Rutas y configuración
    ├── dataset.py         <- Carga y preparación de datos
    ├── features.py        <- Construcción de variables
    ├── modeling           <- Entrenamiento y predicción (etapas futuras)
    └── plots.py           <- Funciones de visualización
```
