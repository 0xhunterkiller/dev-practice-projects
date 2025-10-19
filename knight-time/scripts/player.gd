extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -400.0
var is_dead: bool = false
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D

func die():
	print("player died")
	is_dead = true
	animated_sprite_2d.play("death")
	audio_manager.play_death()
	ui.show_death_label()
	game_manager.restart_game()

func _physics_process(delta: float) -> void:
	if is_dead:
		velocity = Vector2.ZERO
		return  # Skip everything if dead
	# Add the gravity.
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Handle jump.
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY
		if animated_sprite_2d.animation != "idle":
			animated_sprite_2d.play("idle")
			

	# Get the input direction and handle the movement/deceleration.
	var direction := Input.get_axis("move_left", "move_right")
	if direction:
		if animated_sprite_2d.animation != "run":
			animated_sprite_2d.play("run")
		if direction < 0:
			animated_sprite_2d.flip_h = true
		elif direction > 0:
			animated_sprite_2d.flip_h = false
		velocity.x = direction * SPEED
	else:
		if animated_sprite_2d.animation != "idle":
			animated_sprite_2d.play("idle")
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()
