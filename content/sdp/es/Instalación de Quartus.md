---
title: Instalación de Quartus en tu ordenador
draft: false
tags:
  - herramientas
---

prev > [inicio](sdp/es/index)

*Por Ricardo José Colom Palero*

Uno de los objetivos de esta asignatura es que todos los diseños digitales que se realicen no se verifiquen únicamente mediante simulación, sino que también se prueben físicamente sobre hardware. En el laboratorio disponemos de la placa de evaluación **DE2-115**, desarrollada por Terasic junto con Altera dentro de su programa universitario. Junto con el hardware se emplea el programa **Quartus** de Altera (hoy Intel FPGA) para la realización de los diseños digitales.

La placa DE2-115 dispone de una FPGA de la familia **Cyclone IV E** de Altera, concretamente el dispositivo **EP4CE115F29C7**. En las prácticas se utiliza la versión **17.1.1 Internal Build 593** de Quartus, que ya está instalada en el laboratorio. A continuación se explica cómo conseguir esta misma versión para trabajar en tu ordenador sin problemas de compatibilidad.

## Descarga

El siguiente enlace lleva al centro de descargas de Intel FPGA: [Intel FPGA Download Center](https://www.intel.com/content/www/us/en/collections/products/fpga/software/downloads.html)

![[assets/Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.30.48.png]]

En esa página se puede buscar «17.1» para reducir el número de opciones. Después hay que elegir **Intel Quartus Prime Lite Edition Design Software Version 17.1 for Windows** (o Linux, si es tu sistema operativo).

> [!warning] Cuidado
> Elige la edición **Lite**, que es gratuita, y no las ediciones **Standard** o **Pro**, que son de pago.

![[assets/Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.41.16.png]]

En la pestaña **Multiple Download**, el botón *Download* descarga un archivo de 5,8 GB con la versión completa y gratuita de Quartus. Es la forma más sencilla de obtener el software, aunque incluye más componentes de los necesarios.

Si el tamaño te parece excesivo, puedes descargar solo los paquetes que se van a usar desde la pestaña **Individual Files**. Como muestra la imagen, para las asignaturas de este grado basta con:

- Quartus Prime (includes Nios II EDS), 1,7 GB.
- ModelSim-Intel FPGA Edition (includes Starter Edition), 1,1 GB.
- Cyclone IV device support, 466,6 MB.

![[assets/Instalar Quartus/Captura de Pantalla 2022-09-15 a las 15.40.05.png]]

## Instalación y actualización

Una vez descargados los archivos, instala Quartus siguiendo las instrucciones de la propia página web.

Para la versión 17.1 existe una actualización que lleva a la **17.1.1 Internal Build 593**, la misma del laboratorio. Se descarga desde la pestaña **Updates**, como se ve en la imagen; solo hay que seguir las instrucciones de la página para instalarla.

![[assets/Instalar Quartus/Captura de Pantalla 2022-09-15 a las 16.23.00.png]]

next > [[Crear QAR]]
