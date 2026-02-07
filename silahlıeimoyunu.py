from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random, math

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.enabled = False

# ---------------- STATE ----------------
MAX_HEALTH = 100
player_health = MAX_HEALTH
score = 0
last_hit_time = 0
game_over = False

bots = []
bullets = []

# ---------------- UI ----------------
health_text = Text("", position=(-0.85, .45), scale=2, color=color.red)
score_text = Text("", position=(-0.85, .38), scale=1.5)

damage_overlay = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2),
    color=color.rgba(255, 0, 0, 0)
)

death_panel = Entity(parent=camera.ui, enabled=False)

Entity(parent=death_panel, model='quad',
       scale=(1.4, .8), color=color.black66)

Text(parent=death_panel, text="ÖLDÜN", scale=4, y=.15)
Text(parent=death_panel, text="R = Tekrar Oyna\nESC = Çık", y=-.2)

# ---------------- WORLD ----------------
Sky()

ground = Entity(
    model='plane',
    scale=200,
    collider='box',
    texture='white_cube',
    texture_scale=(100, 100),
    color=color.dark_gray
)

# ---------------- PLAYER ----------------
player = FirstPersonController(speed=12)
player.cursor.color = color.red

# ---------------- GUN ----------------
gun = Entity(parent=camera, position=(.6, -.45, 1))

Entity(parent=gun, model='cube',
       scale=(.35, .25, 1.2),
       color=color.gray)

Entity(parent=gun, model='cylinder',
       scale=(.12, .12, .9),
       z=.8,
       rotation=(90, 0, 0),
       color=color.dark_gray)

Entity(parent=gun, model='cube',
       scale=(.2, .12, .4),
       y=.22,
       z=.2,
       color=color.black)

# ---------------- BOT SPAWN ----------------
def spawn_bot():
    dist = random.randint(20, 40)
    angle = player.rotation_y + random.uniform(-70, 70)

    rad = math.radians(angle)
    x = player.x + math.sin(rad) * dist
    z = player.z + math.cos(rad) * dist

    bot = Entity(position=(x, 1.5, z))

    Entity(parent=bot, model='cube',
           scale=(1.5, 2, 1),
           color=color.azure)

    head = Entity(parent=bot, model='cube',
                  scale=(1, 1, 1),
                  y=1.8,
                  color=color.light_gray)

    Entity(parent=head, model='sphere',
           scale=.15, x=-.25, z=-.55,
           color=color.red)

    Entity(parent=head, model='sphere',
           scale=.15, x=.25, z=-.55,
           color=color.red)

    Entity(parent=head, model='cylinder',
           scale=(.1, .5, .1),
           y=.8,
           color=color.yellow)

    bot.collider = 'box'
    bots.append(bot)

# ---------------- SPAWN WAVE ----------------
def spawn_wave(n=6):
    for _ in range(n):
        spawn_bot()

# ---------------- RESET ----------------
def reset_game():
    global player_health, score, game_over

    for b in bots:
        destroy(b)
    bots.clear()

    for b in bullets:
        destroy(b)
    bullets.clear()

    player_health = MAX_HEALTH
    score = 0
    game_over = False

    player.position = (0, 1, 0)
    player.enabled = True
    mouse.locked = True

    death_panel.enabled = False

    health_text.text = f"CAN: {player_health}"
    score_text.text = f"SKOR: {score}"

    spawn_wave()

# ---------------- INPUT ----------------
def input(key):
    global game_over

    if game_over:
        if key == 'r':
            reset_game()
        return

    if key == 'left mouse down':
        gun.animate_rotation((0, 0, -4), duration=.05)
        gun.animate_rotation((0, 0, 0), duration=.05, delay=.05)

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

# ---------------- UPDATE ----------------
def update():
    global player_health, score, last_hit_time, game_over

    if game_over:
        return

    # ---------- BULLETS ----------
    for b in bullets[:]:

        if not b or not b.enabled:
            if b in bullets:
                bullets.remove(b)
            continue

        try:
            b.position += b.forward * 75 * time.dt
        except:
            if b in bullets:
                bullets.remove(b)
            continue

        hit = b.intersects()

        if hit.hit:

            if hit.entity in bots:
                bot = hit.entity

                if bot in bots:
                    bots.remove(bot)
                destroy(bot)
                spawn_bot()

                score += 1
                score_text.text = f"SKOR: {score}"

            if b in bullets:
                bullets.remove(b)
            destroy(b)

    # ---------- BOTS ----------
    for bot in bots[:]:

        if not bot or not bot.enabled:
            if bot in bots:
                bots.remove(bot)
            continue

        bot.look_at(player.position)
        bot.rotation_x = 0

        if distance(bot.position, player.position) > 3.5:
            bot.position += bot.forward * 6 * time.dt

        else:
            if time.time() - last_hit_time > 1:

                player_health -= 15
                last_hit_time = time.time()

                health_text.text = f"CAN: {player_health}"

                camera.shake(.2, 2)

                damage_overlay.color = color.rgba(255, 0, 0, 120)
                damage_overlay.animate_color(
                    color.rgba(255, 0, 0, 0),
                    duration=.4
                )

    # ---------- DEATH ----------
    if player_health <= 0 and not game_over:
        game_over = True
        death_panel.enabled = True
        player.enabled = False
        mouse.locked = False


# ---------------- START ----------------
spawn_wave()

health_text.text = f"CAN: {player_health}"
score_text.text = f"SKOR: {score}"

app.run()
