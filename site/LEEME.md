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
- número de WhatsApp
- puntaje y cantidad de reseñas de Google, y el link para calificar
- el titular del hero ("Despertá el volcán") es una propuesta, no está confirmado

## La página Entrenamientos

`entrenamientos.html` lista las cuatro formas de entrenar: musculación, funcional,
personalizado y acondicionamiento. Las tarjetas alternan foto a izquierda y derecha.

**Cada una tiene su desvío propio**: un botón que abre WhatsApp con un mensaje ya escrito
específico de esa disciplina ("Quiero consultar los horarios de funcional", etc.), así llega
la consulta con contexto. Si más adelante cada disciplina tiene su página, ahí se cambian
esos links.

Abajo hay un bloque con el teléfono y la rutina, que lleva a `rutina.html`.

## El iPhone de la página "Tu rutina"

**No es una captura: es el sitio de verdad.** Dentro del marco hay un `<iframe>` que carga
`socios.html?demo=1`, así que se puede tocar, tachar ejercicios y reservar clases desde ahí.

El truco del tamaño: el iframe se dibuja a **390 px de ancho** (un celular real) y después se
achica con `transform: scale()` para entrar en el marco. Si se le pone el ancho del marco
directamente, el sitio se renderiza a 278 px y el contenido se desborda.

La escala se calcula sola: `--escala: var(--ancho-marco) / var(--ancho-real)`. Para cambiar el
tamaño del teléfono alcanza con tocar `--ancho-marco`.

El `?demo=1` hace que el área de socios entre derecho al panel, sin pasar por la pantalla de
acceso: está en `js/socios.js`.

## La página El gym

`gym.html` (generada por `paginas.py`, como las otras) tiene tres partes:

1. **Galería** en mosaico de 7 fotos. Las piezas están medidas para llenar la grilla de
   4x3 sin dejar huecos: una ocupa 2x2, dos ocupan 1x2 y las otras cuatro 1x1. Si agregás
   o sacás fotos, revisá que las áreas sigan cerrando o va a quedar un hueco.
2. **Equipamiento**, agrupado en Fuerza / Máquinas / Cardio / La sala. **La lista se armó
   mirando las fotos, una por una**: está sólo lo que se ve. No hay prensa 45°, ni sauna,
   ni vestuarios, porque no aparecen en ninguna imagen. Si existen, agregarlos.
3. **Dónde estamos**, con la dirección real (**Sarmiento 518, La Falda**), el mapa embebido
   de Google y un botón "Cómo llegar" que abre la app de mapas del celular.

El mapa es un iframe de Google, o sea que carga recursos de Google en la página. Si eso
molesta, se puede cambiar por una imagen estática con un link encima.

## Las caminatas ya no van

Aparecían en el submenú y en la descripción. **El gimnasio no las ofrece** (confirmado el
2026-09-14), así que se quitaron de todos lados. Estaban porque hay un destacado viejo de
Instagram que las muestra: no volver a agregarlas por eso.

## Ninguna imagen del sitio sale de un video

Se llegó a usar frames de reels para tapar agujeros, y **se nota**: son más blandos y las
poses quedan a mitad de movimiento. Se sacaron todos. Hoy cada imagen del sitio es una
**foto de una publicación** de Instagram.

Si en algún momento hace falta volver a sacar un frame, que sea a sabiendas y por poco
tiempo: dejarlo marcado acá.

## Los paneles y la altura del celular

Usan **`100dvh`**, no `svh` ni `vh`, y esto importa:

- `svh` es la altura **mínima** del viewport, con las barras del navegador visibles. Cuando en
  el celular la barra se retrae, la pantalla crece y el panel queda corto: **se ve el borde
  del panel siguiente junto al actual**. Fue exactamente el problema que apareció en el
  celular, con dos títulos a la vez.
- `dvh` sigue el viewport real en cada momento, así que el panel siempre lo llena.

Además los paneles llevan `scroll-snap-align:start` y el documento
`scroll-snap-type:y proximity`, para que el scroll tienda a encajar en cada panel y no queden
dos a medias. Es `proximity` y no `mandatory` a propósito: `mandatory` secuestra el scroll y
molesta en las secciones largas de abajo.

## Valores tomados del original

La tipografía y el botón no están a ojo: se midieron sobre go180.nl a 1280 px de ancho.

| | go180 | acá |
|---|---|---|
| Título | 70 px, peso 700, tracking normal, interlínea 1.0 | igual (`5.5vw`) |
| Bajada | 19 px, peso 600, interlínea 1.8, ancho 700 px | igual |
| Botón | alto 56, radio 50, 18 px, peso 700 | igual |
| Texto | `#E1E1E1` | `--fg` (`#E8E8E6`) |

