from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.enabled = False

# --------------------
# GLOBAL STATE
# --------------------
player_health = 100
score = 0
last_hit_time = 0
game_over = False

bots = []
bullets = []

# --------------------
# UI
# --------------------
health_text = Text("", position=(-0.85, .45), scale=2, color=color.red)
score_text = Text("", position=(-0.85, .38), scale=1.5)

damage_overlay = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2),
    color=color.rgba(255, 0, 0, 0)
)

death_panel = Entity(parent=camera.ui, enabled=False)

death_bg = Entity(
    parent=death_panel,
    model='quad',
    scale=(1.5, .9),
    color=color.black66
)

death_text = Text(
    parent=death_panel,
    text="ÖLDÜN",
    scale=4,
    origin=(0, 0.2)
)

restart_hint = Text(
    parent=death_panel,
    text="R = Tekrar Oyna\nESC = Çık",
    y=-.2,
    scale=1.5
)

# --------------------
# WORLD
# --------------------
Sky()

ground = Entity(
    model='plane',
    scale=200,
    collider='box',
    texture='white_cube',
    texture_scale=(100, 100),
    color=color.dark_gray
)

# --------------------
# PLAYER
# --------------------
player = FirstPersonController(speed=12)
player.cursor.color = color.red

gun = Entity(
    parent=camera,
    model='cube',
    position=(.6, -.5, 1),
    scale=(.2, .2, 1),
    color=color.black
)

# --------------------
# BOT SYSTEM
# --------------------
def spawn_bot():
    dist = random.randint(20, 40)
    angle = player.rotation_y + random.uniform(-70, 70)

    rad = math.radians(angle)

    x = player.x + math.sin(rad) * dist
    z = player.z + math.cos(rad) * dist

    bot = Entity(
        model='cube',
        color=color.red,
        scale=(1.5, 3, 1.5),
        position=(x, 1.5, z),
        collider='box'
    )

    bots.append(bot)


def spawn_wave(count=6):
    for _ in range(count):
        spawn_bot()

# --------------------
# RESET GAME
# --------------------
def reset_game():
    global player_health, score, game_over

    for b in bots:
        destroy(b)
    bots.clear()

    for b in bullets:
        destroy(b)
    bullets.clear()

    player_health = 100
    score = 0
    game_over = False

    health_text.color = color.red
    player.enabled = True
    mouse.locked = True

    death_panel.enabled = False

    spawn_wave()

# --------------------
# SHOOTING
# --------------------
def input(key):
    global game_over

    if game_over:
        if key == 'r':
            reset_game()
        return

    if key == 'left mouse down':
        gun.blink(color.yellow, duration=.1)

        bullet = Entity(
            model='sphere',
            scale=.3,
            color=color.orange,
            position=gun.world_position,
            rotation=camera.world_rotation,
            collider='sphere'
        )

        bullets.append(bullet)

        destroy(bullet, delay=2)

# --------------------
# UPDATE LOOP
# --------------------
def update():
    global player_health, score, last_hit_time, game_over

    if game_over:
        return

    # ---- BULLETS ----
    for b in bullets[:]:

        if not b or not b.enabled:
            if b in bullets:
                bullets.remove(b)
            continue

        b.position += b.forward * 70 * time.dt

        hit = b.intersects()

        if hit.hit and hit.entity in bots:

            score += 1
            score_text.text = f"SKOR: {score}"

            bot = hit.entity
            bots.remove(bot)
            destroy(bot)

            spawn_bot()

            bullets.remove(b)
            destroy(b)

    # ---- BOTS ----
    for bot in bots:

        bot.look_at(player.position)
        bot.rotation_x = 0

        dist = distance(bot.position, player.position)

        if dist > 3.5:
            bot.position += bot.forward * 6 * time.dt

        else:
            if time.time() - last_hit_time > 1:

                player_health -= 20
                last_hit_time = time.time()

                health_text.text = f"CAN: {player_health}"

                camera.shake(.2, 2)

                damage_overlay.color = color.rgba(255, 0, 0, 120)
                damage_overlay.animate_color(
                    color.rgba(255, 0, 0, 0),
                    duration=.4
                )

    # ---- DEATH ----
    if player_health <= 0:

        game_over = True

        death_panel.enabled = True
        player.enabled = False
        mouse.locked = False

        health_text.text = "ÖLDÜN"
        health_text.color = color.black


# --------------------
# START
# --------------------
spawn_wave()

health_text.text = f"CAN: {player_health}"
score_text.text = f"SKOR: {score}"

app.run()


