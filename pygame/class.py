import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Collector")
clock = pygame.time.Clock()

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        # Random color for visual variety
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    
    def update(self):
        # Move the circle
        self.x += self.vx
        self.y += self.vy
        
        # Wrap around screen edges (Pac-Man style)
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 2)
    
    def check_collision(self, other):
        """Check if this circle collides with another circle"""
        distance = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return distance < self.radius + other.radius


class Player(Circle):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.vx = 0  # No random velocity
        self.vy = 0
        self.speed = 5
        self.color = (0, 255, 0)  # Green for player
    
    def handle_input(self):
        """Handle keyboard input for player movement"""
        keys = pygame.key.get_pressed()
        self.vx = 0
        self.vy = 0
        
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed
        if keys[pygame.K_UP]:
            self.vy = -self.speed
        if keys[pygame.K_DOWN]:
            self.vy = self.speed
    
    def update(self):
        """Update player position with boundary checking"""
        self.x += self.vx
        self.y += self.vy
        
        # Keep player within screen bounds (no wrapping)
        if self.x < self.radius:
            self.x = self.radius
        elif self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
        
        if self.y < self.radius:
            self.y = self.radius
        elif self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
    
    def draw(self, screen):
        """Draw player as filled circle"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# Create player
player = Player(WIDTH//2, HEIGHT//2, 25)

# Create initial circles
circles = [
    Circle(100, 100, 40),
    Circle(400, 300, 30),
    Circle(600, 200, 50),
    Circle(200, 500, 35)
]

# Score tracking
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Spawn new circle on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            new_circle = Circle(x, y, random.randint(20, 50))
            circles.append(new_circle)
    
    # Handle player input
    player.handle_input()
    player.update()
    
    # Update all circles
    for circle in circles:
        circle.update()
    
    # Check collisions between player and circles
    for circle in circles[:]:  # [:] creates a copy to safely remove items
        if player.check_collision(circle):
            circles.remove(circle)
            score += 1
    
    # Draw everything
    screen.fill((0, 0, 0))
    
    # Draw all circles
    for circle in circles:
        circle.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # Draw instructions
    instructions = font.render('Click to spawn | Arrows to move', True, (150, 150, 150))
    screen.blit(instructions, (WIDTH//2 - 250, HEIGHT - 40))
    
    pygame.display.flip()

pygame.quit()