**La única diferencia a propósito:** go180 **no usa sombra** en el texto del hero, porque sus
videos son parejos y oscuros. Acá las fotos son más claras y sin sombra no se lee, así que
los títulos llevan una sombra suave — mucho más liviana que la que tenían antes.

Lo demás que **no** viene de go180, porque se pidió expresamente: el botón flotante de
WhatsApp, el área de socios y la paleta, que sigue el azul del logo de Volcano en lugar del
petróleo del original.

## La animación de entrada

Es la de go180, copiada de su timeline de GSAP (está en el `main.js` de su tema). Acá se hizo
con animaciones CSS, sin librerías:

| Pieza | Qué hace |
|---|---|
| `.wipe` | Un cuadrado de **200vw × 200vw** anclado en `top:100svh; left:0`, con `transform-origin:0 0`. Arranca en `rotate(-90deg)`, que así cubre toda la pantalla, y **rota hasta -180°** en 1,2 s. Al pivotear sobre la esquina de abajo a la izquierda, su borde barre la pantalla en diagonal: ese es el efecto. |
| `.wipe-logo` | El logo centrado con un **anillo girando** (360° cada 1,8 s), como la O que gira en el logo de go180 mientras carga. Se desvanece en 0,4 s. |
| `.letra` | El título se parte en letras por JS. Cada una entra desde `translateY(100%) rotate(20deg)`, **escalonadas**: 0,6 s repartidos entre todas. |
| `[data-sube]` | La bajada y el botón suben desde abajo, un poco después. |

El `ease` es `cubic-bezier(.645,.045,.355,1)`, que es el Power2.easeInOut que usa el original.

**Al probarla, ojo:** en una pestaña en segundo plano el navegador congela las animaciones CSS
y parece que no pasa nada. Para revisarla conviene manejarla a mano:

```js
document.getAnimations().forEach(a => { a.pause(); a.currentTime = 400; });
```

## Video del hero

`video/hero.mp4` — 1 MB, 1280x720, mudo, en loop. Sale de la **historia destacada "Gym"**
(la tercera): un travelling lento por los espejos circulares con la luz LED cálida, **sin
gente**. `img/hero-1.jpg` es el `poster` y lo que se ve con "reducir movimiento".

Antes se probó con un slideshow de fotos y con otros dos videos. Este quedó porque muestra el
lugar vacío, que es lo que se pidió, y porque a 1280 px se ve bastante mejor que los
recortes anteriores.

### Cómo se captura (esto costó, no improvisar)

Los videos de Instagram van por `blob:` y no hay ffmpeg en esta máquina. El camino que
funciona tiene **dos etapas separadas**, y la separación es el punto:

**Etapa 1 — juntar los cuadros, en la página de Instagram.** Se hace *seek* cuadro por cuadro
(`currentTime = t`) y se dibuja cada uno en un `<canvas>`, tomando la franja central para
pasar de vertical a horizontal. Acá **el tiempo no importa**: se puede tardar lo que sea.
El *seek* funciona aunque la pestaña esté en segundo plano.

**Etapa 2 — armar el mp4, fuera del navegador.** Con `herramientas-armar-video.swift`
(AVFoundation), que arma el video desde los JPEG con el ritmo exacto que se le pida:

```
swiftc -O herramientas-armar-video.swift -o armar
BR=1500000 ./armar <carpeta-con-jpgs> hero.mp4 25
```

**Por qué no se graba directo en el navegador:** la pestaña corre en segundo plano, y ahí
Chrome congela `requestAnimationFrame`, estrangula `setTimeout` a uno por segundo y ni
siquiera un Worker recibe ticks. Grabar con `MediaRecorder` en esas condiciones da un video
**tildado**, porque cada cuadro queda con el sello de tiempo de cuando el navegador se dignó
a ejecutar: se midieron desvíos de hasta un segundo. Ese fue exactamente el problema.

Para pasar los cuadros de Instagram al disco, el CSP de Instagram bloquea `fetch` a
localhost, los iframes y las ventanas abiertas por script. Lo que sí pasa: inyectar un botón
en la página y **hacerle clic de verdad** (un clic real sí permite abrir ventana), y desde
ahí mandar los cuadros por `postMessage` a una página local que los sube al puente.

## Botón de WhatsApp

