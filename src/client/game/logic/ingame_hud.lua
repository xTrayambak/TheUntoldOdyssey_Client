--[[
  Loads up the in-game HUD
--]]

GameStates = tuo.getSharedData().GameStates

local HEART_COUNT = 5

function load_hud()
  log('Loading up ingame HUD.', 'Worker/IngameHUD')

  v = Vector3(4, 5, 6)
end

function main(current_state, previous_state)
  -- Prevent reloading the UI.
  if current_state == GameStates.INGAME and previous_state ~= GameStates.SETTINGS then
    load_hud()
  end
end

tuo.get_event('on_state_change').subscribe(main)
