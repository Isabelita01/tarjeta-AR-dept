import * as ecs from '@8thwall/ecs'

// Botón de interfaz que abre un enlace (redes, portafolio, WhatsApp...).
// Cambia la URL desde el campo "url" de cada botón en la escena.
ecs.registerComponent({
  name: 'open-url-button',
  schema: {
    url: ecs.string,
  },
  schemaDefaults: {
    url: 'https://www.instagram.com/',
  },
  add: (world, component) => {
    const {url} = component.schema
    world.events.addListener(component.eid, ecs.input.UI_CLICK, () => {
      if (url) window.open(url, '_blank')
    })
  },
})
