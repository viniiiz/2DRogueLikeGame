import math

import pygame
import random
from code.Entity import Entity
from code.Background import Background
from code.Player import Player
from code.Enemy import Enemy, TankEnemy
from code.Projectile import Projectile
from code.HUD import HUD
from code.Const import WIN_WIDTH, WIN_HEIGHT


ENEMY_LIMIT = 100
SPAWN_INTERVAL = 40  
SHOOT_INTERVAL = 65  # frames between each shot (2.5 seconds at 60fps)
PROJECTILE_DAMAGE = 20


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        self.entity_list.append(Background((0, 0), WIN_WIDTH, WIN_HEIGHT))
        self.player = Player((WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.entity_list.append(self.player)

        self.enemies: list[Enemy] = []
        self.projectiles: list[Projectile] = []
        self.spawn_timer = 0
        self.spawn_count = 0
        self.shoot_timer = 0
        self.current_spawn_interval = SPAWN_INTERVAL
        self.hud = HUD()

    def _spawn_enemy(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            pos = (random.randint(0, WIN_WIDTH), -32)
        elif side == 'bottom':
            pos = (random.randint(0, WIN_WIDTH), WIN_HEIGHT + 32)
        elif side == 'left':
            pos = (-32, random.randint(0, WIN_HEIGHT))
        else:
            pos = (WIN_WIDTH + 32, random.randint(0, WIN_HEIGHT))

        self.spawn_count += 1

        # Every 10 spawns, create a tank enemy
        if self.spawn_count % 10 == 0:
            self.enemies.append(TankEnemy(pos))
        else:
            self.enemies.append(Enemy(pos))
        

    def _get_closest_enemy(self) -> Enemy | None:
        if not self.enemies:
            return None
        return min(self.enemies, key=lambda e: (
            (e.rect.centerx - self.player.rect.centerx) ** 2 +
            (e.rect.centery - self.player.rect.centery) ** 2
        ))

    def _shoot(self):
        target = self._get_closest_enemy()
        if target:
            dx = target.rect.centerx - self.player.rect.centerx
            dy = target.rect.centery - self.player.rect.centery
            if math.hypot(dx, dy) > 0:  # only shoot if enemy is not on top of player
                self.projectiles.append(Projectile(self.player.rect, target.rect))

    def run_level(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "MENU"
                    
            # Progressive spawn
            self.spawn_timer += 1
            if self.spawn_timer >= self.current_spawn_interval and len(self.enemies) < ENEMY_LIMIT:
                self._spawn_enemy()
                self.spawn_timer = 0
                self.current_spawn_interval = max(30, SPAWN_INTERVAL - len(self.enemies) * 8)  

            # Auto shoot toward closest enemy
            self.shoot_timer += 1
            if self.shoot_timer >= SHOOT_INTERVAL:
                self._shoot()
                self.shoot_timer = 0

            # Move player
            self.player.move()

            # Move enemies and check collision with player
            for enemy in self.enemies:
                enemy.move(self.player.rect)

                # Damage collision
                if enemy.rect.inflate(enemy.damage_inflate, enemy.damage_inflate).colliderect(self.player.rect.inflate(-30, -30)):
                    self.player.take_damage()

                # Push enemy away from player (separation)
                if enemy.rect.inflate(-50, -50).colliderect(self.player.rect.inflate(-50, -50)):
                    dx = enemy.x - self.player.rect.centerx
                    dy = enemy.y - self.player.rect.centery
                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        dx, dy = 1, 0
                        dist = 1
                    push = 2
                    enemy.x += (dx / dist) * push
                    enemy.y += (dy / dist) * push
                    enemy.rect.centerx = int(enemy.x)
                    enemy.rect.centery = int(enemy.y)
                            
            # Separate overlapping enemies
            for i, enemy_a in enumerate(self.enemies):
                for enemy_b in self.enemies[i + 1:]:
                    if enemy_a.rect.inflate(-50, -50).colliderect(enemy_b.rect.inflate(-50, -50)):
                        dx = enemy_b.rect.centerx - enemy_a.rect.centerx
                        dy = enemy_b.rect.centery - enemy_a.rect.centery
                        dist = math.hypot(dx, dy)
                        if dist == 0:
                            dx, dy = 1, 0
                            dist = 1
                        push = 2
                        enemy_a.x -= (dx / dist) * push
                        enemy_a.y -= (dy / dist) * push
                        enemy_b.x += (dx / dist) * push
                        enemy_b.y += (dy / dist) * push
                        enemy_a.rect.centerx = int(enemy_a.x)
                        enemy_a.rect.centery = int(enemy_a.y)
                        enemy_b.rect.centerx = int(enemy_b.x)
                        enemy_b.rect.centery = int(enemy_b.y)

            # Update projectiles and check collision with enemies
            for projectile in self.projectiles:
                projectile.update(WIN_WIDTH, WIN_HEIGHT)
                for enemy in self.enemies:
                    if projectile.active and projectile.rect.colliderect(enemy.rect.inflate(-50, -50)):
                        enemy.take_damage(PROJECTILE_DAMAGE)
                        projectile.active = False

            # Remove inactive projectiles and dead enemies
            self.projectiles = [p for p in self.projectiles if p.active]
            self.enemies = [e for e in self.enemies if e.is_alive()]

            # Check if player is dead
            if not self.player.is_alive():
                return "DEAD"

            # Draw background and entities
            for entity in self.entity_list:
                if hasattr(entity, 'draw'):
                    entity.draw(self.window)
                else:
                    self.window.blit(entity.surf, entity.rect)

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.window)

            # Draw projectiles
            for projectile in self.projectiles:
                projectile.draw(self.window)

            # Draw HUD on top of everything
            self.hud.draw(self.window, self.player.hp)

            pygame.display.flip()
            clock.tick(60)