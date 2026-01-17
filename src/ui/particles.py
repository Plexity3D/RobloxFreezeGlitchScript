"""
Particle system for RoFreeze background.
Creates floating particles that drift across the screen for an atmospheric effect.
"""

import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QBrush

class Particle:
    """Individual particle with position, velocity, and size."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = random.uniform(2.0, 5.0)
        self.speed_y = random.uniform(0.2, 0.8)  # Upward drift
        self.speed_x = random.uniform(-0.2, 0.2) # Horizontal sway
        self.opacity = random.randint(30, 100)
        self.max_opacity = self.opacity
        self.fade_speed = random.uniform(0.5, 2.0)
        self.fading_in = True
        
        # Screen bounds for reset
        self.bounds_width = width
        self.bounds_height = height

    def update(self):
        """Update position and opacity."""
        self.y -= self.speed_y
        self.x += self.speed_x
        
        # Reset if out of bounds (top)
        if self.y < -10:
            self.y = self.bounds_height + 10
            self.x = random.randint(0, self.bounds_width)
            self.opacity = 0
            self.fading_in = True
            
        # Wrap horizontal
        if self.x < -10:
            self.x = self.bounds_width + 10
        elif self.x > self.bounds_width + 10:
            self.x = -10
            
        # Twinkle/Fade effect
        if self.fading_in:
            self.opacity += self.fade_speed
            if self.opacity >= self.max_opacity:
                self.opacity = self.max_opacity
                self.fading_in = False
        else:
            self.opacity -= self.fade_speed
            if self.opacity <= 20:  # Don't disappear completely
                self.opacity = 20
                self.fading_in = True

class ParticleSystem(QWidget):
    """Widget that renders a system of floating particles."""
    
    def __init__(self, parent=None, count=30):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.particles = []
        self.particle_count = count
        
        # Timer for animation loop (30 FPS is sufficient for background)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(33)
        
        self.initialized = False

    def resizeEvent(self, event):
        """Initialize particles on first resize when logic has dimensions."""
        super().resizeEvent(event)
        if not self.initialized and self.width() > 0:
            self._init_particles()
            self.initialized = True
        
        # Update bounds for existing particles
        for p in self.particles:
            p.bounds_width = self.width()
            p.bounds_height = self.height()

    def _init_particles(self):
        """Create initial set of particles."""
        self.particles = []
        for _ in range(self.particle_count):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            self.particles.append(Particle(x, y, self.width(), self.height()))

    def update_particles(self):
        """Update all particles and repaint."""
        for p in self.particles:
            p.update()
        self.update()

    def paintEvent(self, event):
        """Draw the particles."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Particle color (cyan-ish white)
        color = QColor(200, 240, 255)
        
        for p in self.particles:
            color.setAlpha(int(p.opacity))
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(p.x, p.y), p.size/2, p.size/2)
            
        painter.end()
