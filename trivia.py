import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (153, 0, 153)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
SOFT_BLUE = (135, 206, 235)  # Sky Blue
PALE_GREEN = (152, 251, 152)  # Pale Green
LIGHT_BEIGE = (245, 245, 220)  # Beige

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
running = True
question = "The Eiffel Tower is in Paris."
answer = True  # True or False
user_answer = None

# Score tracking
scores = {'text': 0, 'picture': 0, 'sound': 0}
current_question_index = 0
answered = False  # Flag to indicate if the current question has been answered

# Answer button dimensions
button_width = 100
button_height = 50
true_button_pos = (screen_width // 3 - button_width // 2, 400)
false_button_pos = (2 * screen_width // 3 - button_width // 2, 400)

# Load questions
def load_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            question_type = parts[0]

            if question_type == "picture":
                # Assuming the image path is always the second part for picture questions
                image_path = parts[1]
                # Question content starts from the third part up to the last four parts (answers)
                question_content = ' '.join(parts[2:-4])
                # The rest of the logic remains the same
            else:
                # For non-picture questions, adjust as needed
                question_content = ' '.join(parts[1:-4])

            correct_answer = parts[-4]
            wrong_answers = parts[-3:]
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)  # Shuffle here

            if question_type == "picture":
                questions.append((question_type, image_path, question_content, all_answers, correct_answer))
            else:
                questions.append((question_type, question_content, all_answers, correct_answer))
    return questions


def draw_scores():
    score_text = f"Scores - Text: {scores['text']}, Picture: {scores['picture']}, Sound: {scores['sound']}"
    draw_text(score_text, font, BLACK, screen, screen_width - 10, screen_height - 30, align="right")

import random

def draw_text_q(question, answers, correct_answer):
    global answered, scores

    draw_text(question, font, BLACK, screen, screen_width / 4, screen_height / 5)
    quadrants = [(screen_width / 4, 3 * screen_height / 4),  # Top-left
                 (3 * screen_width / 4, 3 * screen_height / 4),  # Top-right
                 (screen_width / 4, 7 * screen_height / 8),  # Bottom-left
                 (3 * screen_width / 4, 7 * screen_height / 8)]  # Bottom-right
    button_width, button_height = 200, 50

    for i, answer in enumerate(answers):
        x, y = quadrants[i][0] - button_width / 2, quadrants[i][1] - button_height / 2
        if draw_button(answer, x, y, button_width, button_height, YELLOW, BLACK):
            if answer == correct_answer and not answered:
                scores['text'] += 1
                answered = True
            break  # Exit after one click to prevent multiple score increments

def draw_text(text, font, color, surface, x, y, align="left"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "right":
        textrect.topright = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_picture_q(image_path, question, answers, correct_answer):
    try:
        image = pygame.image.load(image_path)
        screen.blit(image, (20, 20))  # Adjust position as needed
    except pygame.error as e:
        print(f"Error loading image: {e}")

    draw_text(question, font, BLACK, screen, 20, 220)  # Adjust Y based on image size
    button_height = 50
    spacing = 10  # Space between buttons
    for i, answer in enumerate(answers):
        y = 300 + i * (button_height + spacing)  # Adjust starting Y based on text position
        if draw_button(answer, 20, y, 200, button_height, YELLOW, BLACK):
            print(f"Clicked on: {answer}")  # Placeholder for handling click

def draw_sound_q(sound_path, question, answers, correct_answer):
    try:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

    draw_text(question, font, BLACK, screen, 20, 20)
    button_height = 50
    spacing = 10
    for i, answer in enumerate(answers):
        y = 300 + i * (button_height + spacing)  # Adjust starting Y based on text position
        if draw_button(answer, 20, y, 200, button_height, WHITE, BLACK):
            print(f"Clicked on: {answer}")  # Placeholder for handling click
            

def draw_button(text, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)

    # Draw the button
    pygame.draw.rect(screen, ic, button_rect)

    # Highlight rim if mouse hovers
    if button_rect.collidepoint(mouse[0], mouse[1]):
        pygame.draw.rect(screen, ac, button_rect, 4)  # Only border highlighted

    # Button text
    textSurf, textRect = text_objects(text, font)
    textRect.center = (x + w / 2, y + h / 2)
    screen.blit(textSurf, textRect)

    # Return True if clicked
    return button_rect.collidepoint(mouse[0], mouse[1]) and click[0] == 1

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def button_true():
    global user_answer
    user_answer = True

def button_false():
    global user_answer
    user_answer = False

# Clouds data
clouds = [{
    'x': random.randint(0, screen_width),
    'y': random.randint(50, 150),
    'width': random.randint(60, 100),
    'height': random.randint(30, 60),
    'speed': random.uniform(0.02, .1)
} for _ in range(5)]  # Generate 5 clouds with random properties

def draw_clouds():
    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE, pygame.Rect(cloud['x'], cloud['y'], cloud['width'], cloud['height']))

def move_clouds():
    for cloud in clouds:
        cloud['x'] += cloud['speed']
        if cloud['x'] > screen_width:  # Reset cloud to the left side
            cloud['x'] = -cloud['width']
            cloud['y'] = random.randint(50, 150)  # Jittered Y-value

# Main game loop
def main():
    global current_question_index, answered
    running = True
    questions = load_questions('questions.txt')

    while running:
        screen.fill(SOFT_BLUE)
        # draw_scores()

        if current_question_index < len(questions):
            print(questions[current_question_index])
            # Now, use shuffled_answers directly, which already includes the correct answer mixed with wrong ones
            question_type = questions[current_question_index][0]

            if question_type == 'text':
                question_type, question_content, shuffled_answers, correct_answer = questions[current_question_index]
                draw_text_q(question_content, shuffled_answers, correct_answer)
            elif question_type == 'picture':
                # Ensure the function call aligns with how you've adjusted the question structure
                question_type, image_path, question_content, shuffled_answers, correct_answer = questions[current_question_index]
                draw_picture_q(image_path, image_path, shuffled_answers, correct_answer)

            elif question_type == 'sound':
                draw_sound_q(question_content, "What sound is this?", shuffled_answers, correct_answer)

        if answered:
            # Optional: Display feedback for a few seconds
            pygame.time.wait(2000)  # 2 seconds, for example
            current_question_index += 1
            answered = False  # Reset for the next question

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