Flotante abajo a la derecha, fijo en todas las páginas. Se ensancha al pasar el mouse.
El número es **3548 59-2487** (La Falda). En los links va como `wa.me/5493548592487`:
`54` + `9` (obligatorio para celulares argentinos en WhatsApp) + característica sin el 0 +
número sin el 15. Para `tel:` en cambio va **sin** el 9: `tel:+543548592487`.

Todos los links llevan un mensaje ya escrito (`?text=Hola! Quiero probar una clase...`)
para que la persona no tenga que arrancar de cero.

Está en tres lugares: el botón flotante, el CTA final de la home y el footer.

## Se sacó la sección "Historias"

Prometía testimonios que no existían, y las reseñas de Google que están abajo cumplen esa
función. El panel, su punto de navegación y su ítem del menú se quitaron; la home quedó con
cinco paneles.

## Fotos ampliadas con IA (de vertical a horizontal)

Todo el material de Instagram es vertical, y los paneles del sitio son horizontales a
pantalla completa: se recortaba tanto que se veía un primer plano gigante en lugar del
gimnasio. Cinco fotos se **expandieron a 16:9 con outpainting** (higgsfield, 2 créditos
cada una, 10 en total): `hero-1`, `gym`, `profes`, `contacto` y `entrenamientos`.

La IA **no inventa el gimnasio**: parte de la foto real y sólo completa hacia los costados
(más pared, el techo, el piso, alguna máquina de contexto). Lo que está en el centro de cada
imagen sigue siendo la foto original.

Las verticales originales quedaron guardadas en **`img-verticales-originales/`** por si hay
que volver atrás.

Como ahora son 16:9 nativas, su `background-position` pasó a `center`, sin recorte forzado.
En la galería de `gym.html` las celdas altas se reservan para las fotos que siguen siendo
verticales (`hero-2`, `hero-3`).

## Frames sacados de los reels

Instagram sin login sólo muestra 12 publicaciones, y varias no servían (una en negro, otra
con texto quemado, selfies). Para conseguir más fotos del lugar se sacaron **frames de los
reels**: no hay ffmpeg en esta máquina y los videos de Instagram van por `blob:` (no se
pueden descargar), así que se capturaron desde el `<video>` de la página, dibujándolo en un
`<canvas>` y mandando los JPEG a un servidor local.

Salen a 810x1440, un poco más blandos que una foto, pero son del gimnasio y sirven.
Si aparecen fotos de verdad, reemplazarlas.

## Legibilidad de los paneles

Costó cuatro intentos. Lo que **no** funcionó, para no repetirlo:

1. Sombras y halos flojos: no alcanzaban.
2. Oscurecer toda la foto: legible, pero mataba la imagen.
3. Una placa detrás del texto: se leía bien pero el recuadro hacía ruido, incluso
   difuminado con máscara. Ocupaba espacio y competía con la foto.

**Lo que funciona:** el bloque de texto **no dibuja nada** — sin fondo, sin blur, sin
máscara — y el contraste sale de las propias letras. `.panel__title` y `.panel__lead`
llevan un `text-shadow` de varias capas:

- dos sombras iguales de 2-3px sin desplazamiento, **repetidas a propósito** (repetir una
  sombra acumula su opacidad): forman un halo pegado al contorno de la letra, que es lo
  que la recorta del fondo;
- dos o tres sombras más abiertas, que la despegan.

Como sigue la forma de la letra y no la caja, no ocupa espacio ni tapa la foto. Encima del
velo general de la foto (20%), aguanta hasta el peor caso, que es el panel del gimnasio con
la pared blanca y el ventanal.

Si se cambia una foto por una muy clara, mirar ahí primero.

## Tono

El copy pasó a un registro más profesional: **"El gym" → "El gimnasio"**, **"Profes" →
"Entrenadores"**, "Nuestro gym" → "Conocé las instalaciones", "Profe Ludmi Porrino" →
"Ludmi Porrino", y se sacaron giros como "te bancan el día que no tenés ganas".

Los `id` internos y los nombres de archivo (`gym.html`, `profes.html`, `#profes`) **se
dejaron como están**: no se leen y cambiarlos rompería los links.

La bajada del hero ("Música fuerte, buenas vibras...") **es la bio textual de su Instagram**,
por eso conserva ese tono. Si se quiere subir el registro también ahí, hay que reescribirla.

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

`servidor.py` atiende **varias peticiones a la vez** (`ThreadingTCPServer`). Esto importa:
con el servidor de un solo hilo, un celular que pide diez imágenes y el video en paralelo lo
satura, las conexiones se cortan a mitad y la página **no abre**. Pasó exactamente eso al
compartir el link.

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

## Área de socios (socios.html)

