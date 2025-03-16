# 🎰 Analizador de Datos de Lotería

## 📌 Descripción
Este proyecto es un analizador de datos de lotería desarrollado en Python. Permite extraer información de sorteos pasados, analizar la frecuencia de números y detectar patrones para realizar predicciones básicas.

## 🚀 Características
- Análisis de frecuencia de números en sorteos previos.
- Generación de gráficos estadísticos.
- Uso de algoritmos matemáticos para identificar patrones.
- Predicciones básicas basadas en datos históricos.

## 🛠️ Tecnologías Utilizadas
- **Python 3.11**
- **Pandas** (Manejo de datos)
- **NumPy** (Cálculo numérico)
- **Matplotlib** (Visualización de datos)
- **SciPy** (Análisis estadístico)
- **FastAPI** (API para consulta de datos)
- **Docker & Docker Compose** (Contenedorización y despliegue)

## 📁 Estructura del Proyecto
```
📦 Analizer
│   ├── main.py        # Archivo principal de la API
│   ├── models.py      # Modelos de datos
│   ├── analysis.py    # Funciones de análisis y estadísticas
│   ├── utils.py       # Utilidades generales
│── requirements.txt   # Dependencias del proyecto
│── Dockerfile         # Configuración del contenedor
│── docker-compose.yml # Orquestación con Docker Compose
│── README.md          # Documentación del proyecto
```

## ⚡ Instalación y Ejecución
### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/analizer.git
cd analizer
```

### 2️⃣ Configurar entorno con Docker
#### Construir y ejecutar el contenedor
```bash
docker-compose up --build -d
```
#### Detener los contenedores
```bash
docker-compose down
```

### 3️⃣ Acceder a la API
Una vez en ejecución, puedes acceder a la API en:
- **http://localhost:8000/docs** (Interfaz Swagger para probar la API)

## 📝 Contribuciones
Si deseas mejorar este proyecto, ¡tus contribuciones son bienvenidas! Por favor, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una nueva rama (`feature-nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m "Añadida nueva funcionalidad"`).
4. Envía un pull request para revisión.

## 📜 Licencia
Este proyecto está bajo la licencia MIT. ¡Úsalo libremente y contribuye! 🚀
