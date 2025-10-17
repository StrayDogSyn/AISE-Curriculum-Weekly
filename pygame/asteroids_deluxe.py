import pygame
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 1200, 900  # Increased by 150%
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Deluxe")
clock = pygame.time.Clock()

# Fullscreen state
fullscreen = False

# Color Schemes - Matrix terminal vibes
class ColorScheme:
    """Different terminal color schemes"""
    def __init__(self, name, bg, primary, secondary, accent, dim, bright):
        self.name = name
        self.bg = bg              # Background
        self.primary = primary    # Main color (ships, asteroids)
        self.secondary = secondary # Secondary elements
        self.accent = accent      # Highlights (bullets, explosions)
        self.dim = dim           # Dimmed text/UI
        self.bright = bright     # Bright highlights
        
# Available color schemes
SCHEMES = [
    ColorScheme("MATRIX", (0, 10, 0), (0, 255, 70), (0, 200, 50), (0, 255, 150), (0, 100, 30), (150, 255, 150)),
    ColorScheme("AMBER TERMINAL", (10, 5, 0), (255, 176, 0), (200, 140, 0), (255, 200, 50), (100, 70, 0), (255, 220, 100)),
    ColorScheme("GREEN PHOSPHOR", (0, 5, 0), (51, 255, 51), (30, 200, 30), (100, 255, 100), (20, 100, 20), (200, 255, 200)),
    ColorScheme("BLUE TERMINAL", (0, 0, 10), (100, 200, 255), (50, 150, 255), (150, 220, 255), (30, 80, 120), (200, 230, 255)),
    ColorScheme("RED ALERT", (10, 0, 0), (255, 50, 50), (200, 30, 30), (255, 100, 100), (100, 20, 20), (255, 150, 150)),
    ColorScheme("CLASSIC", (0, 0, 0), (255, 255, 255), (200, 200, 200), (255, 255, 100), (100, 100, 100), (255, 255, 255)),
    ColorScheme("CYAN TERM", (0, 10, 10), (0, 255, 255), (0, 200, 200), (100, 255, 255), (0, 100, 100), (150, 255, 255)),
]

current_scheme_index = 0
current_scheme = SCHEMES[current_scheme_index]

# Sound effects - load from /sounds directory
try:
    # Laser sounds - we'll cycle through these
    laser_sounds = [
        pygame.mixer.Sound('pygame/sounds/retro-laser-shot-04.wav'),
        pygame.mixer.Sound('pygame/sounds/retro-laser-shot-05.wav'),
        pygame.mixer.Sound('pygame/sounds/retro-laser-shot-06.wav'),
        pygame.mixer.Sound('pygame/sounds/puny_laser.wav'),
    ]
    current_laser_index = 0

    # Big laser for UFO - try laser-element or fallback to first retro laser
    try:
        ufo_laser_sound = pygame.mixer.Sound('pygame/sounds/laser-element-only-2.wav')
    except:
        ufo_laser_sound = laser_sounds[0]  # Fallback to a regular laser

    # Explosion sounds - randomize for variety
    explosion_sounds = [
        pygame.mixer.Sound('pygame/sounds/explosion_asteroid.wav'),
        pygame.mixer.Sound('pygame/sounds/explosion_asteroid2.wav'),
        pygame.mixer.Sound('pygame/sounds/space-explosion.wav'),
        pygame.mixer.Sound('pygame/sounds/pelicula-sfx.wav'),
    ]

    # Achievement/Level up sounds
    achievement_sounds = [
        pygame.mixer.Sound('pygame/sounds/achievement.wav'),
        pygame.mixer.Sound('pygame/sounds/jingle_achievement_00.wav'),
        pygame.mixer.Sound('pygame/sounds/jingle_achievement_01.wav'),
    ]

    # Level up sounds - NOTE: These are MP3 files!
    # pygame.mixer.Sound works with mp3 on most systems
    level_up_sounds = [
        pygame.mixer.Sound('pygame/sounds/level-up-01.mp3'),
        pygame.mixer.Sound('pygame/sounds/level-up-02.mp3'),
        pygame.mixer.Sound('pygame/sounds/level-up-03.mp3'),
    ]

    # Power-up/special sounds
    powerup_sound = pygame.mixer.Sound('pygame/sounds/magic-reveal.wav')
    
    # Adjust volumes for balance
    for sound in laser_sounds:
        sound.set_volume(0.3)
    ufo_laser_sound.set_volume(0.4)
    for sound in explosion_sounds:
        sound.set_volume(0.5)
    for sound in achievement_sounds:
        sound.set_volume(0.6)
    for sound in level_up_sounds:
        sound.set_volume(0.6)
    powerup_sound.set_volume(0.5)
    
    sounds_loaded = True
    print("✓ All sound effects loaded successfully!")
    
