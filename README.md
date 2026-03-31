# primer_dia_de_la_oficina

Esta carpeta contiene un ejercicio de programación lineal y una aplicación Flask para analizar los datos CSV disponibles en `data/`.

## Archivos principales

- `ejercicio_programacion_lineal.py`: Resuelve el problema de optimizar el poder del ejército con recursos limitados.
- `app.py`: App Flask que carga y analiza los datos de la carpeta `data/`.
- `requirements.txt`: Dependencias necesarias para ejecutar la app Flask.

## Cómo ejecutar la app Flask

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación:

   ```bash
   python app.py
   ```

3. Abre en tu navegador:

   ```text
   http://127.0.0.1:5000/
   ```

## Qué analiza la app

- resumen de los archivos CSV seleccionados
- análisis de batallas (`battles.csv`)
- análisis de clima (`weather.csv`)
- análisis de terreno (`terrain.csv`)
- solución de optimización del ejército usando programación lineal
