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
| `hero-4.jpg` | dominadas, blanco y negro, con VOLCANO pintado en la pared |
| `entrenamientos.jpg` | entrenando en la sala |
| `profes.jpg` | la remera de Volcano (camuflado + sol argentino) |
| `gym.jpg` | las cintas frente al ventanal, con VOLCANO en el vidrio |
| `historias.jpg` | el cartel de "Matecitos ❤" |
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

## Versión online

Publicada como Artifact en:
**https://claude.ai/code/artifact/5db6decc-b9fb-4610-b69e-8c9c8c02c3b5**

Nace **privada**: solo la ve Guada hasta que le dé a *Share* en la barra de arriba.

Para actualizarla después de tocar el sitio:
1. `python3 site/publicar.py` — regenera `artifact.html` desde `index.html`
   (Artifact envuelve el archivo en su propio `<head>`/`<body>`, así que recibe solo el contenido)
2. Republicar ese archivo a la **misma URL**, pasándola como `url` si es desde otra conversación.

`artifact.html` es generado: no editarlo a mano, se pisa. El que se edita es `index.html`.
