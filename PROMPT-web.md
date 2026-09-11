# Prompt — Sitio web Volcano Fitness (La Falda, Córdoba)

> Pegar en Claude, Lovable, Cursor, Bolt o v0.
> Reemplazar antes de usar todo lo que está entre [CORCHETES].

---

Construí una landing page de una sola página para **Volcano Fitness**, un gimnasio de
La Falda, Córdoba, Argentina. Todo el contenido va en español rioplatense (voseo).

## Tono y referencia

Quiero el nivel de sofisticación editorial de kinective.com: mucho aire, tipografía
grande como protagonista, la fotografía mandando, cero saturación de elementos.
Pero la paleta es oscura, no crema: el gimnasio es de paredes negras con luces
cálidas, y el sitio tiene que sentirse igual que entrar al local.

La marca es cercana y divertida, no intimidante. Su propia bio dice:
"Música fuerte, buenas vibras y entrenos que te hacen sudar pero también reír."
Ese es el tono: enérgico y amistoso, nunca el gimnasio de fisicoculturismo agresivo.

## Paleta

- Fondo base: negro carbón (#0B0B0D), casi todo el sitio
- Fondo secundario: gris piedra texturado (#1A1A1D) para alternar secciones
- Texto: blanco cálido (#F5F3EF), nunca blanco puro
- Acento principal: azul eléctrico del logo (#2E7FE8 aprox), muy dosificado — botones y detalles
- Acento secundario: dorado tenue (#C9A227) para hovers y números, tomado del sol
  argentino de las remeras del equipo
- Luz: usar glows suaves y degradés radiales muy sutiles detrás de los bloques,
  imitando las luces LED cálidas del gimnasio. Nunca degradés estridentes.

## Tipografía

- Títulos: una serif de alto contraste, elegante y grande (tipo Canela, Editorial New
  o, si no hay, Playfair Display). Tamaños generosos, 1 a 3 palabras por línea.
- Cuerpo y navegación: sans geométrica en mayúsculas con tracking amplio para
  botones y menú (tipo Inter o Neue Haas).
- El contraste serif/sans es clave: es lo que hace que se vea caro.

## Estructura de secciones, en orden

1. **Header fijo** — logo Volcano a la izquierda, menú al centro, botón "PROBÁ GRATIS"
   a la derecha. Fondo translúcido con blur al scrollear.

2. **Hero a pantalla partida.** Izquierda: fondo negro con un glow cálido detrás y el
   título en serif enorme cortado en dos líneas: "Entrená fuerte. / Reíte más."
   Debajo, una bajada corta y dos botones. Derecha: foto a sangre del interior del
   gimnasio. Que la división no sea 50/50 exacta, sino 45/55, es más elegante.

3. **Manifiesto** — un solo párrafo grande, centrado, mucho aire arriba y abajo.
   Quiénes son antes de qué venden. Sobre fondo negro liso.

4. **El espacio** — galería de 4 a 6 fotos del gimnasio en grilla asimétrica (unas
   altas, otras anchas). Las fotos reales tienen paredes negras, nichos arqueados
   iluminados y máquinas nuevas: que se luzcan grandes, sin bordes redondeados
   exagerados. Leve parallax al scrollear.

5. **Actividades** — pestañas o acordeón horizontal con: Musculación, Funcional,
   Caminatas al aire libre, [COMPLETAR CON LAS REALES]. Cada una con una foto y
   dos líneas de texto. Al cambiar de pestaña, la foto hace crossfade.

6. **Horarios** — tabla limpia de días y franjas horarias. Legible en celular sin
   zoom: en pantalla chica se convierte en una lista por día, nunca en scroll
   horizontal. [COMPLETAR HORARIOS REALES]

7. **Planes** — 3 tarjetas con el precio VISIBLE. (A diferencia de Kinective, que los
   esconde: en un pueblo esconder el precio genera desconfianza.) La del medio
   destacada con un borde azul. [COMPLETAR PRECIOS]

8. **Equipo** — fotos de los profes con nombre y una línea de especialidad.
   En un pueblo la gente elige por quién te atiende. [COMPLETAR NOMBRES]

9. **Testimonios** — 3 o 4 de alumnos reales, con foto y nombre de pila.

10. **Ubicación y contacto** — mapa embebido, dirección, botón grande de WhatsApp,
    links a Instagram (@volcano_fitnesslafalda) y TikTok (@volcano.fitness).
    [COMPLETAR DIRECCIÓN Y TELÉFONO]

11. **Footer** — logo, menú corto, redes, horarios resumidos.

## Elemento persistente

Una **barra fija abajo de todo**, sobre fondo azul, que acompaña todo el scroll:
"PROBÁ UNA CLASE GRATIS" y que abre WhatsApp directo. Se puede cerrar con una X.
Este es el CTA de verdad del sitio.

## Animaciones

Sobrias y con intención, no decorativas:
- Los títulos entran con un fade + subida de 20px, escalonado por línea
- Las fotos hacen un zoom out muy leve al entrar en viewport
- Parallax sutil en la galería
- Hover en botones: el fondo se llena desde abajo
- Todo debe respetar `prefers-reduced-motion`
- NADA que tape el contenido ni que obligue a esperar para leer

## Requisitos técnicos

- HTML, CSS y JavaScript vanilla en un solo archivo, sin frameworks
- Mobile-first de verdad: la mayoría va a entrar desde el celular, desde Instagram
- Sin scroll horizontal en ningún ancho, mínimo 16px de margen lateral siempre
- Imágenes con lazy loading y `alt` descriptivo en español
- Buen contraste: texto claro sobre fondo oscuro, mínimo 4.5:1
- Navegación por teclado funcional y foco visible
- Usar placeholders grises con la medida indicada donde irían las fotos reales

## Qué NO hacer

- Nada de emojis en la interfaz
- Nada de degradés violeta/fucsia tipo app de fitness
- Nada de stock photos de modelos musculosos en un gimnasio genérico
- No esconder los precios
- No pedir registro para ver información básica
