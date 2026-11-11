---
title: "Ayuda: creación de archivos QAR"
draft: false
tags:
  - herramientas
---

prev > [[sdp/es/instalacion-quartus|Ayuda: instalación de Quartus]]

Cuando se trabaja con una herramienta de diseño electrónico como Quartus, a menudo hay que copiar el trabajo, ya sea para compartirlo o para continuarlo en otro ordenador. Como Quartus trabaja con proyectos, lo primero que se nos ocurre es copiar toda la carpeta del proyecto o comprimirla.

Hay una alternativa mucho mejor: Quartus incluye una utilidad que empaqueta el proyecto en un único archivo con extensión **.QAR**, incluyendo solo los ficheros necesarios. Sus ventajas son que selecciona automáticamente los ficheros imprescindibles mediante configuraciones predefinidas, con lo que el archivo es lo más pequeño posible, y que, como la extensión **.QAR** está asociada a Quartus, basta un doble clic para desempaquetar el proyecto y abrirlo.

## Procedimiento

1. En el menú de Quartus selecciona **Project > Archive Project**. Se abre la ventana **Archive Project**:
   ![[assets/generar-qar/imagen009.jpg]]
2. Escribe el nombre del archivo en **Archive file name**.
3. Pulsa **Advanced...** para abrir la ventana que permite elegir qué ficheros se incluyen:
   ![[assets/generar-qar/imagen012.jpg]]
4. En **File set** selecciona la configuración **Service request**:
   ![[assets/generar-qar/imagen011.jpg]]
5. Pulsa **OK** para volver a **Archive Project**.
6. Pulsa **Archive**. Quartus crea un archivo con el nombre indicado y extensión **.QAR** con los ficheros del proyecto, en la carpeta del proyecto salvo que hayas elegido otra.

> [!tip] Ficheros de inicialización de memoria
> Los ficheros `.hex` o `.mif` que inicializan memorias no siempre se incluyen por defecto. Añádelos a mano en la ventana **Advanced...** con el botón **Add...**.

## Comprobación del archivo

Conviene desempaquetar el **.QAR** y abrirlo en Quartus para comprobar que su contenido es correcto.

> [!danger] No lo desempaquetes en la carpeta del proyecto original
> El proyecto podría corromperse. Copia el **.QAR** a otra carpeta y haz doble clic sobre él: Quartus se abrirá, desempaquetará el proyecto en una carpeta llamada `<nombre_proyecto>_restored` y lo abrirá.

next > [[sdp/es/proyecto1-juego-luces|Proyecto 1: Diseño de un juego de luces]]
