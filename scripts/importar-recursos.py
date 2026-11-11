#!/usr/bin/env python3
"""Copia los recursos de PoliformaT al repo con nombres ASCII.

Uso:  python3 scripts/importar-recursos.py "/ruta/a/Contenido Lessons"

La carpeta es la que se descarga de PoliformaT (GRA_12412_2026) > Recursos >
Contenido Lessons. Los nombres se comparan sin distinguir mayúsculas, la forma
Unicode de las tildes (macOS las guarda descompuestas) ni el saneado que hace
PoliformaT al comprimir (caracteres especiales sustituidos por "_"), así que
no hace falta renombrar nada. Solo copia los ficheros que aún no están en el
repo, salvo que se añada --todo.
"""
import os, re, sys, shutil, unicodedata

ASSETS = {
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 13.13.13.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-13.13.13.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.31.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.31.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.29.56.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.29.56.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.31.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.31.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.30.53.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.30.53.png",
 "Asignaciones_DE2_115/Captura de pantalla 2019-11-05 a las 15.32.44.png": "assets/asignaciones_de2_115/captura-de-pantalla-2019-11-05-a-las-15.32.44.png",
 "Control Pantalla/Diagrama Temporización Horizontal/Imagen133.png": "assets/control-pantalla/diagrama-temporizacion-horizontal/imagen133.png",
 "Control Pantalla/Diagrama Temporización Horizontal/Imagen135.png": "assets/control-pantalla/diagrama-temporizacion-horizontal/imagen135.png",
 "Control Pantalla/Diagrama Temporización Vertical/Imagen134.png": "assets/control-pantalla/diagrama-temporizacion-vertical/imagen134.png",
 "Control Pantalla/Diagrama Temporización Vertical/Imagen136.png": "assets/control-pantalla/diagrama-temporizacion-vertical/imagen136.png",
 "Control Pantalla/Estructura Pantalla Tactil LTM/Imagen043.png": "assets/control-pantalla/estructura-pantalla-tactil-ltm/imagen043.png",
 "Control Pantalla/Pantalla Tactil LTM/Imagen042.png": "assets/control-pantalla/pantalla-tactil-ltm/imagen042.png",
 "Control Pantalla/Representacion Imagenes/Imagen01.png": "assets/control-pantalla/representacion-imagenes/imagen01.png",
 "Control Pantalla/Representación con Cuentas/Imagen05.png": "assets/control-pantalla/representacion-con-cuentas/imagen05.png",
 "Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/Imagen051.png": "assets/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/imagen051.png",
 "Control Pantalla/Subtarea 3/Captura de pantalla 2020-10-06 a las 16.53.11.png": "assets/control-pantalla/subtarea-3/captura-de-pantalla-2020-10-06-a-las-16.53.11.png",
 "Control Pantalla/Subtarea 3/Imagen140.png": "assets/control-pantalla/subtarea-3/imagen140.png",
 "Control Pantalla/Subtarea 3/Imagen163.png": "assets/control-pantalla/subtarea-3/imagen163.png",
 "Control Pantalla/Subtarea 3/Imagen164d_2027.png": "assets/control-pantalla/subtarea-3/imagen164d_2027.png",
 "Control Pantalla/Subtarea 3/Imagen164e_2027.png": "assets/control-pantalla/subtarea-3/imagen164e_2027.png",
 "Control Pantalla/Subtarea 3/Imagen164f_2027.png": "assets/control-pantalla/subtarea-3/imagen164f_2027.png",
 "Control Pantalla/Subtarea 3/Imagen165.png": "assets/control-pantalla/subtarea-3/imagen165.png",
 "Control Pantalla/Subtarea 3/Imagen165bn.png": "assets/control-pantalla/subtarea-3/imagen165bn.png",
 "Control Pantalla/Subtarea 3/Imagen166.png": "assets/control-pantalla/subtarea-3/imagen166.png",
 "Control Pantalla/Subtarea 3/Imagen167.png": "assets/control-pantalla/subtarea-3/imagen167.png",
 "Control Pantalla/Subtarea 3/imagen2027bn.hex": "assets/control-pantalla/subtarea-3/imagen2027bn.hex",
 "Control Pantalla/Subtarea 3/imagen2027color.hex": "assets/control-pantalla/subtarea-3/imagen2027color.hex",
 "Control Pantalla/Subtarea 3/screenshot.png": "assets/control-pantalla/subtarea-3/screenshot.png",
 "Control Pantalla/Subtarea 4/Imagen139.png": "assets/control-pantalla/subtarea-4/imagen139.png",
 "Control Pantalla/Subtarea 4/Imagen147c.png": "assets/control-pantalla/subtarea-4/imagen147c.png",
 "Control Pantalla/Subtarea 4/Imagen148b.png": "assets/control-pantalla/subtarea-4/imagen148b.png",
 "Control Pantalla/Subtarea 4/Imagen149.png": "assets/control-pantalla/subtarea-4/imagen149.png",
 "Control Pantalla/Subtarea 4/Imagen160b.png": "assets/control-pantalla/subtarea-4/imagen160b.png",
 "Control Pantalla/Subtarea 4/char_rom-1.hex": "assets/control-pantalla/subtarea-4/char_rom-1.hex",
 "Control Pantalla/Subtarea 4/char_rom.mif": "assets/control-pantalla/subtarea-4/char_rom.mif",
 "Control Pantalla/Subtarea 5/Imagen142b.png": "assets/control-pantalla/subtarea-5/imagen142b.png",
 "Control Pantalla/Subtarea 5/Imagen173_mod.jpg": "assets/control-pantalla/subtarea-5/imagen173_mod.jpg",
 "Control Pantalla/Subtarea 5/text_rom_ejemplo.mif": "assets/control-pantalla/subtarea-5/text_rom_ejemplo.mif",
 "Control Pantalla/Subtarea 7/Imagen145_rotate.png": "assets/control-pantalla/subtarea-7/imagen145_rotate.png",
 "Control Pantalla/Subtarea 7/Imagen146b.png": "assets/control-pantalla/subtarea-7/imagen146b.png",
 "Control Pantalla/Subtarea 7/keyboard_demo.qar": "assets/control-pantalla/subtarea-7/keyboard_demo.qar",
 "Control Pantalla/Subtarea_Opcional.png": "assets/control-pantalla/subtarea_opcional.png",
 "Control Pantalla/Verificación del Diseño/p2verif_1.png": "assets/control-pantalla/verificacion-del-diseno/p2verif_1.png",
 "Control Pantalla/Verificación del Diseño/p2verif_2.png": "assets/control-pantalla/verificacion-del-diseno/p2verif_2.png",
 "Control Pantalla/Verificación del Diseño/p2verif_3.png": "assets/control-pantalla/verificacion-del-diseno/p2verif_3.png",
 "Control Pantalla/Verificación del Diseño/p2verif_4.png": "assets/control-pantalla/verificacion-del-diseno/p2verif_4.png",
 "Control Pantalla/Visualizacion en Pantalla/Imagen02.png": "assets/control-pantalla/visualizacion-en-pantalla/imagen02.png",
 "Control Pantalla/Visualizacion en una Pantalla/2000px-AdditiveColor.png": "assets/control-pantalla/visualizacion-en-una-pantalla/2000px-additivecolor.png",
 "Disenyo FSM/2024/Proy3_Ap1.png": "assets/disenyo-fsm/2024/proy3_ap1.png",
 "Disenyo FSM/2024/Proy3_Ap2.png": "assets/disenyo-fsm/2024/proy3_ap2.png",
 "Disenyo FSM/2024/Proy3_Ap3.png": "assets/disenyo-fsm/2024/proy3_ap3.png",
 "Disenyo FSM/2024/cronograma_mealy.png": "assets/disenyo-fsm/2024/cronograma_mealy.png",
 "Diseño de una Comunicación Serie/Características _Touch_/Imagen044.png": "assets/diseno-de-una-comunicacion-serie/caracteristicas-_touch_/imagen044.png",
 "Diseño de una Comunicación Serie/Comprobación/Imagen034.png": "assets/diseno-de-una-comunicacion-serie/comprobacion/imagen034.png",
 "Diseño de una Comunicación Serie/Comprobación/captura_11_may_2024.png": "assets/diseno-de-una-comunicacion-serie/comprobacion/captura_11_may_2024.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen047.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen047.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen053.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen053.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen054.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen054.png",
 "Diseño de una Comunicación Serie/Diagrama de Temporización/Imagen055.png": "assets/diseno-de-una-comunicacion-serie/diagrama-de-temporizacion/imagen055.png",
 "Diseño de una Comunicación Serie/Estructura Pantalla Táctil LTM/Imagen043.png": "assets/diseno-de-una-comunicacion-serie/estructura-pantalla-tactil-ltm/imagen043.png",
 "Diseño de una Comunicación Serie/Pantalla Táctil LTM/Imagen042.png": "assets/diseno-de-una-comunicacion-serie/pantalla-tactil-ltm/imagen042.png",
 "Diseño de una Comunicación Serie/Plantilla_Proyecto_4.qar": "assets/diseno-de-una-comunicacion-serie/plantilla_proyecto_4.qar",
 "Diseño de una Comunicación Serie/Propuesta FSM/Imagen060.png": "assets/diseno-de-una-comunicacion-serie/propuesta-fsm/imagen060.png",
 "Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_a.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_a.jpg",
 "Diseño de una Comunicación Serie/SignalTap/captura_serie_storage_b.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/captura_serie_storage_b.jpg",
 "Diseño de una Comunicación Serie/SignalTap/datos02.jpg": "assets/diseno-de-una-comunicacion-serie/signaltap/datos02.jpg",
 "Diseño de una Comunicación Serie/Subtarea 1: Interface Serie del Convertidor ADC/Imagen045.png": "assets/diseno-de-una-comunicacion-serie/subtarea-1-interface-serie-del-convertidor-adc/imagen045.png",
 "Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen046.png": "assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen046.png",
 "Diseño de una Comunicación Serie/Subtarea 2: Visualización del Punto de Contacto de la Pantalla/Imagen052.png": "assets/diseno-de-una-comunicacion-serie/subtarea-2-visualizacion-del-punto-de-contacto-de-la-pantalla/imagen052.png",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen058.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen058.png",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Imagen059.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/imagen059.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen048.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen048.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen056.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen056.png",
 "Diseño de una Comunicación Serie/Sugerencia, contador semiciclos/Imagen057.png": "assets/diseno-de-una-comunicacion-serie/sugerencia-contador-semiciclos/imagen057.png",
 "Diseño de una Comunicación Serie/Verificación del Diseño/Imagen061.png": "assets/diseno-de-una-comunicacion-serie/verificacion-del-diseno/imagen061.png",
 "Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Imagen065.png": "assets/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/imagen065.png",
 "Generar QAR/Imagen009.jpg": "assets/generar-qar/imagen009.jpg",
 "Generar QAR/Imagen011.jpg": "assets/generar-qar/imagen011.jpg",
 "Generar QAR/Imagen012.jpg": "assets/generar-qar/imagen012.jpg",
 "Instalar Quartus/captura 27-01-26 1.png": "assets/instalar-quartus/captura-27-01-26-1.png",
 "Instalar Quartus/captura 27-01-26 2.png": "assets/instalar-quartus/captura-27-01-26-2.png",
 "Instalar Quartus/captura 27-01-26 3.png": "assets/instalar-quartus/captura-27-01-26-3.png",
 "Instalar Quartus/captura 27-01-26 4.png": "assets/instalar-quartus/captura-27-01-26-4.png",
 "Secuenciales/Estrutura_Tarea/Imagen06.png": "assets/secuenciales/estrutura_tarea/imagen06.png",
 "Secuenciales/Estrutura_Tarea/estructura luces.png": "assets/secuenciales/estrutura_tarea/estructura-luces.png",
 "Secuenciales/Estrutura_Tarea/module counter.png": "assets/secuenciales/estrutura_tarea/module-counter.png",
 "Secuenciales/Estrutura_Tarea/module luces-1.png": "assets/secuenciales/estrutura_tarea/module-luces-1.png",
 "Secuenciales/Estrutura_Tarea/module shiftreg.png": "assets/secuenciales/estrutura_tarea/module-shiftreg.png",
 "Secuenciales/Verificación con Verilog HDL/Captura ST1-3 1.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-1.png",
 "Secuenciales/Verificación con Verilog HDL/Captura ST1-3 5_modificada.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-st1-3-5_modificada.png",
 "Secuenciales/Verificación con Verilog HDL/Captura de pantalla 2018-12-11 a las 17.30.43.png": "assets/secuenciales/verificacion-con-verilog-hdl/captura-de-pantalla-2018-12-11-a-las-17.30.43.png"
}
ANIMS = {
 "Control Pantalla/Funcionamiento de la Visualizacion/Pantalla_ver13.html": "quartz/static/animaciones/control-pantalla/funcionamiento-de-la-visualizacion/Pantalla_ver13.html",
 "Control Pantalla/Propuesta Estructura Diseño/Diagrama_bloques_ver20/Diagrama_bloques_ver20.html": "quartz/static/animaciones/control-pantalla/propuesta-estructura-diseno/diagrama_bloques_ver20/Diagrama_bloques_ver20.html",
 "Control Pantalla/Subtarea 1: Generación de las señales de sincronismo/IP_PLL_ver11/IP_PLL_ver11.html": "quartz/static/animaciones/control-pantalla/subtarea-1-generacion-de-las-senales-de-sincronismo/ip_pll_ver11/IP_PLL_ver11.html",
 "Control Pantalla/Subtarea 3/IP_ROM_Img_ver11/IP_ROM_Img_ver11.html": "quartz/static/animaciones/control-pantalla/subtarea-3/ip_rom_img_ver11/IP_ROM_Img_ver11.html",
 "Control Pantalla/Subtarea 4/Funcionamiento_Char_ROM_ver30/Funcionamiento_Char_ROM_ver30.html": "quartz/static/animaciones/control-pantalla/subtarea-4/funcionamiento_char_rom_ver30/Funcionamiento_Char_ROM_ver30.html",
 "Control Pantalla/Subtarea 4/MIF_File/MIF_File.html": "quartz/static/animaciones/control-pantalla/subtarea-4/mif_file/MIF_File.html",
 "Diseño de una Comunicación Serie/Propuesta estructura diseño/Diagrama_bloques_2024/Diagrama_bloques_bi_sin_half.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/propuesta-estructura-diseno/diagrama_bloques_2024/Diagrama_bloques_bi_sin_half.html",
 "Diseño de una Comunicación Serie/Sugerencia, concatenación/Temporizacion_Tactil01.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/sugerencia-concatenacion/Temporizacion_Tactil01.html",
 "Diseño de una Comunicación Serie/Verificación del Diseño/Diagrama_verificacion_bi/Diagrama_verificacion_bi.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-del-diseno/diagrama_verificacion_bi/Diagrama_verificacion_bi.html",
 "Diseño de una Comunicación Serie/Verificación y Mejora del Diseño/Diagrama_bloques_2024/Diagrama_bloques_mejora_bi_sin_half.html": "quartz/static/animaciones/diseno-de-una-comunicacion-serie/verificacion-y-mejora-del-diseno/diagrama_bloques_2024/Diagrama_bloques_mejora_bi_sin_half.html"
}
VIDEOS = {
 "Videos/Direccionamiento XY.mp4": "quartz/static/videos/direccionamiento-xy.mp4",
 "Videos/Memory Content Editor 1.mp4": "quartz/static/videos/memory-content-editor-1.mp4",
 "Videos/Memory Content Editor 2.mp4": "quartz/static/videos/memory-content-editor-2.mp4",
 "Videos/SignalTap 1.mp4": "quartz/static/videos/signaltap-1.mp4",
 "Videos/SignalTap 2.mp4": "quartz/static/videos/signaltap-2.mp4"
}

