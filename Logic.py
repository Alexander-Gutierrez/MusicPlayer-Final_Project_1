from PyQt6.QtWidgets import *
from PyQt6.QtCore import QUrl, Qt
from PyQt6 import QtGui
import pygame
import os
from gui import *


class Logic(QMainWindow, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Set up icons for buttons
        icon_skip_forward = QtGui.QIcon("D:/reposit/Final Project  1/Icons/Media_Skip_Forward(1).png")
        icon_skip_backward = QtGui.QIcon("D:/reposit/Final Project  1/Icons/Media_Skip_Back.png")
        icon_play = QtGui.QIcon("D:/reposit/Final Project  1/Icons/Play_image.png")
        self.Backward_button.setIcon(icon_skip_backward)
        self.Play_pause_button.setIcon(icon_play)
        self.Forward_button.setIcon(icon_skip_forward)

        # Set up a QLabel for displaying cover art (already created in Qt Designer)
        self.cover_art_label = self.cover_art  # Access the existing QLabel by its object name

        # Initializing pygame mixer
        self.current_song_index = 0
        self.playlist = [
            "D:/reposit/Final Project  1/Music/Clairo - Juna.wav",
            "D:/reposit/Final Project  1/Music/Never Be Yours.wav",
            "D:/reposit/Final Project  1/Music/Pink+ White.wav"
        ]
        self.cover_art_folder = "D:/reposit/Final Project  1/Cover Art/"  # Folder containing cover art images
        self.load_song(self.current_song_index)

        # Variable to track whether the music is playing
        self.is_playing = False
        self.current_position = 0  # Track the current position of the song when paused

        # Connect button actions
        self.Forward_button.clicked.connect(self.media_skip_forward)
        self.Backward_button.clicked.connect(self.media_skip_backward)
        self.Play_pause_button.clicked.connect(self.play_pause_button)

    def load_song(self, index):
        """Load the song from the playlist and update cover art."""
        if 0 <= index < len(self.playlist):
            self.current_song = self.playlist[index]
            print(f"Loading song: {self.current_song}")
            try:
                pygame.mixer.music.load(self.current_song)
            except pygame.error as e:
                print(f"Error loading song: {e}")
                # Handle the error (skip to the next song)

            # Get cover art path
            song_name = os.path.basename(self.current_song).replace(".wav", ".jpg")
            cover_art_path = os.path.join(self.cover_art_folder, song_name)

            # Update cover art if the file exists
            if os.path.exists(cover_art_path):
                self.update_cover_art(cover_art_path)
            else:
                print(f"Cover art not found for {self.current_song}")

        else:
            print("Invalid song index")

    def update_cover_art(self, cover_art_path):
        """Update the QLabel with the corresponding cover art image."""
        pixmap = QtGui.QPixmap(cover_art_path)
        pixmap = pixmap.scaled(self.cover_art_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.cover_art_label.setPixmap(pixmap)

    def media_skip_forward(self):
        """Skip to the next song in the playlist."""
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            self.load_song(self.current_song_index)
            self.play_music()
        else:
            print("No more songs in the playlist")

    def media_skip_backward(self):
        """Skip to the previous song in the playlist."""
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.load_song(self.current_song_index)
            self.play_music()
        else:
            print("Already at the first song")

    def play_pause_button(self):
        """Toggle play and pause for the current song."""
        print(f"Playback state: {pygame.mixer.music.get_busy()}")
        if self.is_playing:
            pygame.mixer.music.pause()
            self.current_position = pygame.mixer.music.get_pos()  # Get the current position when paused
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()  # Unpause from the last position
            pygame.mixer.music.play(start=self.current_position / 1000)  # Convert to seconds
            self.is_playing = True

    def play_music(self):
        """Play the current loaded music."""
        pygame.mixer.music.play()
        print(f"Playing: {self.current_song}")
        self.is_playing = True
