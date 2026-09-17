# LESSONS.md — Capital PDF Service

> Vacío por ahora. Se documentan aquí los errores y sus reglas absolutas a medida que aparezcan.

## Sin las fuentes reales instaladas, la paginación cambia entre máquinas

- **Error:** El mismo HTML generaba 16 páginas en local y 17 en Render. La página 3 mostraba una sola fila de una tabla (el índice) que se había "caído" sola a una página nueva.
- **Causa raíz:** El Dockerfile nunca instalaba Fraunces/Inter/IBM Plex Mono, solo `fonts-liberation`. WeasyPrint entonces usa la fuente de reemplazo que encuentre disponible en el sistema — y esa fuente de reemplazo NO es la misma en mi compu (macOS, con su propio set de fuentes) que en el contenedor de Render (Debian mínimo). Métricas de fuente distintas = texto ligeramente más ancho/alto = una tabla que ya estaba al límite se desborda a una página extra.
- **Fix:** Descargar los .ttf reales de Google Fonts y copiarlos a `/usr/share/fonts/truetype/brand/` en el Dockerfile, más `fc-cache -f`. Con la fuente real y exacta en todos los entornos, la paginación queda determinística.
- **REGLA:** SIEMPRE instalar como fuentes de sistema (no solo declarar en CSS) cualquier fuente que el diseño use, en cualquier entorno donde WeasyPrint (o cualquier motor de render a PDF) vaya a correr. Nunca confiar en que "la fuente de reemplazo se va a ver parecida" — las métricas distintas rompen la paginación exacta, no solo la estética.
- **REGLA:** Si un PDF generado por WeasyPrint da un número de páginas distinto entre dos entornos con el mismo HTML de entrada, sospechar primero de fuentes faltantes/distintas antes que de una diferencia real de contenido. Confirmarlo generando el mismo HTML en ambos entornos y comparando encabezado por página (no solo el conteo total).

## `HTML(filename=...)` sin `<meta charset>` puede producir mojibake — usar `HTML(string=...)`

- **Error:** Al probar generación de PDF leyendo un archivo temporal en disco con `HTML(filename=...)`, aparecieron caracteres corruptos (™ y · convertidos en "â„¢" y "Â·"), pese a que el archivo era UTF-8 válido.
- **Causa raíz:** El archivo de prueba no tenía `<meta charset="utf-8">` (se había extraído solo el `<style>` + cuerpo, sin la etiqueta de charset del original). Sin esa pista, WeasyPrint tiene que adivinar la codificación al leer bytes crudos de un archivo, y adivinó mal.
- **Fix:** No es un bug real de producción — el flujo real (Flask recibe JSON, ya viene como string Python decodificado correctamente) nunca pasa por esta ambigüedad. Fue un artefacto de cómo yo probaba manualmente.
- **REGLA:** Para probar el servicio manualmente fuera de la app, usar `HTML(string=texto_ya_decodificado)`, nunca `HTML(filename=...)` sobre un fragmento de HTML sin `<meta charset>` propio — para no perseguir un bug que no existe en producción.