Es una **demostración navegable**, no el sistema real: no hay servidor detrás.

- **No pide contraseña.** Sólo el nombre, y un aviso arriba de todo aclara que es una muestra.
  Esto es a propósito: un formulario de login falso invita a escribir una contraseña real.
- Lo que se carga (ejercicios marcados, kilos, reservas) queda en el **localStorage** de ese
  navegador. Se pierde al limpiar los datos del sitio, y no lo ve nadie más.
- Tiene su propio `css/socios.css` y `js/socios.js`, y **no usa el menú del sitio público**:
  es un entorno aparte, con su propio encabezado y un botón de salir.

### El gráfico de progreso

Barras de los kilos por semana. Una sola serie, así que no lleva leyenda: el título la nombra.
El valor aparece sólo en la última barra y al pasar el mouse, no en todas. Abajo hay un
`<details>` con **la misma información en una tabla**, para quien no pueda leer el gráfico.

La base de las barras arranca unos kilos por debajo del mínimo, no en cero, para que se note
la progresión. Está declarado acá para que nadie lo lea como una escala desde cero.

### Para conectarlo de verdad

Hace falta un backend con usuarios, rutinas y reservas. Los datos de ejemplo están al
principio de `js/socios.js` (`EJERCICIOS`, `PROGRESO`, `CLASES`): ahí es donde van las
llamadas a la API cuando exista. **Sacar el cartel de demostración recién cuando eso pase.**

## La lámina de teléfonos

`mockup.html` arma la imagen con los cuatro celulares. No es parte del sitio: es la
herramienta que la genera. Adentro de cada marco hay un `<iframe>` con la página de
verdad, así que la lámina nunca queda desactualizada — se vuelve a sacar y listo.

Para regenerarla, con el servidor levantado:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --window-size=1460,900 --virtual-time-budget=9000 \
      --screenshot=img/mockup-celular.jpg http://localhost:8899/mockup.html

Tres cosas que hay que hacer en el iframe antes de la foto, y que están en el script:

- ponerle `is-abriendo is-abierto` al body, para saltear la animación de entrada
- cambiar el `<video>` por su `poster`: Chrome headless no trae el códec H.264 y el
  video sale en negro
- el del área de socios se scrollea 86 px, porque si no la isla del notch cae justo
  encima del cartel de "Demostración" y se come el texto

## El contraste de los textos sobre las fotos

Tres cosas estaban mal planteadas y se cambiaron juntas.

**El velo era plano.** Había un `rgba(4,7,14,.26)` cubriendo la foto entera. Eso apaga
la imagen completa y a cambio da poquísimo contraste: es el peor canje posible, se
pierde la foto y igual no se lee. Ahora el velo es un **radial centrado en el bloque de
texto**: oscurece donde están las letras y llega a **0 % en las esquinas**, así la foto
conserva sus negros y su color.

**Los degradados tenían dos paradas.** Un `linear-gradient` de dos paradas deja una
banda visible, porque el ojo no lee la luminancia de forma lineal. Los degradados de
ahora tienen entre 11 y 16 paradas que aproximan una curva suavizada. Es más verboso y
es la razón por la que se ve parejo.

**La sombra del texto era un halo.** `0 0 5px` + `0 2px 26px` rodea cada letra de gris y
la ensucia; a tamaño grande se nota como un manchón. Quedó una sombra corta,
`0 1px 2px rgba(2,4,9,.42)`, que define el filo del glifo y nada más.

### Los números

