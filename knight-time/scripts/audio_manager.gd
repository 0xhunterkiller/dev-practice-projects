extends Node2D

@onready var coin_sound: AudioStreamPlayer2D = $CoinSound
@onready var death_sound: AudioStreamPlayer2D = $DeathSound

func play_coin():
	coin_sound.play()

func play_death():
	death_sound.play()
