# Import the necessary libraries
import pygame  # Pygame for game development (graphics, sound, etc.)
import os  # OS module for file path handling        
import random  # for random number generation
import cv2  # for video manipulation


# Load and set the game icon
icon_path = os.path.join("assets", "ship1.png")  # Path to your icon image
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)

# Initialize pygame's font and mixer `modules`
pygame.font.init()  # Initialize the font module for text rendering
pygame.mixer.init()  # Initialize the mixer module for sound playback

# Set up the display window dimensions
WIDTH, HEIGHT = 1000, 650  # Define window width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a pygame window with the defined dimensions
pygame.display.set_caption("Space Diddler")  # Set the title of the game window

# Load video files using OpenCV
game_video_path = os.path.join("assets", "background_video3.mp4")  # Define path to the game background video
menu_video_path = os.path.join("assets", "background_video3.mp4")  # Define path to the menu background video

# Capture the videos for gameplay and menu background
game_cap = cv2.VideoCapture(game_video_path)  # Load game video
menu_cap = cv2.VideoCapture(menu_video_path)  # Load menu video

# Load sound effects and music
LASER_HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "laserhit.wav"))  # Sound for laser hit
SPECIAL_ATTACK_SOUND = pygame.mixer.Sound(os.path.join("assets", "specialLaser.wav"))  # Sound for special attack
MENU_MUSIC = os.path.join("assets", "menuMusic.wav")  # Background music for menu
GAME_MUSIC = os.path.join("assets", "FrierentheSlayer.wav")  # Background music for game (same as menu)

# Function to retrieve frames from a video
def get_video_frame(cap, skip_frames=1):
    """Extract a frame from the video and convert it to a pygame surface."""
    for _ in range(skip_frames):  # Skip frames to control playback speed
        ret, frame = cap.read()  # Read a frame from the video
        if not ret:  # If no frame is returned (end of video), reset to the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to the first frame
            ret, frame = cap.read()  # Read the first frame again

    # Resize the frame to fit the game window
    frame = cv2.resize(frame, (WIDTH, HEIGHT))  # Resize the video frame to window size
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame from BGR to RGB
    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))  # Create pygame surface from the frame

    return frame_surface  # Return the pygame surface
    

# Function to apply a color tint to an image
def tint_image(image, tint_color):
    tinted_image = image.copy()  # Create a copy of the original image
    tint_surface = pygame.Surface(tinted_image.get_size(), pygame.SRCALPHA)  # Create a transparent surface
    tint_surface.fill((*tint_color, 100))  # Fill the surface with the tint color and opacity
    tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Apply the tint to the image
    return tinted_image  # Return the tinted image

# Function to display the main menu
def main_menu():
    menu_font = pygame.font.SysFont("comicsans", 70)  # Font for the main title
    controls_font = pygame.font.SysFont("comicsans", 40)  # Font for the controls text
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    FPS = 60  # Set the frame rate to 60 FPS

    # Play the menu music in loop
    pygame.mixer.music.load(MENU_MUSIC)  # Load the menu music file
    pygame.mixer.music.play(-1)  # Play the music indefinitely

    # Load and prepare the centered image
    center_image = pygame.image.load(os.path.join("assets", "spacediddler.png"))
    center_image = pygame.transform.scale(center_image, (1000, 500))  # Resize if needed
    center_x = (WIDTH - center_image.get_width()) // 2
    center_y = (HEIGHT - center_image.get_height()) // 8

    run = True  # Boolean to control the main menu loop
    while run:  # Main loop for the menu
        clock.tick(FPS)  # Ensure the game runs at the specified FPS
        video_frame = get_video_frame(menu_cap)  # Get the current frame from the menu video
        WIN.blit(video_frame, (0, 0))  # Draw the video frame on the window

        # Draw the centered image
        WIN.blit(center_image, (center_x, center_y))

        # Render the title and control text
        enter_text = menu_font.render("", 1, (255, 255, 255))  # Title text
        controls_text = controls_font.render("Enter to start", 1, (255, 255, 255))  # Control instructions text

        # Display the title and controls on the screen
        WIN.blit(enter_text, (WIDTH // 2 - enter_text.get_width() // 2, HEIGHT // 3))  # Center the title on the screen
        WIN.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 100))  # Center the controls text

        pygame.display.update()  # Update the display with the new frame

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                run = False  # Exit the menu loop
                pygame.quit()  # Quit pygame
                menu_cap.release()  # Release the video capture object
                quit()  # Exit the program

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # If the Enter key is pressed
                run = False  # Exit the menu loop and start the game

    menu_cap.release()  # Release the video capture object for the menu
    pygame.mixer.music.stop()  # Stop the menu music when the game starts

