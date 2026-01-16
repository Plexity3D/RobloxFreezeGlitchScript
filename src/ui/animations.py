"""
Reusable animation utilities for RoFreeze UI.
Provides smooth, 60fps animations using QPropertyAnimation.
"""

from PyQt6.QtCore import (QPropertyAnimation, QEasingCurve, 
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          pyqtProperty, QObject)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget


class AnimationHelper:
    """Static methods for creating common animations."""
    
    @staticmethod
    def pulse_opacity(widget: QWidget, min_opacity=0.5, max_opacity=1.0, 
                      duration=1000, loop=True) -> QPropertyAnimation:
        """Creates a pulsing opacity animation."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(min_opacity)
        anim.setEndValue(max_opacity)
        anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        
        if loop:
            anim.setLoopCount(-1)  # Infinite loop
            # Create back-and-forth effect
            anim.finished.connect(lambda: None)
        
        return anim
    
    @staticmethod
    def fade_in(widget: QWidget, duration=300) -> QPropertyAnimation:
        """Fade in animation."""
        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(0)
        widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        return anim
    
    @staticmethod
    def fade_out(widget: QWidget, duration=300) -> QPropertyAnimation:
        """Fade out animation."""
        effect = widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        return anim


class GlowEffect(QObject):
    """
    Custom property holder for animating glow intensity.
    Use with stylesheets that reference the glow value.
    """
    def __init__(self, widget: QWidget, base_color="#22D3EE"):
        super().__init__(widget)
        self._widget = widget
        self._glow = 0.0
        self._base_color = base_color
        self._animation = None
    
    @pyqtProperty(float)
    def glow(self):
        return self._glow
    
    @glow.setter
    def glow(self, value):
        self._glow = value
        self._update_style()
    
    def _update_style(self):
        """Update widget shadow based on glow intensity."""
        # Convert glow (0-1) to blur radius (0-20) and spread
        blur = int(self._glow * 20)
        alpha = int(self._glow * 200)
        
        # Parse base color
        color = self._base_color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        
        shadow = f"rgba({r}, {g}, {b}, {alpha})"
        # Note: Qt stylesheets don't support box-shadow directly
        # This is a placeholder for border-glow effect
        if hasattr(self._widget, 'update_glow'):
            self._widget.update_glow(blur, shadow)
    
    def start_pulse(self, duration=1500):
        """Start a pulsing glow animation."""
        self._animation = QPropertyAnimation(self, b"glow")
        self._animation.setDuration(duration)
        self._animation.setStartValue(0.3)
        self._animation.setEndValue(1.0)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._animation.setLoopCount(-1)
        
        # Ping-pong by reversing direction
        self._animation.finished.connect(self._reverse)
        self._animation.start()
    
    def _reverse(self):
        if self._animation:
            start = self._animation.startValue()
            end = self._animation.endValue()
            self._animation.setStartValue(end)
            self._animation.setEndValue(start)
            self._animation.start()
    
    def stop(self):
        if self._animation:
            self._animation.stop()
            self._glow = 0.0
            self._update_style()
