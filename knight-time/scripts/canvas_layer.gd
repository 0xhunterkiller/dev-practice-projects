extends CanvasLayer

@onready var death_label: Label = $DeathLabel
@onready var win_label: Label = $WinLabel


func reset():
	for node in get_tree().get_nodes_in_group("ui_on_restart_hide"):
		node.visible = false
		if node.has_method("reset"):
			node.reset()

func show_death_label():
	death_label.visible = true

func show_win_label():
	win_label.visible = true