# Function to display the game over screen
def game_over_screen():
    over_font = pygame.font.SysFont("system", 150)  # Font for "Game Over" text
    restart_font = pygame.font.SysFont("system", 80)  # Font for restart instructions
    quit_font = pygame.font.SysFont("system", 80)  # Font for quit instructions

    run = True  # Boolean to control the game over loop
    while run:  # Main loop for game over screen
        WIN.fill((0, 0, 0))  # Fill the screen with black background
        over_label = over_font.render("Game Over", 1, (255, 0, 0))  # Render "Game Over" text
        restart_label = restart_font.render("Press R to Restart", 1, (255, 255, 255))  # Render restart instructions
        quit_label = quit_font.render("Press Q to Quit", 1, (255, 255, 255))  # Render quit instructions

        # Display the game over text and instructions
        WIN.blit(over_label, (WIDTH // 2 - over_label.get_width() // 2, HEIGHT // 2 - 100))  # Center "Game Over" text
        WIN.blit(restart_label, (WIDTH // 2 - restart_label.get_width() // 2, HEIGHT // 2))  # Center restart instructions
        WIN.blit(quit_label, (WIDTH // 2 - quit_label.get_width() // 2, HEIGHT // 2 + 100))  # Center quit instructions

        pygame.display.update()  # Update the display with the new screen

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                pygame.quit()  # Quit pygame
                quit()  # Exit the program

        # Check if player wants to restart or quit
        keys = pygame.key.get_pressed()  # Get the pressed keys
        if keys[pygame.K_r]:  # If "R" is pressed, restart the game
            main()  # Call the main game function
        if keys[pygame.K_q]:  # If "Q" is pressed, quit the game
            pygame.quit()  # Quit pygame
            quit()  # Exit the program

# Load spaceship images and transform them to appropriate sizes
BLACK_SPACE_SHIP = pygame.image.load(os.path.join("assets", "MINI_ENEMY.png"))  # Red ship image
BLACK_SPACE_SHIP = pygame.transform.scale(BLACK_SPACE_SHIP, (70, 70))  # Scale the red ship
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship2.png"))  # Red ship image
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, (70, 70))  # Scale the red ship
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship5.png"))  # Green ship image
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, (70, 70))  # Scale the green ship
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "blueship1.png"))  # Blue ship image
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP, (70, 70))  # Scale the blue ship
MY_SHIP = pygame.image.load(os.path.join("assets", "ship1.png"))  # Player ship image
MY_SHIP = pygame.transform.scale(MY_SHIP, (70, 70))  # Scale the player ship

# Load laser images
BLACK_LASER = pygame.image.load(os.path.join("assets", "ENEMY_LASER_BLAST.png"))  # Yellow laser image
BLACK_LASER = pygame.transform.scale(BLACK_LASER, (30, 30))  # Scale yellow laser
DIDDY_LASER = pygame.image.load(os.path.join("assets", "diddyoil.png"))  # Diddy laser image
DIDDY_LASER = pygame.transform.scale(DIDDY_LASER, (120, 120))  # Scale Diddy laser
RED_LASER = pygame.image.load(os.path.join("assets", "red.png"))  # Red laser image
RED_LASER = pygame.transform.scale(RED_LASER, (30, 30))  # Scale the red laser
GREEN_LASER = pygame.image.load(os.path.join("assets", "green.png"))  # Green laser image
GREEN_LASER = pygame.transform.scale(GREEN_LASER, (30, 30))  # Scale the green laser
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue.png"))  # Blue laser image
BLUE_LASER = pygame.transform.scale(BLUE_LASER, (30, 30))  # Scale the blue laser
YELLOW_LASER = pygame.image.load(os.path.join("assets", "yellow.png"))  # Yellow laser image
YELLOW_LASER = pygame.transform.scale(YELLOW_LASER, (30, 30))  # Scale yellow laser
SUPER_LASER = pygame.image.load(os.path.join("assets", "myLaser.png"))  # Super laser image
SUPER_LASER = pygame.transform.scale(SUPER_LASER, (100, 100))  # Scale super laser

# Laser class for handling laser behavior
class Laser:
    def __init__(self, x, y, img):
        self.x = x  # X-coordinate of laser
        self.y = y  # Y-coordinate of laser
        self.img = img  # Laser image
        self.mask = pygame.mask.from_surface(self.img)  # Create a mask for pixel-perfect collision detection

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))  # Draw the laser on the window

    def move(self, vel):
        self.y += vel  # Move the laser by its velocity along the y-axis

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)  # Check if the laser is off the screen

    def collision(self, obj):
        return collide(self, obj)  # Check if the laser collides with another object