def key(p):
    p = unicodedata.normalize("NFC", p).replace("\\", "/").lower()
    return p

def key_saneado(p):
    p = unicodedata.normalize("NFC", p).replace("\\", "/")
    p = p.replace("+", " ")
    return "/".join(re.sub(r"[^A-Za-z0-9._-]", "_", c) for c in p.split("/")).lower()

def main(src, todo=False):
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index = {}
    for root, dirs, files in os.walk(src):
        for f in files + dirs:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, src)
            index.setdefault(key(rel), full)
            index.setdefault(key_saneado(rel), full)
    def find(orig):
        return index.get(key(orig)) or index.get(key_saneado(orig))
    missing, copied = [], 0
    for table, prefix in ((ASSETS, "content"), (ANIMS, ""), (VIDEOS, "")):
        for orig, dst in table.items():
            out = os.path.join(repo, prefix, dst)
            if os.path.exists(out) and not todo:
                continue
            f = find(orig)
            if not f:
                missing.append(orig); continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(f, out); copied += 1
            if table is ANIMS:
                # carpeta de recursos de Tumult Hype (Nombre.hyperesources)
                res = find(os.path.splitext(orig)[0] + ".hyperesources")
                if res and os.path.isdir(res):
                    shutil.copytree(res, os.path.splitext(out)[0] + ".hyperesources", dirs_exist_ok=True)
                else:
                    missing.append(os.path.splitext(orig)[0] + ".hyperesources/")
    print(f"Copiados {copied} ficheros.")
    big = [v for v in VIDEOS.values() if os.path.exists(os.path.join(repo, v)) and os.path.getsize(os.path.join(repo, v)) > 95e6]
    for b in big:
        print("AVISO: supera el límite de 100 MB de GitHub:", b)
    if missing:
        print("No encontrados:")
        for m in missing: print("  -", m)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--todo"]
    if len(args) != 1: sys.exit(__doc__)
    main(args[0], "--todo" in sys.argv)