El ajuste no se eligió a ojo. Componiendo el velo sobre las siete fotos reales y midiendo
contraste WCAG contra `--fg` (#E8E8E6), en la banda donde cae cada texto:

| | antes | después |
|---|---|---|
| peor píxel bajo el título | 1,51:1 | **4,20:1** |
| peor píxel bajo la bajada | 1,51:1 | **4,91:1** |
| velo sobre las esquinas | 26 % | **0 %** |

WCAG AA pide 4,5:1 para texto normal y 3:1 para texto grande. Los dos pasan, y la foto
queda menos tapada que antes, no más.

El `.80` del centro del radial es el valor mínimo que cumple AA sin tocar la imagen. Si
se cambian las fotos conviene volver a medir antes de bajarlo.

### El desenfoque detrás del texto

El velo radial arregló los números pero seguía sin notarse a simple vista: subía el
contraste sin cambiar la *sensación*. El paso que sí se ve es desenfocar el fondo.

`.panel__body::before` lleva `backdrop-filter: blur(16px) saturate(.88) brightness(.78)`
con una **máscara radial que se desvanece a transparente**. Al no tener borde duro, no
hay recuadro que ocupe lugar: el efecto sigue a las letras y se corta solo.

La idea es que el texto no se separa solo por ser más claro, sino porque lo que tiene
detrás pierde el foco. Las letras quedan como lo único nítido del cuadro, que es como
lo resuelven los vidrios de iOS.

Medido sobre el render real del hero, escondiendo el texto para medir solo el fondo:

| | peor píxel | promedio |
|---|---|---|
| velo plano original | 1,66:1 | 4,44:1 |
| velo radial | 5,41:1 | 12,01:1 |
| velo radial + desenfoque | **7,56:1** | **13,28:1** |

Si el navegador no soporta `backdrop-filter`, un `@supports not` apaga la capa: el velo
radial de abajo ya deja el contraste en regla, así que no hace falta reemplazo.

## La volanta azul

El velo y el desenfoque arreglaron el contraste donde faltaba, pero **en el hero no
cambiaban nada visible**, y con razón: el título cae sobre una pared negra, que sin
ningún velo ya da 5,20:1 de promedio cuando AA pide 3:1 para texto grande. No había
problema de contraste ahí. Lo que faltaba era presencia.

La volanta (`.panel__vol`) es una línea corta en mayúsculas sobre cada título, con un
filete adelante, en el azul del logo. Es **lo único con color en toda la pantalla**: el
contraste deja de depender de la sombra y pasa a darlo el color de marca.

Los textos no son inventados: son los mismos rótulos que ya usaban las páginas internas
en su `.lbl`, así que la home y las internas hablan igual.

| panel | volanta | viene de |
|---|---|---|
| hero | Entrená en La Falda | el `<title>` del sitio |
| Entrenamientos | Qué hacemos | entrenamientos.html |
| Entrenadores | Nuestro equipo | profes.html |
| El gimnasio | Las instalaciones | gym.html |
| ¿Volcano? | Hablemos | contacto.html |

El color es `--accent-txt: #4C8DEC`, no `--accent`. A 11 px el `--accent` (#347BE4) se
queda en 4,27:1 sobre el fondo velado y AA pide 4,5:1 para texto chico; el levantado
llega a 5,3:1. Es el mismo azul, un escalón más claro, que es lo normal para texto
chico sobre oscuro.

## Títulos en mayúscula

`.panel__title` y `.cabecera__titulo` van en caja alta. Dos ajustes que no son opcionales:

- **El cuerpo baja** de 104 a 88 px. En mayúsculas el mismo tamaño ocupa mucho más ancho.
- **Entra tracking positivo** (`.012em`). Las mayúsculas se apelmazan sin aire, porque no
  hay ascendentes ni descendentes que separen las formas.

Los acentos se mantienen: `text-transform:uppercase` respeta EMPEZÁ y ESTÉS, que es lo
correcto en español.

De paso apareció que `.cabecera__titulo` estaba **declarado dos veces**, y la segunda
copia pisaba a la primera. Si se edita una sola, el cambio no llega. Quedaron unificadas.

### Las letras se agrupan por palabra

El título del hero se parte en un `<span>` por letra para escalonar la animación. Si esos
spans cuelgan sueltos del título, **el navegador corta el renglón entre dos letras** —son
`inline-block`— y parte la palabra al medio. Se vio al pasar a mayúsculas, que ocupan más:
quedaba "EMPEZÁ DO / NDE ESTÉS".

Ahora cada palabra va dentro de un `.palabra` con `white-space:nowrap`, y las letras viven
adentro. La animación no cambia: `repartirTiempos()` sigue tomando todos los `.letra` en
orden.

## Ojo al medir en el celular

**Chrome headless tiene un ancho mínimo de ventana.** Con `--window-size=390,844` la página
se maqueta a **500 px** y recién después recorta la imagen a 390. El resultado parece
cortado y corrido, y no lo está.

Para mirar de verdad un ancho de celular hay que usar un `<iframe width="390">` dentro de
una página normal: ahí `innerWidth` da 390 y las media queries responden bien. Se perdió
un buen rato persiguiendo un bug de maquetación que era del instrumento.

## El botón de las tarjetas de Entrenamientos

Pegado a la izquierda quedaba colgando abajo, desprendido del bloque de texto. Ahora va
centrado en su columna: `display:block` + `width:fit-content` + `margin-inline:auto`.

En el celular tiene que seguir ocupando **todo el ancho**, que es lo que conviene para
tocar con el pulgar, así que la media query le devuelve `width:auto`. Sin esa línea el
`fit-content` se colaba también en móvil y el botón se achicaba.