# Ship class to handle ship behavior
class Ship:
    COOLDOWN = 10  # Cooldown time between laser shots
    HIT_INDICATOR_DURATION = 30  # Time the ship stays tinted red when hit

    def __init__(self, x, y, health=100):
        self.x = x  # X-coordinate of ship
        self.y = y  # Y-coordinate of ship
        self.health = health  # Ship's health
        self.ship_img = None  # Placeholder for ship image
        self.laser_img = None  # Placeholder for laser image
        self.lasers = []  # List of lasers shot by the ship
        self.cool_down_counter = 0  # Cooldown counter for shooting
        self.hit_timer = 0  # Timer for hit indicator (red tint)

    def draw(self, window):
        if self.hit_timer > 0:  # If the ship has been hit
            self.hit_timer -= 1  # Decrease the hit timer
            tinted_img = tint_image(self.ship_img, (255, 0, 0))  # Apply a red tint to the ship
            window.blit(tinted_img, (self.x, self.y))  # Draw the tinted ship
        else:
            window.blit(self.ship_img, (self.x, self.y))  # Draw the normal ship

        for laser in self.lasers:  # Draw all lasers shot by the ship
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()  # Handle the shooting cooldown
        for laser in self.lasers:
            laser.move(vel)  # Move the laser
            if laser.off_screen(HEIGHT):  # Remove the laser if it goes off screen
                self.lasers.remove(laser)
            elif laser.collision(obj):  # Check for collision with an object
                obj.take_hit()  # If collision occurs, apply hit to the object
                obj.health -= 10  # Decrease object's health
                LASER_HIT_SOUND.play()  # Play the laser hit sound
                self.lasers.remove(laser)  # Remove the laser after collision

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:  # If cooldown is complete
            self.cool_down_counter = 0  # Reset the cooldown counter
        elif self.cool_down_counter > 0:  # If cooldown is still ongoing
            self.cool_down_counter += 1  # Increment the cooldown counter

    def shoot(self):
        if self.cool_down_counter == 0:  # If cooldown is complete
            laser = Laser(self.x + self.get_width()//2, self.y, self.laser_img)  # Create a new laser
            self.lasers.append(laser)  # Add the laser to the list of lasers
            self.cool_down_counter = 1  # Start the cooldown

    def take_hit(self):
        self.hit_timer = self.HIT_INDICATOR_DURATION  # Start the hit indicator timer

    def get_width(self):
        return self.ship_img.get_width()  # Return the width of the ship

    def get_height(self):
        return self.ship_img.get_height()  # Return the height of the ship

# Player class, inheriting from Ship
class Player(Ship):
    def __init__(self, x, y, health=1000):
        super().__init__(x, y, health)  # Initialize the player with position and health
        self.ship_img = MY_SHIP  # Set the player's ship image
        self.laser_img = YELLOW_LASER  # Set the player's laser image
        self.mask = pygame.mask.from_surface(self.ship_img)  # Create a mask for the ship
        self.max_health = health  # Store the player's maximum health

        self.fuel = 0  # Initial fuel level (0% full)
        self.max_fuel = 100  # Maximum fuel level (100% full)
        self.super_move_ready = False  # Track if the super move is ready

        # New properties for fuel bar animation
        self.target_fuel = 0  # Where we want the fuel to reach
        self.fuel_fill_speed = 1  # Control the speed of the fuel bar filling

    def move_lasers(self, vel, objs):
        self.cooldown()  # Handle the shooting cooldown
        for laser in self.lasers[:]:
            laser.move(vel)  # Move the laser
            if laser.off_screen(HEIGHT):  # If the laser goes off screen
                self.lasers.remove(laser)
            else:
                for obj in objs:  # Check for collision with each object
                    if laser.collision(obj):
                        obj.take_hit()  # If collision occurs, apply hit
                        obj.health -= 200  # One-hit kill: laser deals 100 damage
                        LASER_HIT_SOUND.play()  # Play hit sound
                        if obj.health <= 0:  # If object's health reaches 0
                            objs.remove(obj)  # Remove the object
                            global score  # Increase score on enemy kill
                            score += 100  # Add points to the score

                        # Smoothly fill the fuel bar when hitting enemies
                        self.target_fuel += 10  # Increase fuel target
                        if self.target_fuel >= self.max_fuel:  # If fuel is maxed out
                            self.target_fuel = self.max_fuel  # Cap fuel at max level
                            self.super_move_ready = True  # Super move ready once fuel is full

                        if laser in self.lasers:  # Ensure the laser is removed after hit
                            self.lasers.remove(laser)

    def shoot_super_laser(self):
        """Shoot the super laser only if fuel is full."""
        if self.super_move_ready:  # Ensure super move can only be used when ready
            # Play special attack sound effect
            SPECIAL_ATTACK_SOUND.play()
            laser = Laser(self.x + self.get_width()//2 - SUPER_LASER.get_width()//2, self.y - SUPER_LASER.get_height(), SUPER_LASER)  # Create the super laser
            self.lasers.append(laser)  # Add the super laser to the player's lasers
            self.super_move_ready = False  # Reset super move availability
            self.fuel = 0  # Empty the fuel bar after using the super move
            self.target_fuel = 0  # Reset target fuel to 0

    def update_fuel(self):
        """Smoothly update the fuel towards the target level."""
        if self.fuel < self.target_fuel:
            self.fuel += self.fuel_fill_speed  # Gradually increase the fuel
        elif self.fuel > self.target_fuel:
            self.fuel = self.target_fuel  # Clamp fuel to target

    def draw(self, window):
        super().draw(window)  # Draw the player ship and its lasers
        self.healthbar(window)  # Draw the health bar
        self.draw_fuel_bar(window)  # Draw the fuel bar on the screen

    def healthbar(self, window): 
        """Draw health bar below the ship."""
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))  # Draw red (empty) health bar
        pygame.draw.rect(window, (0, 255, 0), 
                         (self.x, self.y + self.get_height() + 10, self.get_width() * (self.health / self.max_health), 10))  # Draw green (filled) health bar

    def draw_fuel_bar(self, window):
        """Draw the fuel bar on the screen."""
        fuel_bar_x = self.x  # X-coordinate for fuel bar
        fuel_bar_y = self.y + self.ship_img.get_height() + 20  # Y-coordinate for fuel bar
        fuel_bar_width = self.ship_img.get_width()  # Width of the fuel bar
        fuel_bar_height = 10  # Height of the fuel bar

        # Draw empty fuel bar (red background)
        pygame.draw.rect(window, (255, 0, 0), (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height))
        
        # Draw filled part of the fuel bar (blue foreground)
        fuel_ratio = self.fuel / self.max_fuel  # Calculate fuel ratio
        pygame.draw.rect(window, (0, 0, 255), (fuel_bar_x, fuel_bar_y, fuel_bar_width * fuel_ratio, fuel_bar_height))

    def collect_power_up(self, power_up):
        """Handle different types of power-ups."""
        if power_up.type == "health":
            self.health = self.max_health  # Fully restore health
        elif power_up.type == "fuel":
            self.target_fuel = min(self.max_fuel, self.target_fuel + 50)  # Increase fuel by 50
        elif power_up.type == "shield":
            # Placeholder for shield effect, could be implemented as extra hit points or temporary invincibility
            print("Shield power-up collected!")

