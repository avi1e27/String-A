import numpy as np
import cv2
from PIL import Image, ImageDraw
import streamlit as st
import io
import json
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class StringArtConfig:
    """Configuration for string art generation"""
    num_pins: int
    num_connections: int
    canvas_size: int = 800
    pin_radius: int = 3
    string_opacity: float = 0.3
    
class StringArtGenerator:
    def __init__(self, config: StringArtConfig):
        self.config = config
        self.pins = self._generate_pins()
        self.canvas = np.ones((config.canvas_size, config.canvas_size), dtype=np.float32)
        self.line_cache = {}
        
    def _generate_pins(self) -> List[Tuple[int, int]]:
        """Generate pin positions around the circle perimeter"""
        center = self.config.canvas_size // 2
        radius = center - 50  # Leave some margin
        pins = []
        
        for i in range(self.config.num_pins):
            angle = 2 * math.pi * i / self.config.num_pins
            x = int(center + radius * math.cos(angle))
            y = int(center + radius * math.sin(angle))
            pins.append((x, y))
            
        return pins
    
    def _get_line_pixels(self, pin1_idx: int, pin2_idx: int) -> List[Tuple[int, int]]:
        """Get all pixels on the line between two pins using Bresenham's algorithm"""
        cache_key = (min(pin1_idx, pin2_idx), max(pin1_idx, pin2_idx))
        if cache_key in self.line_cache:
            return self.line_cache[cache_key]
            
        x1, y1 = self.pins[pin1_idx]
        x2, y2 = self.pins[pin2_idx]
        
        pixels = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        while True:
            if 0 <= x < self.config.canvas_size and 0 <= y < self.config.canvas_size:
                pixels.append((x, y))
            
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
                
        self.line_cache[cache_key] = pixels
        return pixels
    
    def _calculate_line_darkness(self, pin1_idx: int, pin2_idx: int, target_image: np.ndarray) -> float:
        """Calculate how much darkness a line would add to match the target image"""
        pixels = self._get_line_pixels(pin1_idx, pin2_idx)
        total_benefit = 0
        
        for x, y in pixels:
            if 0 <= x < self.config.canvas_size and 0 <= y < self.config.canvas_size:
                # How dark should this pixel be vs how dark it currently is
                target_darkness = 1 - target_image[y, x]  # Invert for darkness
                current_darkness = 1 - self.canvas[y, x]
                
                # Benefit of adding a string (making it darker)
                benefit = max(0, target_darkness - current_darkness)
                total_benefit += benefit
                
        return total_benefit / len(pixels) if pixels else 0
    
    def _add_string(self, pin1_idx: int, pin2_idx: int):
        """Add a string between two pins to the canvas"""
        pixels = self._get_line_pixels(pin1_idx, pin2_idx)
        
        for x, y in pixels:
            if 0 <= x < self.config.canvas_size and 0 <= y < self.config.canvas_size:
                # Make the pixel darker (string adds darkness)
                self.canvas[y, x] = max(0, self.canvas[y, x] - self.config.string_opacity)
    
    def generate_string_art(self, image_path: str = None, image_array: np.ndarray = None) -> Tuple[np.ndarray, List[int]]:
        """
        Generate string art from an image
        
        Args:
            image_path: Path to image file (optional)
            image_array: Image as numpy array (optional)
            
        Returns:
            Tuple of (result_image, connection_sequence)
        """
        # Load and preprocess image
        if image_array is not None:
            image = image_array
        else:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
        # Resize and normalize image to match canvas
        image = cv2.resize(image, (self.config.canvas_size, self.config.canvas_size))
        image = image.astype(np.float32) / 255.0
        
        # Create circular mask
        center = self.config.canvas_size // 2
        radius = center - 50
        y, x = np.ogrid[:self.config.canvas_size, :self.config.canvas_size]
        mask = (x - center) ** 2 + (y - center) ** 2 <= radius ** 2
        image = image * mask  # Apply circular mask
        
        # Apply Gaussian blur to smooth the image
        image = cv2.GaussianBlur(image, (5, 5), 1)
        
        # Generate string connections
        connections = []
        current_pin = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(self.config.num_connections):
            best_pin = current_pin
            best_score = -1
            
            # Find the best next pin (that creates the most darkness where needed)
            for next_pin in range(self.config.num_pins):
                if next_pin == current_pin:
                    continue
                    
                # Skip if this connection was used recently (avoid immediate repeats)
                if len(connections) > 0 and next_pin == connections[-1]:
                    continue
                    
                score = self._calculate_line_darkness(current_pin, next_pin, image)
                
                if score > best_score:
                    best_score = score
                    best_pin = next_pin
            
            # Add the best string
            if best_pin != current_pin:
                self._add_string(current_pin, best_pin)
                connections.append(best_pin)
                current_pin = best_pin
            
            # Update progress
            if i % 50 == 0:
                progress = (i + 1) / self.config.num_connections
                progress_bar.progress(progress)
                status_text.text(f"Generated {i + 1}/{self.config.num_connections} connections...")
        
        progress_bar.progress(1.0)
        status_text.text(f"Completed! Generated {len(connections)} connections.")
        
        return self.canvas, connections
    
    def create_visualization(self, connections: List[int]) -> Image.Image:
        """Create a visual representation of the string art"""
        # Create PIL image
        img = Image.new('RGB', (self.config.canvas_size, self.config.canvas_size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw circle outline
        center = self.config.canvas_size // 2
        radius = center - 50
        draw.ellipse([center - radius, center - radius, center + radius, center + radius], 
                    outline='black', width=2)
        
        # Draw pins
        for i, (x, y) in enumerate(self.pins):
            draw.ellipse([x - self.config.pin_radius, y - self.config.pin_radius,
                         x + self.config.pin_radius, y + self.config.pin_radius],
                        fill='red', outline='darkred')
            
        # Draw strings
        current_pin = 0
        string_color = (0, 0, 0, int(255 * self.config.string_opacity))
        
        for next_pin in connections:
            x1, y1 = self.pins[current_pin]
            x2, y2 = self.pins[next_pin]
            draw.line([(x1, y1), (x2, y2)], fill=string_color[:3], width=1)
            current_pin = next_pin
            
        return img
    
    def save_connections(self, connections: List[int], filename: str):
        """Save connections to a file"""
        # Add the starting pin (0) to make it a complete sequence
        full_sequence = [0] + connections
        
        # Save as JSON with metadata
        data = {
            'connections': full_sequence,
            'num_pins': self.config.num_pins,
            'num_connections': len(connections),
            'instructions': 'Start at pin 0, then follow the sequence. Each number represents the next pin to connect to.',
            'format': 'Continuous path - connect pin 0 to pin connections[0], then to connections[1], etc.'
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        # Also save as simple text file
        text_filename = filename.replace('.json', '.txt')
        with open(text_filename, 'w') as f:
            f.write("String Art Connection Sequence\n")
            f.write(f"Number of pins: {self.config.num_pins}\n")
            f.write(f"Number of connections: {len(connections)}\n")
            f.write("Connection sequence (start at pin 0):\n")
            f.write(", ".join(map(str, full_sequence)))
            
        return filename, text_filename
