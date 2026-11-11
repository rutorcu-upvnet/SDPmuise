# Recursos pendientes

No queda ningún recurso pendiente: todas las imágenes, ficheros, animaciones y vídeos que enlazan las prácticas (versión de PoliformaT **GRA_12412_2026**, Proyectos 1–4) están en el repo.

Si en el futuro cambian los recursos en PoliformaT, descarga **Recursos › Contenido Lessons**, descomprímelo y ejecuta

```bash
python3 scripts/importar-recursos.py "/ruta/a/Contenido Lessons"          # solo copia lo que falte
python3 scripts/importar-recursos.py "/ruta/a/Contenido Lessons" --todo   # sobrescribe todo
```

El script reconoce los nombres saneados del zip de PoliformaT, copia cada fichero a su destino con nombre ASCII, lista los que no encuentre y avisa si algún vídeo supera el límite de 100 MB de GitHub.