# PowerUp class to handle power-up behavior
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x  # X-coordinate of power-up
        self.y = y  # Y-coordinate of power-up
        self.type = type  # Power-up type (health, fuel, shield)
        if self.type == "health":
            self.img = pygame.image.load(os.path.join("assets", "healthOrb.png.png"))  # Load health power-up image
        else:
            self.img = pygame.image.load(os.path.join("assets", "bluorb.png"))  # Load fuel power-up image
        self.img = pygame.transform.scale(self.img, (50, 50))  # Scale the power-up image
        self.mask = pygame.mask.from_surface(self.img)  # Create a mask for collision detection

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))  # Draw the power-up on the screen

    def move(self, vel):
        self.y += vel  # Move the power-up downwards by the given velocity

    def collision(self, obj):
        return collide(self, obj)  # Check if the power-up collides with the player

# Function to spawn random power-ups
def spawn_power_up():
    power_up_types = ["health", "shield", "fuel"]  # Define available power-up types
    chosen_power_up = random.choice(power_up_types)  # Randomly select a power-up type
    return PowerUp(random.randrange(50, WIDTH - 50), random.randrange(-1000, -100), chosen_power_up)  # Return a new power-up object at a random position

# Enemy class, inheriting from Ship
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),  # Red ship and laser
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),  # Green ship and laser
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),  # Blue ship and laser
        "black": (BLACK_SPACE_SHIP, BLACK_LASER) 
    }

    def __init__(self, x, y, color):
        super().__init__(x, y, health=10)  # Normal enemies have 10 health (die in one hit)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]  # Assign the ship and laser images based on color
        self.mask = pygame.mask.from_surface(self.ship_img)  # Create a mask for the ship

    def move(self, vel):
        self.y += vel  # Move the enemy downwards by the given velocity

    def shoot(self):
        if self.cool_down_counter == 0:  # If cooldown is complete
            laser = Laser(self.x - 20, self.y, self.laser_img)  # Create a new laser
            self.lasers.append(laser)  # Add the laser to the enemy's lasers
            self.cool_down_counter = 1  # Start the cooldown

