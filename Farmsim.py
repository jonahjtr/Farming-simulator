import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
CELL_SIZE = 40
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + 300  # Extra space for UI
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100
FPS = 60

# Colors
BLACK = (0, 0, 0)
DARK_GREEN = (45, 80, 22)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
LIGHT_PURPLE = (200, 100, 200)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
BLUE = (0, 100, 255)
RED = (255, 50, 50)

class FarmGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Farm Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Game state
        self.player_x = 10
        self.player_y = 10
        self.gold = 200
    
        self.inventory = {'corn': 0, 'turnips': 0}
        self.shed_storage = {'corn': 0, 'turnips': 0}
        self.grid = [[{'type': 'empty', 'growth': 0} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.merchant_open = False
        self.merchant_menu = 'main'  # 'main', 'buy', 'sell'
        self.growth_timer = 0
        self.move_timer = 0
        self.move_delay = 8  # frames between moves when holding key
        
        # AI Helper
        self.has_ai_helper = False
        self.ai_x = 3
        self.ai_y = 3
        self.ai_harvest_timer = 0
        self.ai_harvest_interval = 120  # frames between AI harvests
        
        # Place merchant
        self.merchant_x = 5
        self.merchant_y = 5
        self.grid[self.merchant_y][self.merchant_x] = {'type': 'merchant', 'growth': 0}
        
        # Place shed
        self.shed_x = 15
        self.shed_y = 15
        self.grid[self.shed_y][self.shed_x] = {'type': 'shed', 'growth': 0}
        
        # Initialize crops
        for _ in range(15):
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x]['type'] == 'empty':
                crop_type = random.choice(['corn', 'turnip'])
                self.grid[y][x] = {'type': crop_type, 'growth': random.randint(0, 100)}
    
    def get_cell_color(self, cell):
        if cell['type'] == 'merchant':
            return ORANGE
        elif cell['type'] == 'shed':
            return BROWN
        elif cell['type'] == 'corn':
            intensity = 100 + int(cell['growth'] * 1.55)
            return (intensity, intensity, 0)
        elif cell['type'] == 'turnip':
            intensity = 100 + int(cell['growth'] * 1.55)
            return (intensity, 0, intensity)
        else:
            return DARK_GREEN
    
    def draw_grid(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = self.grid[y][x]
                color = self.get_cell_color(cell)
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw growth percentage for growing crops
                if cell['type'] in ['corn', 'turnip'] and cell['growth'] < 100:
                    growth_text = self.font.render(f"{cell['growth']}%", True, WHITE)
                    text_rect = growth_text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, 
                                                              y * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(growth_text, text_rect)
                
                # Draw symbols for mature crops, merchant, and shed
                if cell['type'] == 'corn' and cell['growth'] == 100:
                    symbol = self.font.render("C", True, WHITE)
                    symbol_rect = symbol.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                          y * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(symbol, symbol_rect)
                elif cell['type'] == 'turnip' and cell['growth'] == 100:
                    symbol = self.font.render("T", True, WHITE)
                    symbol_rect = symbol.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                          y * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(symbol, symbol_rect)
                elif cell['type'] == 'merchant':
                    symbol = self.title_font.render("M", True, WHITE)
                    symbol_rect = symbol.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                          y * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(symbol, symbol_rect)
                elif cell['type'] == 'shed':
                    symbol = self.title_font.render("S", True, WHITE)
                    symbol_rect = symbol.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                          y * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(symbol, symbol_rect)
        
        # Draw AI helper
        if self.has_ai_helper:
            ai_rect = pygame.Rect(self.ai_x * CELL_SIZE + 5, 
                                 self.ai_y * CELL_SIZE + 5,
                                 CELL_SIZE - 10, CELL_SIZE - 10)
            pygame.draw.rect(self.screen, BLUE, ai_rect, 3)
            ai_text = self.title_font.render("A", True, BLUE)
            ai_text_rect = ai_text.get_rect(center=(self.ai_x * CELL_SIZE + CELL_SIZE // 2,
                                                    self.ai_y * CELL_SIZE + CELL_SIZE // 2))
            self.screen.blit(ai_text, ai_text_rect)
        
        # Draw player
        player_rect = pygame.Rect(self.player_x * CELL_SIZE + 5, 
                                 self.player_y * CELL_SIZE + 5,
                                 CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(self.screen, WHITE, player_rect, 3)
        player_text = self.title_font.render("@", True, WHITE)
        player_text_rect = player_text.get_rect(center=(self.player_x * CELL_SIZE + CELL_SIZE // 2,
                                                        self.player_y * CELL_SIZE + CELL_SIZE // 2))
        self.screen.blit(player_text, player_text_rect)
    
    def draw_ui(self):
        ui_x = GRID_SIZE * CELL_SIZE + 20
        ui_y = 20
        
        # Title
        title = self.title_font.render("FARM SIMULATOR", True, GOLD)
        self.screen.blit(title, (ui_x, ui_y))
        
        # Stats
        stats_y = ui_y + 60
        gold_text = self.font.render(f"Gold: {self.gold}", True, GOLD)
        self.screen.blit(gold_text, (ui_x, stats_y))
        
        inv_title = self.font.render("Inventory:", True, WHITE)
        self.screen.blit(inv_title, (ui_x, stats_y + 30))
        
        corn_text = self.font.render(f"  Corn: {self.inventory['corn']}", True, YELLOW)
        self.screen.blit(corn_text, (ui_x, stats_y + 55))
        
        turnip_text = self.font.render(f"  Turnips: {self.inventory['turnips']}", True, LIGHT_PURPLE)
        self.screen.blit(turnip_text, (ui_x, stats_y + 80))
        
        # Shed storage
        shed_title = self.font.render("Shed Storage:", True, WHITE)
        self.screen.blit(shed_title, (ui_x, stats_y + 110))
        
        shed_corn = self.font.render(f"  Corn: {self.shed_storage['corn']}", True, YELLOW)
        self.screen.blit(shed_corn, (ui_x, stats_y + 135))
        
        shed_turnip = self.font.render(f"  Turnips: {self.shed_storage['turnips']}", True, LIGHT_PURPLE)
        self.screen.blit(shed_turnip, (ui_x, stats_y + 160))
        
        # AI Helper status
        ai_y = stats_y + 195
        if self.has_ai_helper:
            ai_status = self.font.render("AI Helper: Active", True, BLUE)
        else:
            ai_status = self.font.render("AI Helper: None", True, GRAY)
        self.screen.blit(ai_status, (ui_x, ai_y))
        
        # Controls
        controls_y = ai_y + 40
        control_lines = [
            "CONTROLS:",
            "WASD - Move (hold)",
            "Left Click - Harvest/Plant",
            "Walk to M - Merchant",
            "Walk to S - Shed",
            "ESC - Quit"
        ]
        
        for i, line in enumerate(control_lines):
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (ui_x, controls_y + i * 22))
        
        # Legend
        legend_y = controls_y + 150
        legend_lines = [
            "LEGEND:",
            "@ - You",
            "A - AI Helper",
            "M - Merchant",
            "S - Shed",
            "C/T - Ripe crops"
        ]
        
        for i, line in enumerate(legend_lines):
            text = self.font.render(line, True, GRAY)
            self.screen.blit(text, (ui_x, legend_y + i * 22))
    
    def draw_merchant_window(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw merchant window
        window_width = 500
        window_height = 450
        window_x = (WINDOW_WIDTH - window_width) // 2
        window_y = (WINDOW_HEIGHT - window_height) // 2
        
        pygame.draw.rect(self.screen, BROWN, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, GOLD, (window_x, window_y, window_width, window_height), 3)
        
        if self.merchant_menu == 'main':
            # Title
            title = self.title_font.render("MERCHANT SHOP", True, GOLD)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, window_y + 30))
            self.screen.blit(title, title_rect)
            
            # Current gold
            gold_text = self.font.render(f"Your Gold: {self.gold}", True, WHITE)
            self.screen.blit(gold_text, (window_x + 30, window_y + 80))
            
            # Menu options
            menu_y = window_y + 140
            menu_text = self.font.render("What would you like to do?", True, WHITE)
            self.screen.blit(menu_text, (window_x + 30, menu_y))
            
            option1 = self.font.render("1 - Sell Crops", True, GREEN)
            self.screen.blit(option1, (window_x + 50, menu_y + 50))
            
            option2 = self.font.render("2 - Buy Items", True, GREEN)
            self.screen.blit(option2, (window_x + 50, menu_y + 90))
            
            option3 = self.font.render("ESC - Close", True, GRAY)
            self.screen.blit(option3, (window_x + 50, menu_y + 130))
        
        elif self.merchant_menu == 'sell':
            # Title
            title = self.title_font.render("SELL CROPS", True, GOLD)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, window_y + 30))
            self.screen.blit(title, title_rect)
            
            # Current gold
            gold_text = self.font.render(f"Your Gold: {self.gold}", True, WHITE)
            self.screen.blit(gold_text, (window_x + 30, window_y + 80))
            
            # Inventory
            inv_y = window_y + 120
            inv_text = self.font.render("Your Inventory:", True, WHITE)
            self.screen.blit(inv_text, (window_x + 30, inv_y))
            
            corn_text = self.font.render(f"Corn: {self.inventory['corn']}", True, YELLOW)
            self.screen.blit(corn_text, (window_x + 50, inv_y + 30))
            
            turnip_text = self.font.render(f"Turnips: {self.inventory['turnips']}", True, LIGHT_PURPLE)
            self.screen.blit(turnip_text, (window_x + 50, inv_y + 60))
            
            # Exchange rates
            rates_y = window_y + 230
            rates_text = self.font.render("Exchange Rates:", True, WHITE)
            self.screen.blit(rates_text, (window_x + 30, rates_y))
            
            corn_rate = self.font.render("1 Corn = 1 Gold", True, YELLOW)
            self.screen.blit(corn_rate, (window_x + 50, rates_y + 30))
            
            turnip_rate = self.font.render("1 Turnip = 2 Gold", True, LIGHT_PURPLE)
            self.screen.blit(turnip_rate, (window_x + 50, rates_y + 60))
            
            # Buttons
            button_y = window_y + 350
            instructions = self.font.render("C: Sell Corn | T: Sell Turnips | ESC: Back", True, WHITE)
            inst_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, button_y))
            self.screen.blit(instructions, inst_rect)
        
        elif self.merchant_menu == 'buy':
            # Title
            title = self.title_font.render("BUY ITEMS", True, GOLD)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, window_y + 30))
            self.screen.blit(title, title_rect)
            
            # Current gold
            gold_text = self.font.render(f"Your Gold: {self.gold}", True, WHITE)
            self.screen.blit(gold_text, (window_x + 30, window_y + 80))
            
            # AI Helper item
            item_y = window_y + 140
            item_title = self.title_font.render("AI HELPER", True, BLUE)
            self.screen.blit(item_title, (window_x + 30, item_y))
            
            price_text = self.font.render("Price: 200 Gold", True, GOLD)
            self.screen.blit(price_text, (window_x + 30, item_y + 40))
            
            desc_lines = [
                "The AI Helper will automatically:",
                "- Harvest mature crops",
                "- Store them in the Shed",
                "- Work continuously"
            ]
            
            for i, line in enumerate(desc_lines):
                text = self.font.render(line, True, WHITE)
                self.screen.blit(text, (window_x + 30, item_y + 80 + i * 25))
            
            if self.has_ai_helper:
                status = self.font.render("STATUS: Already Purchased!", True, GREEN)
                self.screen.blit(status, (window_x + 30, item_y + 200))
                
                instructions = self.font.render("ESC - Back", True, WHITE)
            else:
                if self.gold >= 200:
                    instructions = self.font.render("Press B to Buy | ESC - Back", True, WHITE)
                else:
                    need_text = self.font.render(f"Need {200 - self.gold} more gold!", True, RED)
                    self.screen.blit(need_text, (window_x + 30, item_y + 200))
                    instructions = self.font.render("ESC - Back", True, WHITE)
            
            inst_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, window_y + 390))
            self.screen.blit(instructions, inst_rect)
    
    def draw_shed_window(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw shed window
        window_width = 500
        window_height = 400
        window_x = (WINDOW_WIDTH - window_width) // 2
        window_y = (WINDOW_HEIGHT - window_height) // 2
        
        pygame.draw.rect(self.screen, BROWN, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, GOLD, (window_x, window_y, window_width, window_height), 3)
        
        # Title
        title = self.title_font.render("SHED STORAGE", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, window_y + 30))
        self.screen.blit(title, title_rect)
        
        # Shed storage
        storage_y = window_y + 100
        storage_text = self.font.render("Stored Items:", True, WHITE)
        self.screen.blit(storage_text, (window_x + 30, storage_y))
        
        corn_text = self.font.render(f"Corn: {self.shed_storage['corn']}", True, YELLOW)
        self.screen.blit(corn_text, (window_x + 50, storage_y + 40))
        
        turnip_text = self.font.render(f"Turnips: {self.shed_storage['turnips']}", True, LIGHT_PURPLE)
        self.screen.blit(turnip_text, (window_x + 50, storage_y + 80))
        
        # Your inventory
        inv_y = window_y + 230
        inv_text = self.font.render("Your Inventory:", True, WHITE)
        self.screen.blit(inv_text, (window_x + 30, inv_y))
        
        your_corn = self.font.render(f"Corn: {self.inventory['corn']}", True, YELLOW)
        self.screen.blit(your_corn, (window_x + 50, inv_y + 40))
        
        your_turnip = self.font.render(f"Turnips: {self.inventory['turnips']}", True, LIGHT_PURPLE)
        self.screen.blit(your_turnip, (window_x + 50, inv_y + 80))
        
        # Instructions
        inst_y = window_y + 350
        instructions = self.font.render("C: Withdraw Corn | T: Withdraw Turnips | ESC: Close", True, WHITE)
        inst_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, inst_y))
        self.screen.blit(instructions, inst_rect)
    
    def handle_click(self, mouse_x, mouse_y):
        grid_x = mouse_x // CELL_SIZE
        grid_y = mouse_y // CELL_SIZE
        
        # Check if click is within grid
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            # Check if adjacent to player
            if abs(self.player_x - grid_x) <= 1 and abs(self.player_y - grid_y) <= 1:
                cell = self.grid[grid_y][grid_x]
                
                if cell['type'] == 'corn' and cell['growth'] == 100:
                    self.inventory['corn'] += 1
                    self.grid[grid_y][grid_x] = {'type': 'empty', 'growth': 0}
                elif cell['type'] == 'turnip' and cell['growth'] == 100:
                    self.inventory['turnips'] += 1
                    self.grid[grid_y][grid_x] = {'type': 'empty', 'growth': 0}
                elif cell['type'] == 'empty':
                    crop_type = random.choice(['corn', 'turnip'])
                    self.grid[grid_y][grid_x] = {'type': crop_type, 'growth': 0}
    
    def move_player(self, dx, dy):
        new_x = max(0, min(GRID_SIZE - 1, self.player_x + dx))
        new_y = max(0, min(GRID_SIZE - 1, self.player_y + dy))
        self.player_x = new_x
        self.player_y = new_y
        
        # Check if on merchant
        if self.grid[self.player_y][self.player_x]['type'] == 'merchant':
            self.merchant_open = True
            self.merchant_menu = 'main'
        # Check if on shed
        elif self.grid[self.player_y][self.player_x]['type'] == 'shed':
            self.merchant_open = True
            self.merchant_menu = 'shed'
    
    def ai_harvest(self):
        # Find nearest mature crop
        best_dist = float('inf')
        target_x, target_y = None, None
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = self.grid[y][x]
                if cell['type'] in ['corn', 'turnip'] and cell['growth'] == 100:
                    dist = abs(x - self.ai_x) + abs(y - self.ai_y)
                    if dist < best_dist:
                        best_dist = dist
                        target_x, target_y = x, y
        
        # Move towards target or harvest if adjacent
        if target_x is not None:
            if abs(self.ai_x - target_x) <= 1 and abs(self.ai_y - target_y) <= 1:
                # Harvest
                cell = self.grid[target_y][target_x]
                if cell['type'] == 'corn':
                    self.shed_storage['corn'] += 1
                elif cell['type'] == 'turnip':
                    self.shed_storage['turnips'] += 1
                self.grid[target_y][target_x] = {'type': 'empty', 'growth': 0}
            else:
                # Move towards target
                if abs(self.ai_x - target_x) > abs(self.ai_y - target_y):
                    if self.ai_x < target_x:
                        self.ai_x = min(GRID_SIZE - 1, self.ai_x + 1)
                    else:
                        self.ai_x = max(0, self.ai_x - 1)
                else:
                    if self.ai_y < target_y:
                        self.ai_y = min(GRID_SIZE - 1, self.ai_y + 1)
                    else:
                        self.ai_y = max(0, self.ai_y - 1)
    
    def grow_crops(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = self.grid[y][x]
                if cell['type'] in ['corn', 'turnip'] and cell['growth'] < 100:
                    cell['growth'] = min(100, cell['growth'] + 2)
    
    def sell_corn(self):
        if self.inventory['corn'] > 0:
            self.gold += self.inventory['corn']
            self.inventory['corn'] = 0
    
    def sell_turnips(self):
        if self.inventory['turnips'] > 0:
            self.gold += self.inventory['turnips'] * 2
            self.inventory['turnips'] = 0
    
    def buy_ai_helper(self):
        if not self.has_ai_helper and self.gold >= 200:
            self.gold -= 200
            self.has_ai_helper = True
    
    def withdraw_from_shed(self, crop_type):
        if crop_type == 'corn' and self.shed_storage['corn'] > 0:
            self.inventory['corn'] += self.shed_storage['corn']
            self.shed_storage['corn'] = 0
        elif crop_type == 'turnip' and self.shed_storage['turnips'] > 0:
            self.inventory['turnips'] += self.shed_storage['turnips']
            self.shed_storage['turnips'] = 0
    
    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.merchant_open:
                        if event.key == pygame.K_ESCAPE:
                            if self.merchant_menu == 'main':
                                self.merchant_open = False
                            else:
                                self.merchant_menu = 'main'
                        elif self.merchant_menu == 'main':
                            if event.key == pygame.K_1:
                                self.merchant_menu = 'sell'
                            elif event.key == pygame.K_2:
                                self.merchant_menu = 'buy'
                        elif self.merchant_menu == 'sell':
                            if event.key == pygame.K_c:
                                self.sell_corn()
                            elif event.key == pygame.K_t:
                                self.sell_turnips()
                        elif self.merchant_menu == 'buy':
                            if event.key == pygame.K_b:
                                self.buy_ai_helper()
                        elif self.merchant_menu == 'shed':
                            if event.key == pygame.K_c:
                                self.withdraw_from_shed('corn')
                            elif event.key == pygame.K_t:
                                self.withdraw_from_shed('turnip')
                    else:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.merchant_open:
                    if event.button == 1:  # Left click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.handle_click(mouse_x, mouse_y)
            
            # Handle held keys for movement
            if not self.merchant_open:
                keys = pygame.key.get_pressed()
                self.move_timer += 1
                
                if self.move_timer >= self.move_delay:
                    moved = False
                    if keys[pygame.K_w]:
                        self.move_player(0, -1)
                        moved = True
                    elif keys[pygame.K_s]:
                        self.move_player(0, 1)
                        moved = True
                    elif keys[pygame.K_a]:
                        self.move_player(-1, 0)
                        moved = True
                    elif keys[pygame.K_d]:
                        self.move_player(1, 0)
                        moved = True
                    
                    if moved:
                        self.move_timer = 0
            
            # AI Helper logic
            if self.has_ai_helper:
                self.ai_harvest_timer += 1
                if self.ai_harvest_timer >= self.ai_harvest_interval:
                    self.ai_harvest()
                    self.ai_harvest_timer = 0
            
            # Grow crops every second
            self.growth_timer += 1
            if self.growth_timer >= FPS:
                self.grow_crops()
                self.growth_timer = 0
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_ui()
            
            if self.merchant_open:
                if self.merchant_menu == 'shed':
                    self.draw_shed_window()
                else:
                    self.draw_merchant_window()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FarmGame()
    game.run()