except Exception as e:
    print(f"⚠ Could not load sounds: {e}")
    print("⚠ Game will run without sound effects")
    
    # Create dummy sounds that do nothing
    class DummySound:
        def play(self): pass
        def stop(self): pass
        def set_volume(self, vol): pass
    
    laser_sounds = [DummySound() for _ in range(4)]
    current_laser_index = 0
    ufo_laser_sound = DummySound()
    explosion_sounds = [DummySound() for _ in range(4)]
    achievement_sounds = [DummySound() for _ in range(3)]
    level_up_sounds = [DummySound() for _ in range(3)]
    powerup_sound = DummySound()
    sounds_loaded = False


def play_laser_sound():
    """Cycle through laser sounds for variety"""
    global current_laser_index
    laser_sounds[current_laser_index].play()
    current_laser_index = (current_laser_index + 1) % len(laser_sounds)


def play_explosion_sound():
    """Play random explosion sound"""
    random.choice(explosion_sounds).play()


def play_achievement_sound():
    """Play random achievement sound"""
    random.choice(achievement_sounds).play()


def play_level_up_sound():
    """Play random level up sound"""
    random.choice(level_up_sounds).play()


class Particle:
    """Small particles for visual effects"""
    def __init__(self, x, y, vx, vy, color_type='accent', lifetime=30):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color_type = color_type  # 'accent', 'primary', 'secondary', 'bright'
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 4)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # Fade out as lifetime decreases
        self.vx *= 0.98
        self.vy *= 0.98
    
    def is_expired(self):
        return self.lifetime <= 0
    
    def draw(self, screen):
        # Get color from current scheme
        if self.color_type == 'accent':
            color = current_scheme.accent
        elif self.color_type == 'primary':
            color = current_scheme.primary
        elif self.color_type == 'bright':
            color = current_scheme.bright
        else:
            color = current_scheme.secondary
        
        # Fade alpha based on lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*color, alpha)
        
        # Create a surface with per-pixel alpha
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vx = 0
        self.vy = 0
        self.rotation_speed = 5
        self.thrust_power = 0.2
        self.max_speed = 8
        self.friction = 0.99
        self.radius = 15
        
        # Power-ups
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.shield = False
        self.shield_timer = 0
        
        # Invulnerability after respawn
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Hyperspace cooldown
        self.hyperspace_cooldown = 0
        
        self.is_thrusting = False
    
    def handle_input(self, keys, particles):
        """Handle rotation, thrust, and special abilities"""
        # Arrow key controls
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed

        self.is_thrusting = False
        if keys[pygame.K_UP]:
            self.is_thrusting = True
            # Thrust in the direction we're facing
            rad = math.radians(self.angle)
            self.vx += math.sin(rad) * self.thrust_power
            self.vy -= math.cos(rad) * self.thrust_power

            # Cap max speed
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > self.max_speed:
                self.vx = (self.vx / speed) * self.max_speed
                self.vy = (self.vy / speed) * self.max_speed

            # Spawn thrust particles
            self.spawn_thrust_particles(particles)

        # Hyperspace jump (LSHIFT)
        if keys[pygame.K_LSHIFT] and self.hyperspace_cooldown <= 0:
            self.hyperspace_jump(particles)
            self.hyperspace_cooldown = 180  # 3 seconds
    
    def spawn_thrust_particles(self, particles):
        """Create particles behind the ship when thrusting"""
        if random.random() < 0.5:  # Don't spawn every frame
            rad = math.radians(self.angle)
            # Position particles at the back of the ship
            back_x = self.x - math.sin(rad) * self.radius
            back_y = self.y + math.cos(rad) * self.radius
            
            # Particles move opposite to thrust direction
            particle_vx = self.vx - math.sin(rad) * 3 + random.uniform(-1, 1)
            particle_vy = self.vy + math.cos(rad) * 3 + random.uniform(-1, 1)
            
            # Use accent color for thrust
            particles.append(Particle(back_x, back_y, particle_vx, particle_vy, 
                                    'accent', lifetime=20))
    
    def hyperspace_jump(self, particles):
        """Teleport to random location with particle effect"""
        # Create particles at old location
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particles.append(Particle(self.x, self.y, vx, vy, 'bright', lifetime=40))
        
        # Teleport to random position
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.vx = 0
        self.vy = 0
        
        # Create particles at new location
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particles.append(Particle(self.x, self.y, vx, vy, 'bright', lifetime=40))
        
        # Small chance of telefragging yourself into an asteroid (risk!)
        # Handled by collision detection
    
    def update(self):
        """Apply velocity and friction"""
        self.vx *= self.friction
        self.vy *= self.friction
        
        self.x += self.vx
        self.y += self.vy
        
        # Wrap around screen
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
        
        # Update timers
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                self.rapid_fire = False
        
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer == 0:
                self.invulnerable = False
        
        if self.hyperspace_cooldown > 0:
            self.hyperspace_cooldown -= 1
    
    def draw(self, screen):
        """Draw the ship as a teardrop"""
        rad = math.radians(self.angle)
        
        # Flicker when invulnerable
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return
        
        # Draw shield
        if self.shield:
            shield_color = (*current_scheme.bright, 100)
            surf = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
            pygame.draw.circle(surf, shield_color, (self.radius * 1.5, self.radius * 1.5),
                             int(self.radius * 1.5), 3)
            screen.blit(surf, (int(self.x - self.radius * 1.5),
                              int(self.y - self.radius * 1.5)))

        # Use primary color for ship
        ship_color = current_scheme.primary
        
        # Create teardrop shape - pointed front, rounded back
        # Define points around the teardrop in local coordinates
        teardrop_points = []
        
        # Front point (sharp nose)
        nose_length = self.radius * 1.2
        
        # Create smooth teardrop using multiple points
        num_points = 12
        for i in range(num_points):
            # Angle around the back of the ship (from -150° to +150°)
            angle_offset = math.pi * (i / (num_points - 1) - 0.5) * 1.67  # 1.67 gives us about 300°
            
            # Distance from center - creates the teardrop curve
            # More distance at the back (angle_offset near 0), less at sides
            curve_factor = abs(math.cos(angle_offset * 0.8))
            distance = self.radius * 0.7 * (0.4 + 0.6 * curve_factor)
            
            # Calculate point in local coordinates (before rotation)
            local_x = math.sin(angle_offset) * distance
            local_y = -math.cos(angle_offset) * distance * 0.6  # Squash vertically
            
            # Rotate point based on ship's angle
            rotated_x = local_x * math.cos(rad) - local_y * math.sin(rad)
            rotated_y = local_x * math.sin(rad) + local_y * math.cos(rad)
            
            # Translate to ship position
            teardrop_points.append((self.x + rotated_x, self.y + rotated_y))
        
        # Add the nose point at the front
        nose_x = self.x + math.sin(rad) * nose_length
        nose_y = self.y - math.cos(rad) * nose_length
        teardrop_points.insert(num_points // 2, (nose_x, nose_y))
        
        # Draw the teardrop
        pygame.draw.polygon(screen, ship_color, teardrop_points, 2)
        
        # Optional: Add a small thruster detail at the back when thrusting
        if self.is_thrusting:
            back_x = self.x - math.sin(rad) * self.radius * 0.5
            back_y = self.y + math.cos(rad) * self.radius * 0.5
            pygame.draw.circle(screen, current_scheme.accent, (int(back_x), int(back_y)), 3)
    
    def shoot(self):
        """Create a bullet"""
        rad = math.radians(self.angle)
        
        bullet_x = self.x + math.sin(rad) * self.radius
        bullet_y = self.y - math.cos(rad) * self.radius
        
        bullet_speed = 10
        bullet_vx = self.vx + math.sin(rad) * bullet_speed
        bullet_vy = self.vy - math.cos(rad) * bullet_speed
        
        play_laser_sound()  # Cycle through different laser sounds
        return Bullet(bullet_x, bullet_y, bullet_vx, bullet_vy)


class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 3
        self.lifetime = 60
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # Wrap around screen
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
    
    def is_expired(self):
        return self.lifetime <= 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, current_scheme.accent, (int(self.x), int(self.y)), self.radius)


class Asteroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        
        if size == 'large':
            self.radius = 40
            self.points = 20
        elif size == 'medium':
            self.radius = 25
            self.points = 50
        else:  # small
            self.radius = 15
            self.points = 100
        
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        
        # Prevent barely-moving asteroids
        if abs(self.vx) < 0.5:
            self.vx = 1 if self.vx >= 0 else -1
        if abs(self.vy) < 0.5:
            self.vy = 1 if self.vy >= 0 else -1
        
        # Create irregular polygon shape
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        self.create_polygon()
    
    def create_polygon(self):
        """Generate an irregular polygon for this asteroid"""
        num_points = random.randint(8, 12)
        self.polygon = []
        
        for i in range(num_points):
            angle = (360 / num_points) * i + random.uniform(-15, 15)
            distance = self.radius + random.uniform(-self.radius * 0.3, self.radius * 0.2)
            
            rad = math.radians(angle)
            px = math.cos(rad) * distance
            py = math.sin(rad) * distance
            self.polygon.append((px, py))
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        
        # Wrap around screen
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
    
    def draw(self, screen):
        """Draw as irregular polygon"""
        rad = math.radians(self.rotation)
        
        # Rotate and translate polygon points
        points = []
        for px, py in self.polygon:
            # Rotate
            rotated_x = px * math.cos(rad) - py * math.sin(rad)
            rotated_y = px * math.sin(rad) + py * math.cos(rad)
            
            # Translate to asteroid position
            points.append((self.x + rotated_x, self.y + rotated_y))
        
        pygame.draw.polygon(screen, current_scheme.secondary, points, 2)
    
    def split(self):
        """Create smaller asteroids"""
        new_asteroids = []
        
        if self.size == 'large':
            for _ in range(2):
                new_asteroids.append(Asteroid(self.x, self.y, 'medium'))
        elif self.size == 'medium':
            for _ in range(2):
                new_asteroids.append(Asteroid(self.x, self.y, 'small'))
        
        return new_asteroids
    
    def check_collision_bullet(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        return distance < self.radius + bullet.radius
    
    def check_collision_ship(self, ship):
        distance = math.sqrt((self.x - ship.x)**2 + (self.y - ship.y)**2)
        return distance < self.radius + ship.radius


class UFO:
    """Enemy UFO that tracks and shoots at players"""
    def __init__(self):
        # Spawn from edge of screen
        side = random.choice(['left', 'right'])
        if side == 'left':
            self.x = -20
            self.vx = random.uniform(1, 2)
        else:
            self.x = WIDTH + 20
            self.vx = random.uniform(-2, -1)
        
        self.y = random.randint(100, HEIGHT - 100)
        self.vy = random.uniform(-1, 1)
        self.radius = 20
        self.shoot_cooldown = 0
        self.shoot_delay = 90  # Shoots every 1.5 seconds
    
    def update(self, ships):
        """Move and shoot at nearest player"""
        self.x += self.vx
        self.y += self.vy
        
        # Gentle vertical wobble
        self.vy += random.uniform(-0.1, 0.1)
        self.vy = max(-2, min(2, self.vy))
        
        # Remove if off screen
        if self.x < -50 or self.x > WIDTH + 50:
            return None
        
        self.shoot_cooldown -= 1
        
        # Shoot at nearest player
        if self.shoot_cooldown <= 0 and ships:
            nearest_ship = min(ships, key=lambda s: 
                             math.sqrt((s.x - self.x)**2 + (s.y - self.y)**2))
            
            bullet = self.shoot_at(nearest_ship)
            self.shoot_cooldown = self.shoot_delay
            return bullet
        
        return None
    
    def shoot_at(self, target):
        """Shoot in the general direction of target (not perfect aim)"""
        dx = target.x - self.x
        dy = target.y - self.y
        angle = math.atan2(dy, dx)
        
        # Add some inaccuracy
        angle += random.uniform(-0.3, 0.3)
        
        speed = 5
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        
        ufo_laser_sound.play()  # Distinctive UFO laser sound
        return UFOBullet(self.x, self.y, vx, vy)
    
    def draw(self, screen):
        """Draw classic UFO saucer shape"""
        # Use bright color for UFO to make it stand out as dangerous
        ufo_color = current_scheme.bright
        
        # Top dome
        pygame.draw.arc(screen, ufo_color, 
                       (self.x - self.radius, self.y - self.radius//2, 
                        self.radius * 2, self.radius), 
                       0, math.pi, 2)
        # Bottom saucer
        pygame.draw.ellipse(screen, ufo_color,
                          (self.x - self.radius, self.y - 5,
                           self.radius * 2, 10), 2)
    
    def check_collision_bullet(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        return distance < self.radius + bullet.radius
    
    def check_collision_ship(self, ship):
        distance = math.sqrt((self.x - ship.x)**2 + (self.y - ship.y)**2)
        return distance < self.radius + ship.radius


class UFOBullet(Bullet):
    """UFO bullets look different"""
    def draw(self, screen):
        pygame.draw.circle(screen, current_scheme.bright, (int(self.x), int(self.y)), self.radius)


class PowerUp:
    """Collectible power-ups"""
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type  # 'rapid_fire' or 'shield'
        self.radius = 15
        self.lifetime = 600  # Disappears after 10 seconds
        self.pulse = 0
        
        # Power-ups keep distinct colors but use scheme's bright for visibility
        if power_type == 'rapid_fire':
            self.symbol = 'R'
        else:  # shield
            self.symbol = 'S'
    
    def update(self):
        self.lifetime -= 1
        self.pulse += 0.1
    
    def is_expired(self):
        return self.lifetime <= 0
    
    def draw(self, screen):
        # Pulsing effect
        pulse_size = self.radius + math.sin(self.pulse) * 3
        
        # Use accent color for power-ups
        color = current_scheme.accent
        
        pygame.draw.circle(screen, color, 
                         (int(self.x), int(self.y)), int(pulse_size), 2)
        
        # Draw letter in center
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbol, True, color)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)
    
    def check_collision_ship(self, ship):
        distance = math.sqrt((self.x - ship.x)**2 + (self.y - ship.y)**2)
        return distance < self.radius + ship.radius


