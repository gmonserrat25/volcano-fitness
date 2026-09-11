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

## Imágenes

Las 10 fotos son **generadas con IA** (modelo `z_image`, 1,5 créditos en total) siguiendo la
descripción del interior real: paredes negras texturadas, arcos LED cálidos detrás de los racks,
máquinas negras, ventanales, y las sierras para la caminata.
**Son provisorias**: reemplazar por fotos reales del gym cuando estén.

Archivos en `img/`: `hero-1..5.jpg` (slideshow del hero), `entrenamientos.jpg`, `profes.jpg`,
`gym.jpg`, `historias.jpg`, `contacto.jpg`.

## Falta completar

Buscar `[COMPLETAR` en `index.html`:
- dirección, horarios, teléfono, email
- número de WhatsApp
- puntaje y cantidad de reseñas de Google, y el link para calificar
- el titular del hero ("Despertá el volcán") es una propuesta, no está confirmado
