extends Area2D

func _on_body_entered(body: Node2D) -> void:
	print("Entered Coin")
	game_manager.add_point()
	self.queue_free()
