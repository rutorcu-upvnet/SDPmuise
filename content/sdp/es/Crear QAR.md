---
title: Archivar un proyecto de Quartus (crear QAR)
draft: false
tags:
  - herramientas
---

prev > [[Instalación de Quartus]]

*Por Ricardo José Colom Palero*

Cuando se trabaja con una herramienta de diseño electrónico como Quartus siempre surge la necesidad de copiar el trabajo para llevarlo a otros equipos. Como Quartus trabaja con proyectos, lo más inmediato es copiar todo el directorio del proyecto o comprimirlo en un archivo.

Sin embargo, Quartus incluye una utilidad que empaqueta el proyecto en un único archivo con extensión **.qar**, seleccionando solo los archivos necesarios. Su ventaja es doble: elige automáticamente los archivos realmente necesarios mediante configuraciones predefinidas y, como la extensión **.qar** está asociada a Quartus, basta un doble clic sobre el archivo para desempaquetar el proyecto y abrirlo.

## Procedimiento

1. En el menú de Quartus selecciona **Project > Archive Project**. Se abre la ventana **Archive Project**:
   ![[assets/Generar QAR/Imagen009.jpg]]
2. Escribe un nombre para el archivo en el campo **Archive file name**.
3. Pulsa **Advanced...** para abrir la ventana que permite personalizar los archivos que se incluirán:
   ![[assets/Generar QAR/Imagen012.jpg]]
4. En **File set** selecciona la configuración predefinida **Service request**:
   ![[assets/Generar QAR/Imagen011.jpg]]
5. Pulsa **OK** para volver a la ventana **Archive Project**.
6. Pulsa **Archive**. Se crea el archivo con el nombre indicado y extensión **.qar**, que contiene los archivos del proyecto. Se guarda en el directorio del proyecto, salvo que se haya indicado otra ubicación.

## Comprobación del archivo

Una vez generado el **.qar**, conviene comprobar su contenido descomprimiéndolo.

> [!danger] No lo descomprimas en la carpeta del proyecto original
> Copia el archivo **.qar** a otra carpeta y haz doble clic sobre él: Quartus se abrirá, desempaquetará el proyecto en una carpeta llamada `nombre_proyecto_restored` y lo abrirá.

next > [[Tarea 1 - Diseño de sistemas secuenciales]]
