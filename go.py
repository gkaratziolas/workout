import pygame
import time
import random
import pyaudio
import wave
import threading
import time
import os

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000

warmup = [
    {
        "name": "Star Jumps",
        "duration_s": 30
    }, {
        "name": "High Knees",
        "duration_s": 30
    }, {
        "name": "Arm Circles (FWD)",
        "duration_s": 30
    }, {
        "name": "Arm Circles (BWD)",
        "duration_s": 30
    }, {
        "name": "Squats",
        "duration_s": 30
    }
]

main_circuit = [
    {
        "name": "Dumbell Squats",
        "duration_s": 60,
    }, {
        "name": "Push-Ups",
        "duration_s": 60
    }, {
        "name": "Bent Over Dumbbell Rows (Left)",
        "duration_s": 60
    }, {
        "name": "Bent Over Dumbbell Rows (Right)",
        "duration_s": 60
    }, {
        "name": "Dumbbell Lunges",
        "duration_s": 60
    }, {
        "name": "Chair Dips",
        "duration_s": 60
    }, {
        "name": "Crunches",
        "duration_s": 60
    }
]

cool_down = [
    {
        "name": "Shoulder Stretch",
        "duration_s": 60
    }, {
        "name": "Hamstring Stretch",
        "duration_s": 60
    }, {
        "name": "Quadriceps Stretch",
        "duration_s": 60
    }, {
        "name": "Triceps Stretch",
        "duration_s": 60
    }, {
        "name": "Deep Breathing and Relaxation",
        "duration_s": 60
    }
]

def play_audio(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    stream.stop_stream()
    stream.close()
    p.terminate()

def play_audio_nb(filename):
    audio_thread = threading.Thread(target=play_audio, args=(filename,))
    audio_thread.start()

# Use a thread to play audio
sound_dir = "C:\\Users\\meisg\\OneDrive\\Desktop\\Announcer\\Gameplay\\"
ready_sound_path = os.path.join(sound_dir, "00139 (0x02D2).wav")
go_sound_path = os.path.join(sound_dir, "00132 (0x0293).wav")
congratulations_sound_path = os.path.join(sound_dir, "00087 (0x0234).wav")
select_your_monkey_sound_path = os.path.join(sound_dir, "00179 (0x031B).wav")
goal_sound_path = os.path.join(sound_dir, "00131 (0x028A).wav")

# Initialize Pygame
pygame.init()

kaiti_path = "C:\\Windows\\Fonts\\simkai.ttf"
simsun_path = "C:\\Windows\\Fonts\\simsun.ttc"

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("3D Timer")

# Set up font
font_size = 60
#font = pygame.font.SysFont("Courier", font_size)
font = pygame.font.Font(simsun_path, font_size)
small_font = pygame.font.Font(simsun_path, 40)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

def draw_wobble_string(screen, s, x, y, colour=(0,0,0), small=False, wobble=2):
    f = font
    if small:
        f = small_font
    str_width, str_height = f.size(s)
    x_offset = -str_width / 2
    y_offset = -str_height / 2

    for c in s:
        c_render = f.render(c, True, colour)
        x0 = x + random.randint(-wobble, wobble) + x_offset
        y0 = y + random.randint(-wobble, wobble) + y_offset
        screen.blit(c_render, (x0, y0))
        char_width, char_height = f.size(c)
        x += char_width

play_audio_nb(ready_sound_path)
time.sleep(2)
play_audio_nb(go_sound_path)

running = True
start_time = time.time()

i = 0
main_circuit_loops = 2
ready_sounded = 0
rest_sounded = 0
transition_time = warmup[i]["duration_s"]

states = ["WARMUP", "MAIN", "COOLDOWN"]
state = "WARMUP"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate time elapsed
    elapsed_time = time.time() - start_time

    if state == "WARMUP":
        display = warmup[i]["name"]
        if i < len(warmup) - 1:
            display_next = warmup[i+1]["name"]
        else:
            display_next = main_circuit[0]["name"]

        if (transition_time - elapsed_time < 2) and not ready_sounded:
            ready_sounded = 1
            play_audio_nb(ready_sound_path)
        if (elapsed_time > transition_time):
            play_audio_nb(go_sound_path)
            ready_sounded = 0
            if (i < len(warmup) - 1):
                i += 1
                transition_time = elapsed_time + warmup[i]["duration_s"]
            else:
                state = "MAIN"
                i = 0
                transition_time = elapsed_time + main_circuit[i]["duration_s"]
                rest_time = transition_time - 15
                rest_sounded = 0

    elif state == "MAIN":
        if (elapsed_time > rest_time):
            display = "REST"
            if not rest_sounded:
                play_audio_nb(goal_sound_path)
                rest_sounded = 1
        else:
            display = main_circuit[i]["name"]

        if i < len(main_circuit) - 1:
            display_next = main_circuit[i+1]["name"]
        else:
            if (main_circuit_loops > 0):
                display_next = main_circuit[0]["name"]
            else:
                display_next = cool_down[0]["name"]

        if (transition_time - elapsed_time < 2) and not ready_sounded:
            ready_sounded = 1
            play_audio_nb(ready_sound_path)

        if (elapsed_time > transition_time):
            play_audio_nb(go_sound_path)
            ready_sounded = 0
            rest_sounded = 0
            if (i < len(main_circuit) - 1):
                i += 1
                transition_time = elapsed_time + main_circuit[i]["duration_s"]
                rest_time = transition_time - 15
            else:
                i = 0
                transition_time = elapsed_time + main_circuit[i]["duration_s"]
                rest_time = transition_time - 15
                main_circuit_loops -= 1
                if main_circuit_loops == 0:
                    state = "COOLDOWN"

    elif state == "COOLDOWN":
        display = cool_down[i]["name"]
        if i < len(cool_down) - 1:
            display_next = cool_down[i+1]["name"]
        else:
            display_next = "DONE"
        if (transition_time - elapsed_time < 2) and not ready_sounded:
            ready_sounded = 1
            play_audio_nb(ready_sound_path)
        if (elapsed_time > transition_time):
            play_audio_nb(go_sound_path)
            ready_sounded = 0
            if (i < len(cool_down) - 1):
                i += 1
                transition_time = elapsed_time + cool_down[i]["duration_s"]
            else:
                state = "CLOSE"
                i = 0
                transition_time = elapsed_time + cool_down[i]["duration_s"]
                rest_time = transition_time - 15
                rest_sounded = 0
    else:
        play_audio_nb(congratulations_sound_path)
        time.sleep(2)
        pygame.quit()


    # Render the text
    time_string = f"{int(elapsed_time / 60):02d}:{int(elapsed_time % 60):02d}"
    text_shadow = font.render(time_string, True, black)
    # Clear screen
    screen.fill(white)
    # Draw text

    if state == "WARMUP":
        draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, wobble=1)
        draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, colour=(240, 130, 20))
    elif state == "MAIN":
        if display == "REST":
            draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, wobble=1)
            draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, colour=(30, 30, 170), wobble=2)
        else:
            draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, wobble=2)
            draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, colour=(255, 0, 0), wobble=4)
    elif state == "COOLDOWN":
        draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400)
        draw_wobble_string(screen, str(display), WINDOW_WIDTH/2, 400, colour=(255, 0, 0))
        
    draw_wobble_string(screen, str(time_string), WINDOW_WIDTH/2, 500)
    draw_wobble_string(screen, "Next:" + str(display_next), WINDOW_WIDTH/2, 600, small=True)
    #screen.blit(text, (50, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()