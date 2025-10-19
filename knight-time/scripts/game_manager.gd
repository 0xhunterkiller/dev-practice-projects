extends Node2D

var score: int = 0
var restart_timer: Timer
var coins_left: int = 0

# Instantiate a new timer
func _ready():
	restart_timer = Timer.new()
	restart_timer.wait_time = 2.0
	restart_timer.one_shot = true
	restart_timer.connect("timeout", Callable(self, "_on_restart_timer_timeout"))
	add_child(restart_timer)
	
func add_point():
	coins_left = get_tree().get_nodes_in_group("coins").size()
	coins_left -= 1
	if coins_left == 0:
		ui.show_win_label()
		self.restart_game()
	audio_manager.play_coin()
	
# Wait for 2 seconds
func restart_game():
	restart_timer.start()
	
# Reload the game scene
func _on_restart_timer_timeout() -> void:
	ui.reset()
	get_tree().reload_current_scene()
