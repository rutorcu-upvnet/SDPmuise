---
title: Revisión de las prácticas de SDP (PoliformaT → Quartz)
draft: true
---

Informe de la migración de las Tareas 1–4 y las ayudas de Quartus/QAR de PoliformaT (DOC_34625_2026) a Markdown para Quartz. Generado el 5 de noviembre de 2026. Está marcado `draft: true` para que no se publique.

## Estructura generada

- `content/sdp/es/` y `content/sdp/en/`: una página por tarea (las subpáginas de PoliformaT pasan a ser secciones), más `index.md`, instalación de Quartus y creación de QAR.
- Nombres de fichero en ASCII, minúsculas y sin espacios (`tarea1-sistemas-secuenciales.md`, `task1-sequential-systems.md`...). El título visible está en el *frontmatter*.
- Enlaces internos como wikilinks con ruta completa (`[[sdp/es/tarea2-control-pantalla|Tarea 2 ...]]`).
- Imágenes en `content/assets/<carpeta-ascii>/<fichero-ascii>`; animaciones en `quartz/static/animaciones/<carpeta-ascii>/<Fichero>.html`, incrustadas con ruta relativa (`../../static/...`) para que funcionen bajo `/SDPmuise/`.
- La lista de recursos que faltan y el script para copiarlos están en `RECURSOS-PENDIENTES.md` y `scripts/importar-recursos.py`, en la raíz del repo.

## Pendiente antes de publicar

1. **Copiar recursos**: 127 imágenes/ficheros y 25 animaciones (ver `RECURSOS-PENDIENTES.md`).
2. **Vídeos no exportables**: PoliformaT tiene 3 vídeos embebidos sin fichero accesible (uso del *In-System Memory Content Editor* en la Tarea 2, y dos de SignalTap en la Tarea 4). Están marcados con un comentario `<!-- PoliformaT: vídeo ... -->`; hay que subirlos o enlazarlos.
3. **Tests previos** (Tareas 1 y 4): el texto remite a un test de PoliformaT que no se puede enlazar desde una web pública. He dejado un aviso `[!warning] Test previo`.
4. **Enlaces de Intel** (Instalación de Quartus): los dos enlaces originales son elementos URL de PoliformaT que no pude resolver. He puesto el Intel FPGA Download Center; conviene comprobar el enlace directo a Quartus Lite 17.1.
5. **Dos «Tarea 3» visibles**: «Juego de luces mejorado con FSMs» (versión 2024) y «Diseño de Máquinas de Estados Finitos» (motor paso a paso). Están las dos; decide cuál se publica.
6. **Screen Simulator**: se mantiene el enlace corto `https://is.gd/JtLbap`; conviene sustituirlo por la URL final.

## Correcciones técnicas

| Página | Original | Corregido / motivo |
| --- | --- | --- |
| T1 Estructura | «estructurada en cuatro subtareas» | Son **tres** subtareas. |
| T1 Subtarea 1 | `CLogB2` «con redondeo al entero más próximo» | **Redondeo hacia arriba** (techo). Con redondeo al más próximo, p. ej. N = 20 daría 4 bits y no cabe. |
| T1 Testbench | Código formateado en negrita párrafo a párrafo | Reescrito como bloque ```` ```verilog ```` (mismo código). |
| T1 Testbench | «alrededor de 20 ciclos» | Se para unos **24 ciclos** después de habilitar (`#(T*24)`), y se ven 0→19→0. |
| T1/T4 Menú | «Tools > Run Simulation Tools > Run RTL Simulation» | `Tools > Run Simulation Tool > RTL Simulation` (nombre real del menú en Quartus 17.1). |
| T2 | «2n» posibles valores / «2n por Y» | **2ⁿ** (se había perdido el superíndice). |
| T2 Direccionamiento X-Y | «potencia de 2 mayor que X» | **mayor o igual** (coincide con la versión inglesa). |
| T2 Verificación / Subtarea 2 | «cercano a los 23 ms» / «casi 23 ms» | 1056 × 525 × 40 ns = **22,18 ms**; cambiado a «unos 22 ms». |
| T2 ROM | «memorias... sincronías», «seña de reloj» | «síncronas», «señal de reloj». |
| T3 (motor) Subtarea 2 | «jugando con los diferentes botones y computadores» | «pulsadores e interruptores». |
| T4 Objetivos (EN) | «characteristics and operation modes of a **display screen**» | **touchscreen** (la ES habla de pantalla táctil). |
| T1 Verificación en placa (EN) | «the address (**Direction**)» | **direction**. |

