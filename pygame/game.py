import pygame
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Deluxe")
clock = pygame.time.Clock()

# Sound effects (placeholder - replace with actual .wav files if you have them)
# To add sounds: place .wav files in same folder and uncomment these lines
try:
    shoot_sound = pygame.mixer.Sound('shoot.wav')
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    thrust_sound = pygame.mixer.Sound('thrust.wav')
    powerup_sound = pygame.mixer.Sound('powerup.wav')
except:
    # If no sound files, create dummy sounds that do nothing
    class DummySound:
        def play(self): pass
        def stop(self): pass
    shoot_sound = DummySound()
    explosion_sound = DummySound()
    thrust_sound = DummySound()
    powerup_sound = DummySound()


class Particle:
    """Small particles for visual effects"""
    def __init__(self, x, y, vx, vy, color, lifetime=30):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
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
        # Fade alpha based on lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        
        # Create a surface with per-pixel alpha
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))


class Ship:
    def __init__(self, x, y, controls='arrows', color=(255, 255, 255)):
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
        self.controls = controls  # 'arrows' or 'wasd'
        self.color = color
        
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
        # Determine which keys to use based on control scheme
        if self.controls == 'arrows':
            left, right, thrust, shoot, hyperspace = (
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, 
                pygame.K_LCTRL, pygame.K_LSHIFT
            )
        else:  # wasd
            left, right, thrust, shoot, hyperspace = (
                pygame.K_a, pygame.K_d, pygame.K_w,
                pygame.K_RCTRL, pygame.K_RSHIFT
            )
        
        if keys[left]:
            self.angle -= self.rotation_speed
        if keys[right]:
            self.angle += self.rotation_speed
        
        self.is_thrusting = False
        if keys[thrust]:
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
        
        # Hyperspace jump
        if keys[hyperspace] and self.hyperspace_cooldown <= 0:
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
            
            # Orange/yellow/red flames
            colors = [(255, 200, 0), (255, 100, 0), (255, 50, 0)]
            particles.append(Particle(back_x, back_y, particle_vx, particle_vy, 
                                    random.choice(colors), lifetime=20))
    
    def hyperspace_jump(self, particles):
        """Teleport to random location with particle effect"""
        # Create particles at old location
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particles.append(Particle(self.x, self.y, vx, vy, (0, 255, 255), lifetime=40))
        
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
            particles.append(Particle(self.x, self.y, vx, vy, (0, 255, 255), lifetime=40))
        
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
        """Draw the ship as a triangle"""
        rad = math.radians(self.angle)
        
        # Calculate triangle points
        nose_x = self.x + math.sin(rad) * self.radius
        nose_y = self.y - math.cos(rad) * self.radius
        
        left_x = self.x + math.sin(rad - 2.5) * self.radius
        left_y = self.y - math.cos(rad - 2.5) * self.radius
        
        right_x = self.x + math.sin(rad + 2.5) * self.radius
        right_y = self.y - math.cos(rad + 2.5) * self.radius
        
        # Flicker when invulnerable
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return
        
        # Draw shield
        if self.shield:
            shield_color = (0, 200, 255, 100)
            surf = pygame.Surface((self.radius * 3, self.radius * 3), pygame.SRCALPHA)
            pygame.draw.circle(surf, shield_color, (self.radius * 1.5, self.radius * 1.5), 
                             int(self.radius * 1.5), 3)
            screen.blit(surf, (int(self.x - self.radius * 1.5), 
                              int(self.y - self.radius * 1.5)))
        
        # Draw ship
        pygame.draw.polygon(screen, self.color, 
                          [(nose_x, nose_y), (left_x, left_y), (right_x, right_y)], 2)
    
    def shoot(self):
        """Create a bullet"""
        rad = math.radians(self.angle)
        
        bullet_x = self.x + math.sin(rad) * self.radius
        bullet_y = self.y - math.cos(rad) * self.radius
        
        bullet_speed = 10
        bullet_vx = self.vx + math.sin(rad) * bullet_speed
        bullet_vy = self.vy - math.cos(rad) * bullet_speed
        
        shoot_sound.play()
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
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)


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
        
        pygame.draw.polygon(screen, (150, 150, 150), points, 2)
    
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
        
        shoot_sound.play()
        return UFOBullet(self.x, self.y, vx, vy)
    
    def draw(self, screen):
        """Draw classic UFO saucer shape"""
        # Top dome
        pygame.draw.arc(screen, (255, 0, 255), 
                       (self.x - self.radius, self.y - self.radius//2, 
                        self.radius * 2, self.radius), 
                       0, math.pi, 2)
        # Bottom saucer
        pygame.draw.ellipse(screen, (255, 0, 255),
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
        pygame.draw.circle(screen, (255, 0, 255), (int(self.x), int(self.y)), self.radius)


class PowerUp:
    """Collectible power-ups"""
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type  # 'rapid_fire' or 'shield'
        self.radius = 15
        self.lifetime = 600  # Disappears after 10 seconds
        self.pulse = 0
        
        if power_type == 'rapid_fire':
            self.color = (255, 0, 0)
            self.symbol = 'R'
        else:  # shield
            self.color = (0, 200, 255)
            self.symbol = 'S'
    
    def update(self):
        self.lifetime -= 1
        self.pulse += 0.1
    
    def is_expired(self):
        return self.lifetime <= 0
    
    def draw(self, screen):
        # Pulsing effect
        pulse_size = self.radius + math.sin(self.pulse) * 3
        
        pygame.draw.circle(screen, self.color, 
                         (int(self.x), int(self.y)), int(pulse_size), 2)
        
        # Draw letter in center
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbol, True, self.color)
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


