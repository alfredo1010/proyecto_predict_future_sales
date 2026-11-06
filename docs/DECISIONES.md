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