## Erratas y redacción (ES)

modernización → modelado · «avanzando en el aprendizaje y sus de la jerarquía» → «avanzando en el uso de la jerarquía» · «Como objetivos fundamental» → «El objetivo fundamental» · «En está practica» → «En esta práctica» · «consideré» → «considere» · «Testbech» → «testbench» · «hay emplear» → «hay que emplear» · «una utilizada que permite» → «una utilidad que permite» · FGPA → FPGA · «debanados» → «devanados» · «CLa Tabla» → «La tabla» · «leguaje» → «lenguaje» · «tacando» → «tocando» · «subtrarea» → «subtarea» · «trascripción» → «transcripción» · tildes en «máquina», «módulo», «único», etc. Además se ha aligerado la redacción (frases largas partidas, listas en vez de párrafos enumerativos).

## Versión inglesa

La versión EN de PoliformaT tenía muchas frases de traducción automática. Se ha reescrito manteniendo el contenido: *meter/accounts* → *counter/counts*, *flanks* → *edges*, *end of account* → *terminal count*, *module* → *modulus*, *a used tool* → *a utility*, *it will be called Quartus* → *Quartus will open*, *Testbech*, *lighing*, *memoria*, *an inverted is used* → *an inverter*, etc. Se usa ortografía británica de forma consistente.

## Añadidos (no estaban en PoliformaT)

Todos van en *callouts* para que sean fáciles de localizar o quitar:

- T1: pregunta «¿Has evaluado todos los casos posibles?» con lista de casos; pregunta plegada con el valor de `fin_cuenta` para 0,25 s (12 500 000, 24 bits). Avisos `[!warning]` para la entrega de capturas.
- T2: pregunta plegada con la duración del *frame* (22,18 ms); pregunta plegada con el reparto de los 13 bits de la ROM de caracteres; *tip* sobre RGB565 (**suposición**: comprobar el formato de `imagen_rgb16_xy.hex`); *tip* sobre marcar *Allow In-System Memory Content Editor* al crear la ROM.
- T3 (luces): pregunta plegada sobre por qué `counter_variable` usa `>=`; *tip* sobre sobrescribir el parámetro del divisor en el testbench.
- T3 (motor): tabla de elementos del emulador (antes lista).
- T4: *tip* sobre *Storage Qualifier* de SignalTap.

## Eliminado

- T3 (motor): «Entre sus principales aplicaciones destacan como motor de frecuencia variable, motor de corriente continua sin escobillas, servomotores...». Es técnicamente confuso (un paso a paso no es una aplicación de un motor brushless). Si quieres conservarlo, conviene reformularlo.

## Dudas para el profesor

- T1 Subtarea 1: no se especifica cuándo se activa **TC** contando hacia abajo (¿en 0?). Convendría indicarlo.
- T1 Subtarea 2: la especificación del registro no dice el sentido de desplazamiento.
- T3 (luces) Apartado 1: se pide una máquina **Medvedev** (salidas = bits de estado) con 14 estados y 8 LEDs. Si la secuencia repite patrones de LEDs en la ida y la vuelta, no puede ser Medvedev pura (dos estados con la misma salida serían el mismo estado). Revisar según `Imagen06.png`.
- T2 Subtarea 1: la versión EN dice que RST_n es asíncrono y la ES no lo especifica.
- T4: «el parámetro del módulo del contador deberá ajustarse... en función de la velocidad de transmisión»: el retardo de 0,5 s no depende de la velocidad de transmisión; quizá se refiere a ajustarlo de forma empírica.