def create_explosion(x, y, particles, color=(255, 100, 0)):
    """Create particle explosion effect"""
    for _ in range(30):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        particles.append(Particle(x, y, vx, vy, color, lifetime=40))


# Game setup
ships = [
    Ship(WIDTH//2 - 50, HEIGHT//2, 'arrows', (255, 255, 255)),
    Ship(WIDTH//2 + 50, HEIGHT//2, 'wasd', (0, 255, 0))
]

asteroids = spawn_asteroids(4)
bullets = []
ufo_bullets = []
particles = []
powerups = []
ufo = None

scores = [0, 0]  # Scores for player 1 and player 2
lives = [3, 3]
wave = 1
game_over = False
multiplayer = False  # Toggle with M key

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)

# Shooting cooldown for each player
shoot_cooldowns = [0, 0]
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
            # Toggle multiplayer
            if event.key == pygame.K_m and not game_over:
                multiplayer = not multiplayer
            
            # Restart game
            if event.key == pygame.K_SPACE and game_over:
                ships = [
                    Ship(WIDTH//2 - 50, HEIGHT//2, 'arrows', (255, 255, 255)),
                    Ship(WIDTH//2 + 50, HEIGHT//2, 'wasd', (0, 255, 0))
                ]
                asteroids = spawn_asteroids(4)
                bullets = []
                ufo_bullets = []
                particles = []
                powerups = []
                ufo = None
                scores = [0, 0]
                lives = [3, 3]
                wave = 1
                game_over = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        
        # Determine active ships
        active_ships = [ships[0]]
        if multiplayer:
            active_ships.append(ships[1])
        
        # Handle ship input
        for i, ship in enumerate(active_ships):
            ship.handle_input(keys, particles)
            
            # Shooting
            shoot_key = pygame.K_LCTRL if ship.controls == 'arrows' else pygame.K_RCTRL
            delay = RAPID_FIRE_DELAY if ship.rapid_fire else SHOOT_DELAY
            
            if keys[shoot_key] and shoot_cooldowns[i] <= 0:
                bullets.append(ship.shoot())
                shoot_cooldowns[i] = delay
            
            if shoot_cooldowns[i] > 0:
                shoot_cooldowns[i] -= 1
        
        # Update ships
        for ship in active_ships:
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
            new_bullet = ufo.update(active_ships)
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
                    
                    # Determine which player shot it
                    # (In real game, bullets would track owner)
                    if multiplayer:
                        scores[0] += asteroid.points // 2
                        scores[1] += asteroid.points // 2
                    else:
                        scores[0] += asteroid.points
                    
                    # Particle explosion
                    create_explosion(asteroid.x, asteroid.y, particles)
                    explosion_sound.play()
                    
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
                    
                    scores[0] += 500  # Big points for UFO
                    if multiplayer:
                        scores[1] += 500
                    
                    create_explosion(ufo.x, ufo.y, particles, (255, 0, 255))
                    explosion_sound.play()
                    ufo = None
        
        # Check ship-asteroid collisions
        for i, ship in enumerate(active_ships):
            if ship.invulnerable or ship.shield:
                continue
            
            for asteroid in asteroids[:]:
                if asteroid.check_collision_ship(ship):
                    lives[i] -= 1
                    
                    # Explosion
                    create_explosion(ship.x, ship.y, particles, ship.color)
                    explosion_sound.play()
                    
                    # Remove asteroid
                    asteroids.remove(asteroid)
                    
                    # Reset ship
                    if ship.controls == 'arrows':
                        active_ships[i] = Ship(WIDTH//2 - 50, HEIGHT//2, 'arrows', (255, 255, 255))
                    else:
                        active_ships[i] = Ship(WIDTH//2 + 50, HEIGHT//2, 'wasd', (0, 255, 0))
                    
                    active_ships[i].invulnerable = True
                    active_ships[i].invulnerable_timer = 120  # 2 seconds
                    
                    if lives[i] <= 0:
                        if not multiplayer or all(l <= 0 for l in lives):
                            game_over = True
                    
                    break
        
        # Check UFO bullet-ship collisions
        for bullet in ufo_bullets[:]:
            for i, ship in enumerate(active_ships):
                if ship.invulnerable or ship.shield:
                    continue
                
                distance = math.sqrt((ship.x - bullet.x)**2 + (ship.y - bullet.y)**2)
                if distance < ship.radius + bullet.radius:
                    if bullet in ufo_bullets:
                        ufo_bullets.remove(bullet)
                    
                    lives[i] -= 1
                    
                    create_explosion(ship.x, ship.y, particles, ship.color)
                    explosion_sound.play()
                    
                    if ship.controls == 'arrows':
                        active_ships[i] = Ship(WIDTH//2 - 50, HEIGHT//2, 'arrows', (255, 255, 255))
                    else:
                        active_ships[i] = Ship(WIDTH//2 + 50, HEIGHT//2, 'wasd', (0, 255, 0))
                    
                    active_ships[i].invulnerable = True
                    active_ships[i].invulnerable_timer = 120
                    
                    if lives[i] <= 0:
                        if not multiplayer or all(l <= 0 for l in lives):
                            game_over = True
                    
                    break
        
        # Check ship-UFO collision
        if ufo:
            for i, ship in enumerate(active_ships):
                if ship.invulnerable or ship.shield:
                    continue
                
                if ufo.check_collision_ship(ship):
                    lives[i] -= 1
                    
                    create_explosion(ship.x, ship.y, particles, ship.color)
                    create_explosion(ufo.x, ufo.y, particles, (255, 0, 255))
                    explosion_sound.play()
                    
                    ufo = None
                    
                    if ship.controls == 'arrows':
                        active_ships[i] = Ship(WIDTH//2 - 50, HEIGHT//2, 'arrows', (255, 255, 255))
                    else:
                        active_ships[i] = Ship(WIDTH//2 + 50, HEIGHT//2, 'wasd', (0, 255, 0))
                    
                    active_ships[i].invulnerable = True
                    active_ships[i].invulnerable_timer = 120
                    
                    if lives[i] <= 0:
                        if not multiplayer or all(l <= 0 for l in lives):
                            game_over = True
                    
                    break
        
        # Check power-up collisions
        for powerup in powerups[:]:
            for i, ship in enumerate(active_ships):
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
            asteroids = spawn_asteroids(4, 'large', wave)
            
            # Update ship references
            ships[0] = active_ships[0]
            if multiplayer:
                ships[1] = active_ships[1]
    
    # Drawing
    screen.fill((0, 0, 0))
    
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
        
        # Draw ships
        active_ships = [ships[0]]
        if multiplayer:
            active_ships.append(ships[1])
        
        for ship in active_ships:
            ship.draw(screen)
        
        # Draw UI
        # Player 1 (left side)
        score_text = font.render(f'P1: {scores[0]}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f'Lives: {lives[0]}', True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        
        # Wave
        wave_text = font.render(f'Wave: {wave}', True, (255, 255, 255))
        screen.blit(wave_text, (WIDTH//2 - 70, 10))
        
        # Player 2 (right side) if multiplayer
        if multiplayer:
            p2_score = font.render(f'P2: {scores[1]}', True, (0, 255, 0))
            screen.blit(p2_score, (WIDTH - 150, 10))
            
            p2_lives = font.render(f'Lives: {lives[1]}', True, (0, 255, 0))
            screen.blit(p2_lives, (WIDTH - 150, 50))
        
        # Power-up indicators
        if ships[0].rapid_fire or (multiplayer and ships[1].rapid_fire):
            rapid_text = small_font.render('RAPID FIRE!', True, (255, 0, 0))
            screen.blit(rapid_text, (WIDTH//2 - 60, 50))
        
        if ships[0].shield or (multiplayer and ships[1].shield):
            shield_text = small_font.render('SHIELD!', True, (0, 200, 255))
            screen.blit(shield_text, (WIDTH//2 - 40, 75))
        
        # Controls
        if multiplayer:
            controls = small_font.render('P1: Arrows+LCtrl+LShift | P2: WASD+RCtrl+RShift | M:Toggle', 
                                       True, (100, 100, 100))
        else:
            controls = small_font.render('Arrows: Move | LCtrl: Shoot | LShift: Hyperspace | M: Multiplayer', 
                                       True, (100, 100, 100))
        screen.blit(controls, (10, HEIGHT - 30))
    
    else:
        # Game over screen
        game_over_text = large_font.render('GAME OVER', True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 100))
        
        if multiplayer:
            if scores[0] > scores[1]:
                winner_text = font.render('Player 1 Wins!', True, (255, 255, 255))
            elif scores[1] > scores[0]:
                winner_text = font.render('Player 2 Wins!', True, (0, 255, 0))
            else:
                winner_text = font.render('Tie!', True, (255, 255, 0))
            screen.blit(winner_text, (WIDTH//2 - 100, HEIGHT//2 - 30))
            
            p1_final = font.render(f'P1 Score: {scores[0]}', True, (255, 255, 255))
            screen.blit(p1_final, (WIDTH//2 - 120, HEIGHT//2 + 20))
            
            p2_final = font.render(f'P2 Score: {scores[1]}', True, (0, 255, 0))
            screen.blit(p2_final, (WIDTH//2 - 120, HEIGHT//2 + 60))
        else:
            final_score = font.render(f'Final Score: {scores[0]}', True, (255, 255, 255))
            screen.blit(final_score, (WIDTH//2 - 140, HEIGHT//2))
            
            final_wave = font.render(f'Wave Reached: {wave}', True, (255, 255, 255))
            screen.blit(final_wave, (WIDTH//2 - 140, HEIGHT//2 + 50))
        
        restart_text = font.render('Press SPACE to restart', True, (150, 150, 150))
        screen.blit(restart_text, (WIDTH//2 - 170, HEIGHT//2 + 120))
    
    pygame.display.flip()

pygame.quit()