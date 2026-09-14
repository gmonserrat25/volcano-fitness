# Volcano Fitness — sitio web

Maquetación calcada de **go180.nl**, con la identidad de Volcano.

## Cómo verlo

```
cd ~/Proyectos/volcano-fitness/site
python3 -m http.server 8899
```
Después abrir http://localhost:8899

## Qué se copió de go180.nl

| Pieza | Original | Acá |
|---|---|---|
| Preloader | logo centrado + cortina diagonal | igual |
| Header | logo izq. + hamburguesa der., fijo, 74px | igual |
| Menú | overlay a pantalla completa, links grandes a la izquierda, submenú desplegable | igual |
| Dots | columna vertical a la derecha, el activo con anillo | igual |
| Paneles | 6 pantallas completas: foto de fondo, título gigante, bajada, botón pill | igual |
| Movimiento | el contenido sale a media velocidad del panel (parallax medido sobre el original) | igual |
| Reseñas | barra de Google debajo de los paneles | igual |
| Footer | newsletter + 4 columnas + legales | igual |

## Qué cambió (identidad Volcano)

- Fondo `#0B1220` en lugar del petróleo `#0D1E25` del original: mismo rol, girado al azul del logo.
- Acento **azul eléctrico `#1E6BFF`**, el del volcán del logo. Aparece en el dot activo, el hover
  de los links y los botones secundarios.
- Tipografía **Figtree** 600/700/800 (el original usa Gilroy, que es de pago; Figtree es la más
  cercana y es gratis).
- Logo: wordmark `VOLCANO` con la primera O convertida en cráter, igual que `GO180` tiene un
  glifo en su O.

## Imágenes — fotos reales del Instagram

Las 9 fotos salen del Instagram público **@volcano_fitnesslafalda** (las 12 publicaciones más
recientes, que son las del gimnasio nuevo). Se bajaron a 1080px por el endpoint
`instagram.com/p/<código>/media/?size=l` y se redimensionaron a 1600px de alto.

| Archivo | Qué muestra |
|---|---|
| `hero-1.jpg` | rack negro con el círculo de luz LED cálida detrás |
| `hero-2.jpg` | rack con el arco LED sobre la pared texturada |
| `hero-3.jpg` | el espejo con el círculo LED de fondo |
| `hero-3.jpg` | la sala con el logo VOLCANO (frame de un reel) |
| `hero-4.jpg` | dominadas, blanco y negro, con VOLCANO pintado en la pared |
| `entrenamientos.jpg` | entrenando en la máquina (frame de un reel) |
| `profes.jpg` | la remera de Volcano (camuflado + sol argentino) |
| `gym.jpg` | las cintas frente al ventanal, con VOLCANO en el vidrio |
| `historias.jpg` | la sala con el logo VOLCANO en la pared (frame de un reel) |
| `contacto.jpg` | el grupo con las remeras, bajo el arco LED |

**Ojo con el encuadre.** Las fotos de Instagram son verticales (3:4 y 9:16) y los paneles son
horizontales a pantalla completa, así que se recortan bastante. Cada una tiene su
`background-position` ajustado a mano en el HTML (`center 18%`, `center 32%`…). Si se cambia
una foto hay que revisar ese valor. Fotos horizontales se verían bastante mejor.

Quedaron afuera dos de las 12: una en negro (video) y otra con texto quemado encima.

## Logo

`img/logo.png` es el logo real, recortado de la foto de perfil de Instagram (150x150, que es
la máxima resolución que Instagram sirve sin login). El fondo negro se convirtió en
transparencia real y se escaló x4 a 520x396.

Por eso el logo **no da para usarse mucho más grande** que en el footer (92px de alto).
Si aparece el archivo original del logo, reemplazar `img/logo.png` y listo.

El azul de la marca se muestreó del propio logo: `#154DA0` (`--brand`), y el acento de
interfaz `#347BE4` (`--accent`) es ese mismo tono aclarado para que se lea sobre el fondo oscuro.

## Falta completar

Buscar `[COMPLETAR` en `index.html`:
- dirección, horarios, teléfono, email
- número de WhatsApp
- puntaje y cantidad de reseñas de Google, y el link para calificar
- el titular del hero ("Despertá el volcán") es una propuesta, no está confirmado

