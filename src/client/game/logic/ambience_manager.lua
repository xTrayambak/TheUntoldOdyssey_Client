--[[
  Ambience Manager for the game, rewritten in LUA.
--]]

local GameStates = tuo.getSharedData().GameStates
local Task = tuo.get_task_signals()

local first_runtime_cycle = true

local songs_ingame_overworld = {'assets/music/gone.mp3', 'assets/music/harbinger_of_joy.mp3', 'assets/music/sonata.flac'}
local songs_ingame_hell = {}
local songs_ingame_void = {'assets/music/mist001.flac', 'assets/music/mist002.flac'}

local songs_menu = {'assets/music/unlighted.mp3'}

function ambience_task()
  if tuo.get_volume_master() == 0 then
    return Task.cont
  end

  if first_runtime_cycle == true then
    first_runtime_cycle = false
    return Task.pause(random.randint(10, 25))
  end


  if tuo.getState() == GameStates.MENU then
    local audio = audio_loader.load(random.choice(songs_menu))
    audio.play()

    return Task.pause(random.randint(80, 80 + audio.get_length_int()))
  end

  if tuo.getState() == GameStates.INGAME then
    local audio = audio_loader.load(random.choice(songs_ingame_overworld))
    audio.play()

    return Task.pause(random.randint(256, 256 + audio.get_length_int()))
  end

  return tuo.get_task_signals().cont
end

function main()
  tuo.new_task('ambience', ambience_task, true)
end

main()
