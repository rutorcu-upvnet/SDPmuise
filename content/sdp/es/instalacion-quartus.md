---
title: "Ayuda: instalación de Quartus"
draft: false
tags:
  - herramientas
---

prev > [[sdp/es/index|inicio]]

Para las prácticas de la asignatura se usa el software **Quartus** de Altera. En los ordenadores del laboratorio está instalada la versión **17.1.1 Internal Build 593**. Es posible (y recomendable) instalar esa misma versión en tu ordenador para trabajar también fuera del laboratorio sin problemas de compatibilidad. Esta página explica cómo hacerlo.

## Descarga

El siguiente enlace lleva al centro de descargas de Altera: [Centro de descargas de Altera](https://www.intel.com/content/www/us/en/collections/products/fpga/software/downloads.html)

![[assets/instalar-quartus/captura-27-01-26-1.png]]

En el desplegable de software elige **Quartus Prime Lite** y, en el siguiente, la **versión 17.1**, que es la que se usa en prácticas. En el último desplegable puedes elegir la versión para Windows o para Linux (no hay versión para Mac).

> [!warning] Cuidado
> Elige la edición **Lite**, que es gratuita, y no las ediciones **Standard** o **Pro**, que son de pago.

![[assets/instalar-quartus/captura-27-01-26-2.png]]

## Paquetes recomendados

El software completo incluye muchos componentes que no se usan en las asignaturas del grado, así que recomendamos descargar solo los necesarios. En la pestaña **Individual Files** pulsa **Download** en estos componentes:

- **Quartus Prime (includes Nios II EDS)**, 1,7 GB
- **ModelSim-FPGA Edition (includes Starter Edition)**, 1,1 GB
- **Cyclone IV device support**, 466,7 MB

Una vez descargados, instala haciendo doble clic sobre el fichero de Quartus (`QuartusLiteSetup-17.1.0.590-windows.exe`). Con las opciones por defecto se instalan automáticamente los tres componentes.

![[assets/instalar-quartus/captura-27-01-26-3.png]]

> [!note] Alternativa: descarga completa
> En la pestaña **Multiple Download**, el botón **Download** descarga un archivo de 5,8 GB con la versión completa y gratuita de Quartus, que se instala siguiendo las instrucciones de la misma página. Los inconvenientes son el mayor tamaño de la descarga y del software instalado, y que necesitarás un programa de descompresión (como WinRAR) para descomprimirlo antes de instalarlo.

## Actualización a la 17.1.1

Después de instalar la versión 17.1 hay que aplicar una actualización para llegar a la **17.1.1 Internal Build 593**, la misma del laboratorio. En la misma página de descarga, en la pestaña **Updates**, descarga el fichero **Quartus Prime Software v17.1 Update 1** (1,6 GB) y sigue las instrucciones de la página para instalarlo.

![[assets/instalar-quartus/captura-27-01-26-4.png]]

next > [[sdp/es/crear-qar|Ayuda: creación de QAR]]
