--[[
  Loads up the in-game HUD
--]]

GameStates = tuo.getSharedData().GameStates

function load_hud()
  tuo.log('Loading up ingame HUD.', 'Worker/IngameHUD')
  
  heart_full_texture = image_loader.load_image('assets/img/heart_full.png', {0.5, 0, 0}, 0.1)
  heart_half_texture = image_loader.load_image('assets/img/heart_half.png', nil, 0.1)
end

function main(current_state, previous_state)
  if current_state == GameStates.INGAME then
    load_hud()
  end
end

tuo.get_event('on_state_change').subscribe(main)
