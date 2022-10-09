local GameStates = tuo.getSharedData().GameStates

function load_map(current_state, previous_state)
  if current_state == GameStates.INGAME and previous_state ~= GameStates.SETTINGS then
    log('Loading map!', 'Worker/MapLoader')
    --[[local map = Object(tuo, 'assets/models/map_area_starting_plains.obj')
    map.set_texture('assets/textures/terrain/overworld_grass_1.jpg')--]]
  end
end

function main()
  tuo.get_event('on_state_change').subscribe(load_map)
end

main()
