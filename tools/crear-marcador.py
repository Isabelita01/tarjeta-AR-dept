"""Convierte una imagen (el diseño de la tarjeta) en un marcador de 8th Wall.

Uso:
    python3 tools/crear-marcador.py ruta/a/mi-tarjeta.png

Genera en image-targets/ los archivos Tarjeta.json, Tarjeta_original.jpg,
Tarjeta_cropped.jpg, Tarjeta_luminance.jpg y Tarjeta_thumbnail.jpg, con el mismo
formato que produce 8th Wall. Si la imagen es horizontal se gira para que el
recorte 3:4 vertical aproveche toda la tarjeta.
"""
import json
import sys
import time
from pathlib import Path

from PIL import Image

NAME = 'Tarjeta'
OUT = Path(__file__).resolve().parent.parent / 'image-targets'


def main(src: str) -> None:
    image = Image.open(src).convert('RGB')
    rotated = image.width > image.height
    if rotated:
        image = image.rotate(90, expand=True)

    # Escala para que el lado corto quede en 768 px y recorta al centro a 3:4.
    scale = 768 / min(image.width, image.height * 3 / 4)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left = (image.width - 768) // 2
    top = (image.height - 1024) // 2
    cropped = image.crop((left, top, left + 768, top + 1024))

    OUT.mkdir(exist_ok=True)
    image.save(OUT / f'{NAME}_original.jpg', quality=92)
    cropped.save(OUT / f'{NAME}_cropped.jpg', quality=92)
    cropped.convert('L').resize((480, 640), Image.LANCZOS).convert('RGB').save(
        OUT / f'{NAME}_luminance.jpg', quality=92)
    cropped.resize((263, 350), Image.LANCZOS).save(OUT / f'{NAME}_thumbnail.jpg', quality=88)

    now = int(time.time() * 1000)
    data = {
        'type': 'PLANAR',
        'properties': {
            'top': top, 'left': left, 'width': 768, 'height': 1024,
            'isRotated': rotated,
            'originalWidth': image.width, 'originalHeight': image.height,
        },
        'imagePath': f'image-targets/{NAME}_luminance.jpg',
        'metadata': None,
        'name': NAME,
        'resources': {
            'originalImage': f'{NAME}_original.jpg',
            'croppedImage': f'{NAME}_cropped.jpg',
            'thumbnailImage': f'{NAME}_thumbnail.jpg',
            'luminanceImage': f'{NAME}_luminance.jpg',
        },
        'created': now,
        'updated': now,
    }
    (OUT / f'{NAME}.json').write_text(json.dumps(data, indent=2))
    print(f'Marcador listo en {OUT}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