## La sección de la app

Va en `index.html`, entre el último panel y las reseñas (`id="app"`), y también está en el
menú. Muestra de qué sirve la app y tiene un teléfono dibujado con CSS que repite la misma
rutina de `rutina.html`, para que lo que se ve prometido sea lo que hay.

**Faltan los dos links de las tiendas**: buscá `[COMPLETAR link App Store]` y
`[COMPLETAR link Google Play]` en `index.html`. Si el gimnasio no tiene app propia sino que
usa una de terceros, ahí van los links de esa.

Los botones son propios, no los badges oficiales de Apple y Google. Si hace falta usar los
oficiales hay que bajarlos de sus sitios de marca y respetar sus reglas de uso.

## Frames sacados de los reels

Instagram sin login sólo muestra 12 publicaciones, y varias no servían (una en negro, otra
con texto quemado, selfies). Para conseguir más fotos del lugar se sacaron **frames de los
reels**: no hay ffmpeg en esta máquina y los videos de Instagram van por `blob:` (no se
pueden descargar), así que se capturaron desde el `<video>` de la página, dibujándolo en un
`<canvas>` y mandando los JPEG a un servidor local.

Salen a 810x1440, un poco más blandos que una foto, pero son del gimnasio y sirven.
Si aparecen fotos de verdad, reemplazarlas.

## Legibilidad de los paneles

Los títulos sobre las fotos se perdían, sobre todo en las claras. Tres cosas lo arreglan,
todas en `.panel__scrim` y `.panel__title` / `.panel__lead`:

1. Un **halo radial** en el scrim, centrado donde va el texto, que lo despega de la foto sin
   ensuciar toda la imagen.
2. **Doble sombra** en el texto: una corta y cerrada que le da borde, y una amplia y difusa
   que le da fondo.
3. El **parallax** del contenido bajó de 46% a 24% de recorrido, así el texto no se va tanto
   del centro mientras scrolleás.

Si se cambia una foto por una muy clara, revisá que el título siga leyéndose.

## Páginas internas

Igual que en go180, las secciones del menú son páginas aparte:

- **`rutina.html`** — "Tu rutina". Una rutina de ejemplo (tren inferior) con series,
  repeticiones, descanso y los kilos de la última sesión. Los ejercicios son inventados
  para mostrar cómo se ve; dice explícitamente que es un ejemplo.
- **`profes.html`** — "Los profes". Ludmi Porrino con su foto, y dos lugares más con
  solo la silueta, sin datos inventados, para cuando se sumen los otros profes.

Las dos **se generan** con `python3 paginas.py`, que copia el preloader, el header, el
menú y el footer desde `index.html` para que no se desincronicen, y les reescribe los
anclas (`#gym` pasa a `index.html#gym`). Si cambiás el menú en `index.html`, corré ese
script para que las internas se actualicen. El contenido propio de cada página está
adentro de `paginas.py`, en el diccionario `CONTENIDO`.

La foto `img/profe-ludmi.jpg` es un recorte de retrato del posteo de @ludmiporrino.
Esa foto se sacó del slideshow del hero, que ahora rota entre 3.

## Cómo levantarlo

```
cd ~/Proyectos/volcano-fitness/site
python3 servidor.py        # http://localhost:8899
```

Usá `servidor.py`, no `python3 -m http.server`: manda `Cache-Control: no-store`, así el
navegador no te muestra versiones viejas del HTML o del CSS después de editarlos. Si igual
ves algo desactualizado, un **Cmd+Shift+R** lo destraba.

## Para verlo desde el celular o pasárselo a alguien

El Artifact que había se borró. Para tener una URL que se abra desde cualquier lado:

```
cd ~/Proyectos/volcano-fitness/site
python3 servidor.py &
~/bin/cloudflared tunnel --url http://localhost:8899
```

Imprime una URL `*.trycloudflare.com` que funciona mientras la Mac esté prendida y el
comando corriendo. El link cambia cada vez que se levanta.

Si hace falta una dirección fija que ande siempre, la opción es GitHub Pages
(la cuenta `gmonserrat25` ya está configurada), pero eso deja el sitio público.
