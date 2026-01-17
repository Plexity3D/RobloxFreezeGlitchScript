"""
Enhanced widgets for RoFreeze UI.
Provides styled buttons with gradients, glow effects, and animations.
"""

from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QHBoxLayout
from PyQt6.QtGui import QFont, QCursor, QColor, QPainter, QLinearGradient, QPen
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect


class ModernButton(QPushButton):
    """Enhanced button with gradient, glow, and hover animations."""
    
    def __init__(self, text, parent=None, is_primary=True):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(50)
        self._is_primary = is_primary
        self._hover_progress = 0.0
        self._is_active = False
        
        font = QFont("Segoe UI", 11)
        font.setBold(True)
        self.setFont(font)
        
        # Setup hover animation
        self._hover_anim = QPropertyAnimation(self, b"hoverProgress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._apply_style()
    
    @pyqtProperty(float)
    def hoverProgress(self):
        return self._hover_progress
    
    @hoverProgress.setter
    def hoverProgress(self, value):
        self._hover_progress = value
        self.update()
    
    def _apply_style(self):
        """Apply base stylesheet."""
        if self._is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: white;
                    border-radius: 25px;
                    border: 2px solid rgba(34, 211, 238, 0.5);
                    padding: 0 30px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #aaaaaa;
                    border-radius: 20px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 10);
                    color: white;
                }
            """)
    
    def set_active(self, active: bool):
        """Set button active state (changes color scheme)."""
        self._is_active = active
        self.update()
    
    def enterEvent(self, event):
        """Animate hover in."""
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Animate hover out."""
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """Custom paint with gradient and glow."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        radius = 25
        
        if self._is_primary:
            # Create gradient based on state
            gradient = QLinearGradient(0, 0, rect.width(), 0)
            
            if self._is_active:
                # Active state: teal gradient
                gradient.setColorAt(0, QColor(13, 59, 102))  # Deep blue
                gradient.setColorAt(1, QColor(34, 211, 238))  # Cyan
            else:
                # Normal state: subtle dark gradient
                base_alpha = int(60 + (self._hover_progress * 40))
                gradient.setColorAt(0, QColor(40, 40, 50, base_alpha + 100))
                gradient.setColorAt(1, QColor(60, 60, 70, base_alpha + 100))
            
            # Draw glow on hover
            if self._hover_progress > 0:
                glow_color = QColor(34, 211, 238)
                glow_alpha = int(self._hover_progress * 80)
                glow_color.setAlpha(glow_alpha)
                
                # Outer glow
                glow_rect = rect.adjusted(-4, -4, 4, 4)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow_color)
                painter.drawRoundedRect(glow_rect, radius + 4, radius + 4)
            
            # Draw button background
            painter.setBrush(gradient)
            
            # Border
            border_color = QColor(34, 211, 238)
            border_alpha = int(80 + self._hover_progress * 175)
            border_color.setAlpha(border_alpha)
            painter.setPen(QPen(border_color, 2))
            
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)
            
            # Ripple effect (if implemented later, adds nice touch)
            
        # Draw text
        painter.setPen(QColor(255, 255, 255))
        font = self.font()
        # Scale effect on text
        if self._hover_progress > 0:
            font.setPointSize(11 + int(self._hover_progress))
        
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        
        painter.end()

    def mousePressEvent(self, event):
        """Scale down on press."""
        super().mousePressEvent(event)
        self.animate_scale(0.95)

    def mouseReleaseEvent(self, event):
        """Scale back up."""
        super().mouseReleaseEvent(event)
        self.animate_scale(1.0)
        
    def animate_scale(self, scale):
        # Implementation for scale animation would go here
        # For now we use simple property hook or could add a transform
        pass


class KeyBadge(QWidget):
    """Styled keyboard shortcut badge with 3D depth and press animation."""
    
    def __init__(self, key: str, label: str = "", parent=None, tooltip: str = ""):
        super().__init__(parent)
        self._key = key
        self._label = label
        self._pressed = False
        self._press_offset = 0
        
        self.setFixedSize(80, 75) # Increased height for movement
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if tooltip:
            self.setToolTip(tooltip)

        # Set accessible name for screen readers
        self.setAccessibleName(f"Key {key}, {label}")
    
    def set_pressed(self, pressed: bool):
        """Visual feedback for key press with animation."""
        self._pressed = pressed
        self._press_offset = 4 if pressed else 0
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw key badge
        y_offset = self._press_offset
        key_rect = QRect(15, 5 + y_offset, 50, 40)
        shadow_rect = QRect(15, 45, 50, 4 - y_offset) # Shadow extrusion
        
        if self._pressed:
             # Pressed state - flatter
            painter.setBrush(QColor(34, 211, 238, 180))
            painter.setPen(QPen(QColor(34, 211, 238), 2))
        else:
            # Normal state - 3D look
            # Draw "side"/shadow first for 3D effect
            painter.setBrush(QColor(20, 20, 30, 200))
            painter.setPen(Qt.PenStyle.NoPen)
            # Draw extrusion manually
            path = QPainter.RenderHint.Antialiasing
            painter.drawRoundedRect(15, 10, 50, 40, 8, 8) # Shadow layer
            
            # Main face
            painter.setBrush(QColor(40, 40, 50, 230))
            painter.setPen(QPen(QColor(100, 100, 120), 1))
        
        # Draw main key cap
        if not self._pressed:
            # 3D Side (Shadow/Depth)
            painter.setBrush(QColor(20, 20, 25))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(15, 9, 50, 40, 8, 8)
            
            # Top Face
            painter.setBrush(QColor(45, 45, 55))
            painter.setPen(QPen(QColor(80, 80, 90), 1))
            painter.drawRoundedRect(15, 5, 50, 40, 8, 8)
        else:
            # Pressed Face
            painter.setBrush(QColor(34, 211, 238, 40))
            painter.setPen(QPen(QColor(34, 211, 238), 2))
            painter.drawRoundedRect(15, 9, 50, 40, 8, 8)
        
        # Key text
        painter.setPen(QColor(255, 255, 255) if not self._pressed else QColor(34, 211, 238))
        font = QFont("Segoe UI", 14)
        font.setBold(True)
        painter.setFont(font)
        # Center text on the face
        text_rect = QRect(15, 5 + y_offset, 50, 40)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._key)
        
        # Label below
        if self._label:
            painter.setPen(QColor(150, 150, 160))
            font.setPointSize(8)
            font.setBold(False)
            painter.setFont(font)
            label_rect = QRect(0, 53, 80, 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, self._label)
        
        painter.end()


class StatusIndicator(QWidget):
    """Animated status indicator with pulsing ring."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._status = "ready"  # ready, running, frozen
        self._pulse = 0.0
        self._text = "Ready"
        
        self.setFixedSize(200, 40)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Pulse animation
        self._pulse_anim = QPropertyAnimation(self, b"pulse")
        self._pulse_anim.setDuration(1200)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
    
    @pyqtProperty(float)
    def pulse(self):
        return self._pulse
    
    @pulse.setter
    def pulse(self, value):
        self._pulse = value
        self.update()
    
    def set_status(self, status: str, text: str = ""):
        """Update status and text."""
        self._status = status
        self._text = text or status.capitalize()
        
        if status in ("running", "frozen"):
            self._pulse_anim.start()
        else:
            self._pulse_anim.stop()
            self._pulse = 0.0
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw Glassmorphism Background
        painter.setBrush(QColor(30, 40, 50, 100))
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        painter.drawRoundedRect(self.rect(), 20, 20)

        center_x = 25
        center_y = self.height() // 2
        
        # Status colors
        colors = {
            "ready": QColor(150, 150, 160),
            "running": QColor(34, 211, 238),
            "frozen": QColor(96, 165, 250), # Icy blue
            "stopped": QColor(248, 113, 113)
        }
        color = colors.get(self._status, colors["ready"])
        
        # Draw pulsing rings for active states
        if self._status in ("running", "frozen"):
            ring_color = QColor(color)
            ring_alpha = int((1 - self._pulse) * 150)
            ring_color.setAlpha(ring_alpha)
            
            ring_radius = int(8 + self._pulse * 12)
            painter.setPen(QPen(ring_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(center_x - ring_radius, center_y - ring_radius,
                               ring_radius * 2, ring_radius * 2)
        
        # Draw center dot
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(center_x - 6, center_y - 6, 12, 12)
        
        # Draw text
        painter.setPen(color)
        font = QFont("Segoe UI", 10)
        font.setBold(True)
        painter.setFont(font)
        text_rect = QRect(50, 0, 140, self.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | 
                        Qt.AlignmentFlag.AlignLeft, self._text)
        
        painter.end()