# Boss class, inheriting from Ship
class Boss(Ship):
    BOSS_COOLDOWN = 50  # 5 seconds cooldown (at 60 FPS)

    def __init__(self, x, y, health=30000):
        super().__init__(x, y, health)  # Initialize the boss with large health
        self.ship_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BOSS_DIDDY.png")), (150, 150))  # Load and scale the boss image
        self.laser_img = DIDDY_LASER  # Assign the laser image for the boss
        self.mask = pygame.mask.from_surface(self.ship_img)  # Create a mask for the boss
        self.max_health = health  # Store the boss's maximum health
        self.boss_cool_down_counter = 0  # Cooldown counter for the boss's attacks

    def move(self, vel):
        # Randomly move the boss in one of the four directions
        direction = random.choice(['up', 'down', 'left', 'right'])

        if direction == 'up' and self.y - vel > 0:
            self.y -= vel  # Move up
        if direction == 'down' and self.y + vel + self.get_height() < HEIGHT:
            self.y += vel  # Move down
        if direction == 'left' and self.x - vel > 0:
            self.x -= vel  # Move left
        if direction == 'right' and self.x + vel + self.get_width() < WIDTH:
            self.x += vel  # Move right

    def draw(self, window):
        super().draw(window)  # Draw the boss and its lasers
        self.healthbar(window)  # Draw the boss's health bar

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))  # Draw the red (empty) health bar
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.get_height() + 10, self.get_width() * (self.health / self.max_health), 10))  # Draw the green (filled) health bar

    def boss_shoot(self):
        if self.boss_cool_down_counter == 0:  # If cooldown is complete
            for angle in [-30, 0, 30]:  # Shoot lasers at three angles (-30, 0, +30 degrees)
                laser = Laser(self.x + self.get_width() // 2 - 10, self.y + self.get_height(), pygame.transform.rotate(self.laser_img, angle))  # Rotate the laser by the angle
                self.lasers.append(laser)  # Add the laser to the boss's lasers
            self.boss_cool_down_counter = 1  # Start the cooldown

    def boss_cooldown(self):
        if self.boss_cool_down_counter >= self.BOSS_COOLDOWN:  # If cooldown is complete
            self.boss_cool_down_counter = 0  # Reset the cooldown counter
        elif self.boss_cool_down_counter > 0:  # If cooldown is still ongoing
            self.boss_cool_down_counter += 1  # Increment the cooldown counter

# Function to spawn a boss at specific levels
def spawn_boss(level):
    if level % 5 == 0:  # Spawn a boss every 5 levels
        health = 30000 + (level // 5) * 5000  # Increase boss health with each boss
        return Boss(WIDTH // 2 - 75, -100, health)  # Return a new boss object
    return None

# Function to detect collision between two objects
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # Calculate x-offset between objects
    offset_y = obj2.y - obj1.y  # Calculate y-offset between objects
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # Return True if masks overlap, indicating a collision

# Function to handle player movement based on key input
def handle_movement(keys, player, player_vel):
    move_speed = player_vel  # Default movement speed
    if keys[pygame.K_LSHIFT]:  # Boost speed when "Shift" is pressed
        move_speed = player_vel * 1.5  # 50% speed increase

    if keys[pygame.K_a] and player.x - move_speed > 0:  # Move left
        player.x -= move_speed
    if keys[pygame.K_d] and player.x + move_speed + player.get_width() < WIDTH:  # Move right
        player.x += move_speed
    if keys[pygame.K_w] and player.y - move_speed > 0:  # Move up
        player.y -= move_speed
    if keys[pygame.K_s] and player.y + move_speed + player.get_height() + 15 < HEIGHT:  # Move down
        player.y += move_speed

# Main game function
def main():
    run = True  # Boolean to control the main game loop
    FPS = 60  # Frames per second
    level = 0  # Initial game level
    lives = 10  # Initial number of lives
    global score  # Declare score as global variable
    score = 0  # Initialize score to 0
    main_font = pygame.font.SysFont("system", 50)  # Font for main game labels
    lost_font = pygame.font.SysFont("system", 60)  # Font for "You Lost" message
    warning_font = pygame.font.SysFont("system", 80)  # Font for boss warning message

    enemies = []  # List to hold enemy ships
    wave_length = 5  # Initial wave length (number of enemies)
    enemy_vel = 1  # Initial enemy movement speed

    player_vel = 10  # Player movement speed
    laser_vel = 5  # Laser movement speed
    boss_vel = 2  # Boss movement speed

    player = Player(300, 630)  # Initialize player ship at (300, 630)

    clock = pygame.time.Clock()  # Create a clock to control frame rate

    lost = False  # Boolean to track if the player has lost
    lost_count = 0  # Counter for how long the lost message is shown

    boss_spawned = False  # Track if the boss has been spawned
    boss = None  # Boss object (None if no boss is present)
    boss_warning_displayed = False  # Track if the boss warning is being displayed
    boss_warning_timer = 0  # Timer for how long the boss warning is shown

    power_ups = []  # List to hold power-ups

    # Play game background music in a loop
    pygame.mixer.music.load(GAME_MUSIC)  # Load the game background music
    pygame.mixer.music.play(-1)  # Play the music indefinitely

    # Function to redraw the game window
    def redraw_window():
        video_frame = get_video_frame(game_cap)  # Get the current frame from the game background video
        WIN.blit(video_frame, (0, 0))  # Draw the video frame on the window

        # Render the game status labels
        lives_label = main_font.render(f"Health: {lives}", 1, (255, 255, 255))  # Health label
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))  # Level label
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))  # Score label

        # Display the labels on the screen
        WIN.blit(lives_label, (10, 10))  # Top left corner for lives
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))  # Top right corner for level
        WIN.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 10))  # Center for score

        for enemy in enemies:  # Draw each enemy on the screen
            enemy.draw(WIN)

        player.draw(WIN)  # Draw the player ship and its health/fuel bars

        for power_up in power_ups:  # Draw each power-up on the screen
            power_up.draw(WIN)

        if boss_spawned:  # If a boss is present
            boss.draw(WIN)  # Draw the boss

        if boss_warning_displayed:  # If the boss warning is being displayed
            warning_label = warning_font.render("Boss Incoming!", 1, (255, 0, 0))  # Render the boss warning text
            WIN.blit(warning_label, (WIDTH // 2 - warning_label.get_width() // 2, HEIGHT // 2))  # Center the warning text

        if lost:  # If the player has lost
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))  # Render "You Lost" message
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))  # Center the lost message

        pygame.display.update()  # Update the display with the new frame

    while run:  # Main game loop
        clock.tick(FPS)  # Control the game frame rate
        redraw_window()  # Redraw the window each frame

        if lives <= 0 or player.health <= 0:  # If the player runs out of lives or health
            lost = True  # Set lost to True
            lost_count += 1  # Increment lost count

        if lost:  # If the player has lost
            if lost_count > FPS * 3:  # After 3 seconds, show the game over screen
                game_over_screen()  # Call the game over screen

        if len(enemies) == 0 and not boss_spawned:  # If no enemies are left and no boss is present
            level += 1  # Increment the level
            wave_length += 5  # Increase the wave length (number of enemies)
            enemy_vel += 0 * (level // 2)  # Increase enemy speed every 2 levels
            for i in range(wave_length):  # Spawn new enemies for the new wave
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green", "black"]))  # Random enemy color
                enemies.append(enemy)  # Add the enemy to the list

            # Spawn a power-up randomly with a 30% chance
            if random.random() < 0.5:
                power_ups.append(spawn_power_up())  # Add a power-up to the list

            # Spawn a boss if it's a boss level
            if not boss_spawned and level % 5 == 0:  # Show warning before boss spawn
                boss_warning_displayed = True  # Show the boss warning
                boss_warning_timer = FPS * 3  # Display warning for 3 seconds
                boss_spawned = True  # Indicate that a boss has spawned
                boss = spawn_boss(level)  # Spawn the boss

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                run = False  # Exit the game loop

        keys = pygame.key.get_pressed()  # Get the pressed keys
        handle_movement(keys, player, player_vel)  # Handle player movement

        if keys[pygame.K_SPACE]:  # If space bar is pressed, shoot lasers
            player.shoot()

        if keys[pygame.K_k] and player.super_move_ready:  # If "K" is pressed and super move is ready, shoot super laser
            player.shoot_super_laser()

        if boss_spawned and boss_warning_displayed:  # If boss has spawned and warning is being displayed
            boss_warning_timer -= 1  # Decrease the warning timer
            if boss_warning_timer <= 0:  # If warning timer runs out
                boss_warning_displayed = False  # Stop displaying the boss warning

        # Handle enemy movement and shooting
        for enemy in enemies[:]:
            enemy.move(enemy_vel)  # Move the enemy
            enemy.move_lasers(laser_vel, player)  # Move enemy lasers and check for collision with player

            if random.randrange(0, 2 * 60) == 1:  # Random chance to shoot lasers
                enemy.shoot()

            if collide(enemy, player):  # Check for collision between enemy and player
                player.take_hit()  # Apply hit to player
                player.health -= 10  # Decrease player's health
                if player.health <= 0:  # If player's health is depleted
                    lives -= 1  # Decrease player's lives
                    player.health = player.max_health  # Restore player's health
                enemies.remove(enemy)  # Remove the enemy
            elif enemy.y + enemy.get_height() > HEIGHT:  # If the enemy moves off screen
                lives -= 1  # Decrease player's lives
                enemies.remove(enemy)  # Remove the enemy

        # Handle boss movement, shooting, and collision with player
        if boss_spawned:
            boss.move(boss_vel)  # Move the boss
            boss.boss_cooldown()  # Handle boss shooting cooldown
            boss.boss_shoot()  # Boss shoots lasers
            boss.move_lasers(laser_vel, player)  # Move boss lasers and check for collision with player

            if collide(boss, player):  # Check for collision between boss and player
                player.take_hit()  # Apply hit to player
                player.health -= 10  # Decrease player's health
                if player.health <= 0:  # If player's health is depleted
                    lives -= 1  # Decrease player's lives
                    player.health = player.max_health  # Restore player's health

            if boss.health > 0:  # If boss is still alive
                player.move_lasers(-laser_vel, [boss])  # Move player lasers and check for collision with boss
                for laser in player.lasers[:]:
                    if collide(laser, boss):  # Check for collision between player's laser and boss
                        boss.take_hit()  # Apply hit to boss
                        boss.health -= 500  # Decrease boss's health
                        LASER_HIT_SOUND.play()  # Play hit sound
                        player.lasers.remove(laser)  # Remove the laser

            if boss.health <= 0:  # If boss's health is depleted
                boss_spawned = False  # Boss is defeated
                boss = None  # Remove the boss object

        # Handle player lasers and collision with enemies
        player.move_lasers(-laser_vel, enemies)  # Move player lasers and check for collision with enemies
        player.update_fuel()  # Update the fuel bar animation

        # Handle power-ups
        for power_up in power_ups[:]:
            power_up.move(2)  # Move the power-up downwards
            if collide(power_up, player):  # Check for collision with player
                player.collect_power_up(power_up)  # Apply the power-up effect to the player
                power_ups.remove(power_up)  # Remove the power-up
            elif power_up.y > HEIGHT:  # If the power-up moves off screen
                power_ups.remove(power_up)  # Remove the power-up

    game_cap.release()  # Release the game background video capture object
    pygame.quit()  # Quit pygame

# Run the game by calling the main menu and main game functions
if __name__ == "__main__":
    main_menu()  # Display the main menu
    main()  # Start the main game