def spawn_asteroids(count, size='large', wave=1):
    """Create asteroids, more on higher waves"""
    asteroids = []
    actual_count = count + (wave - 1)  # Add more asteroids each wave
    
    for _ in range(actual_count):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            
            # Don't spawn near center
            if abs(x - WIDTH//2) > 150 or abs(y - HEIGHT//2) > 150:
                asteroids.append(Asteroid(x, y, size))
                break
    
    return asteroids


def draw_grid_background(screen):
    """Draw matrix-style grid background"""
    grid_color = (*current_scheme.dim, 30)  # Very transparent
    
    # Vertical lines
    for x in range(0, WIDTH, 40):
        surf = pygame.Surface((1, HEIGHT), pygame.SRCALPHA)
        surf.fill(grid_color)
        screen.blit(surf, (x, 0))
    
    # Horizontal lines
    for y in range(0, HEIGHT, 40):
        surf = pygame.Surface((WIDTH, 1), pygame.SRCALPHA)
        surf.fill(grid_color)
        screen.blit(surf, (0, y))


def draw_scanlines(screen):
    """Draw CRT scanline effect"""
    scanline_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for y in range(0, HEIGHT, 2):
        pygame.draw.line(scanline_surf, (0, 0, 0, 30), (0, y), (WIDTH, y), 1)
    
    screen.blit(scanline_surf, (0, 0))


def draw_vignette(screen):
    """Draw dark edges like an old monitor"""
    vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Draw a radial gradient effect
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    # Create corner darkening
    for i in range(4):
        size = max(WIDTH, HEIGHT) // 2
        alpha = 80
        corner_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(corner_surf, (0, 0, 0, alpha), (0, 0, size, size))
        
        if i == 0:  # Top left
            screen.blit(corner_surf, (0, 0))
        elif i == 1:  # Top right
            screen.blit(pygame.transform.flip(corner_surf, True, False), (WIDTH - size, 0))
        elif i == 2:  # Bottom left
            screen.blit(pygame.transform.flip(corner_surf, False, True), (0, HEIGHT - size))
        else:  # Bottom right
            screen.blit(pygame.transform.flip(corner_surf, True, True), (WIDTH - size, HEIGHT - size))


def cycle_color_scheme():
    """Cycle to next color scheme"""
    global current_scheme_index, current_scheme
    current_scheme_index = (current_scheme_index + 1) % len(SCHEMES)
    current_scheme = SCHEMES[current_scheme_index]


def create_explosion(x, y, particles, color_type='accent'):
    """Create particle explosion effect"""
    for _ in range(30):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        particles.append(Particle(x, y, vx, vy, color_type, lifetime=40))


# Game setup
ship = Ship(WIDTH//2, HEIGHT//2)

asteroids = spawn_asteroids(4)
bullets = []
ufo_bullets = []
particles = []
powerups = []
ufo = None

score = 0
lives = 3
wave = 1
game_over = False

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)

# Shooting cooldown
shoot_cooldown = 0
SHOOT_DELAY = 10
RAPID_FIRE_DELAY = 5

# UFO spawn timer
ufo_spawn_timer = 0
UFO_SPAWN_DELAY = 600  # Every 10 seconds

# Game loop
running = True
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Cycle color schemes
            if event.key == pygame.K_c and not game_over:
                cycle_color_scheme()

            # Toggle fullscreen
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

            # Restart game
            if event.key == pygame.K_SPACE and game_over:
                ship = Ship(WIDTH//2, HEIGHT//2)
                asteroids = spawn_asteroids(4)
                bullets = []
                ufo_bullets = []
                particles = []
                powerups = []
                ufo = None
                score = 0
                lives = 3
                wave = 1
                game_over = False
    
    if not game_over:
        keys = pygame.key.get_pressed()

        # Handle ship input
        ship.handle_input(keys, particles)

        # Shooting (LCTRL)
        delay = RAPID_FIRE_DELAY if ship.rapid_fire else SHOOT_DELAY

        if keys[pygame.K_LCTRL] and shoot_cooldown <= 0:
            bullets.append(ship.shoot())
            shoot_cooldown = delay

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # Update ship
        ship.update()
        
        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.is_expired():
                particles.remove(particle)
        
        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.is_expired():
                bullets.remove(bullet)
        
        for bullet in ufo_bullets[:]:
            bullet.update()
            if bullet.is_expired():
                ufo_bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in asteroids:
            asteroid.update()
        
        # Update UFO
        if ufo:
            new_bullet = ufo.update([ship])
            if new_bullet:
                ufo_bullets.append(new_bullet)
            
            # Remove UFO if off screen
            if ufo.x < -50 or ufo.x > WIDTH + 50:
                ufo = None
        
        # Spawn UFO periodically
        ufo_spawn_timer += 1
        if ufo_spawn_timer >= UFO_SPAWN_DELAY and not ufo:
            ufo = UFO()
            ufo_spawn_timer = 0
        
        # Update power-ups
        for powerup in powerups[:]:
            powerup.update()
            if powerup.is_expired():
                powerups.remove(powerup)
        
        # Check bullet-asteroid collisions
        for bullet in bullets[:]:
            hit = False
            for asteroid in asteroids[:]:
                if asteroid.check_collision_bullet(bullet):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += asteroid.points
                    
                    # Particle explosion
                    create_explosion(asteroid.x, asteroid.y, particles)
                    play_explosion_sound()  # Random explosion variety
                    
                    # Split asteroid
                    new_asteroids = asteroid.split()
                    asteroids.remove(asteroid)
                    asteroids.extend(new_asteroids)
                    
                    # Chance to spawn power-up from destroyed asteroid
                    if random.random() < 0.1:  # 10% chance
                        power_type = random.choice(['rapid_fire', 'shield'])
                        powerups.append(PowerUp(asteroid.x, asteroid.y, power_type))
                    
                    hit = True
                    break
            
            # Check bullet-UFO collision
            if not hit and ufo:
                if ufo.check_collision_bullet(bullet):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += 500  # Big points for UFO

                    create_explosion(ufo.x, ufo.y, particles, 'bright')
                    play_explosion_sound()  # Big explosion
                    play_achievement_sound()  # Bonus achievement sound for high value target!
                    ufo = None
        
        # Check ship-asteroid collisions
        if not ship.invulnerable and not ship.shield:
            for asteroid in asteroids[:]:
                if asteroid.check_collision_ship(ship):
                    lives -= 1

                    # Explosion
                    create_explosion(ship.x, ship.y, particles, 'accent')
                    play_explosion_sound()  # Ship destruction

                    # Remove asteroid
                    asteroids.remove(asteroid)

                    # Reset ship
                    ship = Ship(WIDTH//2, HEIGHT//2)
                    ship.invulnerable = True
                    ship.invulnerable_timer = 120  # 2 seconds

                    if lives <= 0:
                        game_over = True

                    break
        
        # Check UFO bullet-ship collisions
        if not ship.invulnerable and not ship.shield:
            for bullet in ufo_bullets[:]:
                distance = math.sqrt((ship.x - bullet.x)**2 + (ship.y - bullet.y)**2)
                if distance < ship.radius + bullet.radius:
                    if bullet in ufo_bullets:
                        ufo_bullets.remove(bullet)

                    lives -= 1

                    create_explosion(ship.x, ship.y, particles, 'accent')
                    play_explosion_sound()  # Ship hit by UFO

                    ship = Ship(WIDTH//2, HEIGHT//2)
                    ship.invulnerable = True
                    ship.invulnerable_timer = 120

                    if lives <= 0:
                        game_over = True

                    break
        
        # Check ship-UFO collision
        if ufo and not ship.invulnerable and not ship.shield:
            if ufo.check_collision_ship(ship):
                lives -= 1

                create_explosion(ship.x, ship.y, particles, 'accent')
                create_explosion(ufo.x, ufo.y, particles, 'bright')
                play_explosion_sound()  # Double explosion - mutual destruction!
                play_explosion_sound()  # Play twice for dramatic effect

                ufo = None

                ship = Ship(WIDTH//2, HEIGHT//2)
                ship.invulnerable = True
                ship.invulnerable_timer = 120

                if lives <= 0:
                    game_over = True
        
        # Check power-up collisions
        for powerup in powerups[:]:
            if powerup.check_collision_ship(ship):
                powerups.remove(powerup)
                powerup_sound.play()

                if powerup.power_type == 'rapid_fire':
                    ship.rapid_fire = True
                    ship.rapid_fire_timer = 300  # 5 seconds
                else:  # shield
                    ship.shield = True
                    ship.shield_timer = 300

                break
        
        # New wave when all asteroids cleared
        if len(asteroids) == 0:
            wave += 1
            play_level_up_sound()  # Celebrate wave completion!
            asteroids = spawn_asteroids(4, 'large', wave)
    
    # Drawing
    screen.fill(current_scheme.bg)
    
    # Draw terminal effects
    draw_grid_background(screen)
    
    if not game_over:
        # Draw particles first (background layer)
        for particle in particles:
            particle.draw(screen)
        
        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)
        
        # Draw UFO
        if ufo:
            ufo.draw(screen)
        
        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        for bullet in ufo_bullets:
            bullet.draw(screen)
        
        # Draw power-ups
        for powerup in powerups:
            powerup.draw(screen)

        # Draw ship
        ship.draw(screen)
        
        # Draw scanlines and vignette
        draw_scanlines(screen)
        draw_vignette(screen)
        
        # Draw UI
        score_text = font.render(f'Score: {score}', True, current_scheme.primary)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f'Lives: {lives}', True, current_scheme.primary)
        screen.blit(lives_text, (10, 50))

        # Wave
        wave_text = font.render(f'Wave: {wave}', True, current_scheme.primary)
        screen.blit(wave_text, (WIDTH//2 - 70, 10))

        # Color scheme name
        scheme_text = small_font.render(f'{current_scheme.name}', True, current_scheme.dim)
        screen.blit(scheme_text, (WIDTH//2 - 70, 50))

        # Power-up indicators
        if ship.rapid_fire:
            rapid_text = small_font.render('RAPID FIRE!', True, current_scheme.accent)
            screen.blit(rapid_text, (WIDTH//2 - 60, 75))

        if ship.shield:
            shield_text = small_font.render('SHIELD!', True, current_scheme.accent)
            screen.blit(shield_text, (WIDTH//2 - 40, 100))

        # Controls
        controls = small_font.render('Arrows: Move | LCtrl: Shoot | LShift: Warp | C: Color | F11: Fullscreen',
                                   True, current_scheme.dim)
        screen.blit(controls, (10, HEIGHT - 30))
    
    else:
        # Game over screen
        draw_scanlines(screen)
        draw_vignette(screen)

        game_over_text = large_font.render('GAME OVER', True, current_scheme.accent)
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 100))

        final_score = font.render(f'Final Score: {score}', True, current_scheme.primary)
        screen.blit(final_score, (WIDTH//2 - 140, HEIGHT//2))

        final_wave = font.render(f'Wave Reached: {wave}', True, current_scheme.primary)
        screen.blit(final_wave, (WIDTH//2 - 140, HEIGHT//2 + 50))

        restart_text = font.render('Press SPACE to restart', True, current_scheme.dim)
        screen.blit(restart_text, (WIDTH//2 - 170, HEIGHT//2 + 120))
    
    pygame.display.flip()

pygame.quit()