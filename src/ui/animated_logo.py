"""
Animated logo widget for RoFreeze.
Displays the snowflake icon with subtle rotation and glow effects.
"""

import os
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPixmap, QPainter, QColor


class AnimatedLogo(QWidget):
    """Animated snowflake logo with rotation and glow effects."""
    
    def __init__(self, parent=None, size=80):
        super().__init__(parent)
        self._size = size
        self._rotation = 0.0
        self._glow_intensity = 0.0
        self._is_active = False
        
        self.setFixedSize(size + 40, size + 40)  # Extra space for glow
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Load the icon
        icon_path = os.path.join(os.path.dirname(__file__), 
                                  '..', '..', 'RoFreezeIcon.png')
        self._original_pixmap = QPixmap(icon_path)
        if self._original_pixmap.isNull():
            # Fallback to just text if icon not found
            self._original_pixmap = None
        else:
            # Scale to desired size
            self._original_pixmap = self._original_pixmap.scaled(
                size, size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
        # Setup animations
        self._setup_animations()
    
    def _setup_animations(self):
        """Initialize rotation and glow animations."""
        # Slow rotation animation
        self._rotation_anim = QPropertyAnimation(self, b"rotation")
        self._rotation_anim.setDuration(20000)  # 20 seconds for full rotation
        self._rotation_anim.setStartValue(0.0)
        self._rotation_anim.setEndValue(360.0)
        self._rotation_anim.setLoopCount(-1)
        self._rotation_anim.setEasingCurve(QEasingCurve.Type.Linear)
        
        # Glow pulse animation (only when active)
        self._glow_anim = QPropertyAnimation(self, b"glowIntensity")
        self._glow_anim.setDuration(1500)
        self._glow_anim.setStartValue(0.3)
        self._glow_anim.setEndValue(1.0)
        self._glow_anim.setLoopCount(-1)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    
    @pyqtProperty(float)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.update()
    
    @pyqtProperty(float)
    def glowIntensity(self):
        return self._glow_intensity
    
    @glowIntensity.setter
    def glowIntensity(self, value):
        self._glow_intensity = value
        self.update()
    
    def start_animations(self):
        """Start the rotation animation."""
        self._rotation_anim.start()
    
    def set_active(self, active: bool):
        """Toggle active state (enables glow pulse)."""
        self._is_active = active
        if active:
            self._glow_anim.start()
        else:
            self._glow_anim.stop()
            self._glow_intensity = 0.0
            self.update()
    
    def paintEvent(self, event):
        """Custom paint with rotation and glow."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Draw glow effect when active
        if self._is_active and self._glow_intensity > 0:
            glow_color = QColor(34, 211, 238)  # Cyan #22D3EE
            glow_color.setAlphaF(self._glow_intensity * 0.5)
            
            # Draw multiple expanding circles for glow
            for i in range(3):
                radius = self._size // 2 + 5 + (i * 8)
                alpha = self._glow_intensity * (0.3 - i * 0.1)
                glow_color.setAlphaF(max(0, alpha))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow_color)
                painter.drawEllipse(center_x - radius, center_y - radius, 
                                   radius * 2, radius * 2)
        
        # Draw the rotated pixmap
        if self._original_pixmap:
            painter.translate(center_x, center_y)
            painter.rotate(self._rotation)
            painter.translate(-self._size // 2, -self._size // 2)
            painter.drawPixmap(0, 0, self._original_pixmap)
        else:
            # Fallback: draw a snowflake emoji
            painter.translate(center_x, center_y)
            painter.rotate(self._rotation)
            painter.setPen(QColor(255, 255, 255))
            font = painter.font()
            font.setPointSize(40)
            painter.setFont(font)
            painter.drawText(-20, 15, "❄")
        
        painter.end()
