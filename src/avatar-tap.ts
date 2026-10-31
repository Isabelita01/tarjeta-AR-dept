import * as ecs from '@8thwall/ecs'

// Al tocar el avatar, la animación se pausa o se reanuda.
ecs.registerComponent({
  name: 'avatar-tap',
  add: (world, component) => {
    world.events.addListener(component.eid, ecs.input.SCREEN_TOUCH_START, () => {
      ecs.GltfModel.mutate(world, component.eid, (model) => {
        model.paused = !model.paused
      })
    })
  },
})
