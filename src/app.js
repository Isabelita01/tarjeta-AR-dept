// Registra el marcador de la tarjeta (image-targets/Tarjeta.json) en el motor de RA.
const onxrloaded = () => {
  XR8.XrController.configure({
    imageTargetData: [
      require('../image-targets/Tarjeta.json'),
    ],
  })
}
window.XR8 ? onxrloaded() : window.addEventListener('xrloaded', onxrloaded)
