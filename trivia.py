import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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
sound = None
sound_played = False

# Load the background music file and set the volume
pygame.mixer.music.load("sounds/dearly_beloved.mp3")
pygame.mixer.music.set_volume(0.5)

# Play the background music indefinitely
pygame.mixer.music.play(-1)

# Score tracking
scores = {'text': 0, 'picture': 0, 'sound': 0}
current_question_index = 0
answered = False  # Flag to indicate if the current question has been answered

# Answer button dimensions
button_width = 100
button_height = 50
true_button_pos = (screen_width // 3 - button_width // 2, 400)
false_button_pos = (2 * screen_width // 3 - button_width // 2, 400)

quadrants = [(screen_width / 4, 3 * screen_height / 4),  # Top-left
                 (3 * screen_width / 4, 3 * screen_height / 4),  # Top-right
                 (screen_width / 4, 7 * screen_height / 8),  # Bottom-left
                 (3 * screen_width / 4, 7 * screen_height / 8)]  # Bottom-right

# Clouds data
clouds = [{
    'x': random.randint(0, screen_width),
    'y': random.randint(0, screen_height),
    'width': random.randint(60, 100),
    'height': random.randint(30, 60),
    'speed': random.uniform(.02, .1)
} for _ in range(50)]  # Generate 5 clouds with random properties

# Load a cloud texture image
cloud_texture = pygame.image.load("pics/cloud_texture.jpg")
# Define a function to draw a tufted cloud with a given center and size
def draw_tufted_cloud(center, size):
    # Calculate the radius of the cloud
    radius = size / 2
    # Draw four ellipses with different offsets and scales
    offsets = [(-radius / 2, -radius / 2), (radius / 4, -radius / 4), (-radius / 4, radius / 4), (radius / 2, radius / 2)]
    scales = [0.75, 0.5, 0.5, 0.75]
    for offset, scale in zip(offsets, scales):
        # Calculate the position and dimensions of the ellipse
        x = center[0] + offset[0]
        y = center[1] + offset[1]
        width = size * scale
        height = size * scale
        # Create a surface to draw the ellipse on
        ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw the ellipse with white color and alpha blending
        pygame.draw.ellipse(ellipse_surface, (255, 255, 255, 128), (0, 0, width, height))
        # Blit the cloud texture onto the ellipse surface with alpha blending
        ellipse_surface.blit(cloud_texture, (0, 0), None, pygame.BLEND_RGBA_MULT)
        # Blit the ellipse surface onto the screen with alpha blending
        screen.blit(ellipse_surface, (x, y), None, pygame.BLEND_RGBA_ADD)

# Define a function to draw multiple tufted clouds with random properties
def draw_tufted_clouds():
    for cloud in clouds:
        # Draw a tufted cloud with the same center and size as the original cloud
        draw_tufted_cloud((cloud['x'] + cloud['width'] / 2, cloud['y'] + cloud['height'] / 2), cloud['width'])

def draw_clouds():
    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE, pygame.Rect(cloud['x'], cloud['y'], cloud['width'], cloud['height']))

def move_clouds():
    for cloud in clouds:
        cloud['x'] += cloud['speed']
        if cloud['x'] > screen_width:  # Reset cloud to the left side
            cloud['x'] = -cloud['width']
            cloud['y'] = random.randint(50, 150)  # Jittered Y-value
last_image_path = None
last_image_object = None

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
            elif question_type == "sound":
                # Assuming the image path is always the second part for picture questions
                sound_path = parts[1]
                image_path = parts[2]
                # Question content starts from the third part up to the last four parts (answers)
                question_content = ' '.join(parts[3:-4])
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
            elif question_type == "sound":
                questions.append((question_type, sound_path, image_path, question_content, all_answers, correct_answer))            
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

def draw_picture_q(image, question, answers, correct_answer):
    global answered, scores  # Add this line to use the global 'answered' variable
    try:
        # Calculate the position to center the image on the screen
        image_x = (screen_width - 400) // 2
        image_y = (screen_height - 300) // 2 - 50  # Adjust Y position as needed

        # Display the resized image
        screen.blit(image, (image_x, image_y))
    except pygame.error as e:
        print(f"Error loading image: {e}")

    draw_text(question, font, BLACK, screen, screen_width / 4, screen_height / 20)  # Adjust Y based on image size
    
    button_width, button_height = 200, 50

    for i, answer in enumerate(answers):
        x, y = quadrants[i][0] - button_width / 2, quadrants[i][1] - button_height / 2
        if draw_button(answer, x, y, button_width, button_height, YELLOW, BLACK):
            if answer == correct_answer and not answered:
                scores['picture'] += 1
                answered = True
            break  # Exit after one click to prevent multiple score increments

def draw_sound_q(image, question, answers, correct_answer):
    global answered, scores  # Add this line to use the global 'answered' variable
    # try:
    #     sound = pygame.mixer.Sound(sound_path)
    #     sound.set_volume(0.5) # Set the volume to 50%
    #     sound.play()
    # except pygame.error as e:
    #     print(f"Error playing sound: {e}")

    try:
        image_x = (screen_width - 400) // 2
        image_y = (screen_height - 300) // 2 - 50  # Adjust Y position as needed

        # Display the resized image
        screen.blit(image, (image_x, image_y))
    except pygame.error as e:
        print(f"Error loading image: {e}")

    draw_text(question, font, BLACK, screen, 20, 20)
    button_width, button_height = 200, 50

    for i, answer in enumerate(answers):
        x, y = quadrants[i][0] - button_width / 2, quadrants[i][1] - button_height / 2
        if draw_button(answer, x, y, button_width, button_height, YELLOW, BLACK):
            if answer == correct_answer and not answered:
                scores['sound'] += 1
                answered = True
            break  # Exit after one click to prevent multiple score increments
            

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

def draw_title_screen(screen):
    title_font = pygame.font.Font(None, 74)  # Adjust font and size as needed
    button_font = pygame.font.Font(None, 50)  # Adjust font and size as needed

    title_text = title_font.render('Namtrivia!', True, (255, 255, 255))  # Adjust color as needed
    play_button_text = button_font.render('Play', True, (0, 0, 0))  # Adjust color as needed

    title_text_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 3))
    play_button_rect = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2, 100, 50)  # Adjust position and size as needed

    running = True
    while running:
        screen.fill((0, 102, 204))  # Adjust background color as needed
        screen.blit(title_text, title_text_rect)

        # Draw play button (simple rectangle here, you might want to make it fancier)
        pygame.draw.rect(screen, (255, 255, 255), play_button_rect)  # Adjust button color as needed
        screen.blit(play_button_text, (play_button_rect.x + 10, play_button_rect.y + 10))  # Adjust text position as needed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Control frame rate


# Main game loop
def main():
    global current_question_index, answered, sound, sound_played
    running = True
    questions = load_questions('questions.txt')
    pygame.display.set_caption('Namtrivia!')

    draw_title_screen(screen) 
    while running:
        screen.fill(SOFT_BLUE)
        # draw_scores()
        
        draw_clouds()
        move_clouds()

        if current_question_index < len(questions):
            
            # print(questions[current_question_index])
            # Now, use shuffled_answers directly, which already includes the correct answer mixed with wrong ones
            question_type = questions[current_question_index][0]
            global last_image_path, last_image_object  # Use global variables if they are defined outside the function
            
            if question_type == 'text':
                question_type, question_content, shuffled_answers, correct_answer = questions[current_question_index]
                draw_text_q(question_content, shuffled_answers, correct_answer)
            elif question_type == 'picture':
                # Ensure the function call aligns with how you've adjusted the question structure
                question_type, image_path, question_content, shuffled_answers, correct_answer = questions[current_question_index]
                    # Check if the current image is different from the last loaded image

                if image_path != last_image_path:
                    try:
                        last_image_object = pygame.image.load(image_path) # Load and store the new image
                        # Resize the image to new dimensions (e.g., 400x300 pixels)
                        last_image_object = pygame.transform.scale(last_image_object, (400, 300))
                        last_image_path = image_path  # Update the last image path
                    except pygame.error as e:
                        print(f"Error loading image: {e}")
                        last_image_object = None  # In case of error, ensure no invalid image is used
                # If the image path is the same, last_image_object already contains the correct image, so do nothing

                draw_picture_q(last_image_object, question_content, shuffled_answers, correct_answer)

            elif question_type == 'sound':
                question_type, sound_path, image_path, question_content, shuffled_answers, correct_answer = questions[current_question_index]
                if sound is None:
                    try:
                        pygame.mixer.music.stop()
                        sound = pygame.mixer.Sound(sound_path)
                        sound.set_volume(0.5) # Set the volume to 50%
                        sound.play()
                        sound_played = True
                    except pygame.error as e:
                        print(f"Error playing sound: {e}")

                if image_path != last_image_path:
                    try:
                        last_image_object = pygame.image.load(image_path) # Load and store the new image
                        # Resize the image to new dimensions (e.g., 400x300 pixels)
                        last_image_object = pygame.transform.scale(last_image_object, (400, 300))
                        last_image_path = image_path  # Update the last image path
                    except pygame.error as e:
                        print(f"Error loading image: {e}")
                        last_image_object = None  # In case of error, ensure no invalid image is used
                # If the image path is the same, last_image_object already contains the correct image, so do nothing

                draw_sound_q(last_image_object, question_content, shuffled_answers, correct_answer)

        if answered:
            # Optional: Display feedback for a few seconds
                # Display feedback for a correct answer
            feedback_font = pygame.font.Font(None, 50)  # Adjust font and size as needed
            feedback_color = (0, 255, 0)  # Green color for correct feedback
            feedback_text = "Correct!"
            feedback_x = screen.get_width() / 2  # Center horizontally
            feedback_y = screen.get_height() / 2  # Center vertically

            # Center the text on the screen. You might need to adjust the x and y to fit your game's UI better.
            draw_text(feedback_text, feedback_font, feedback_color, screen, feedback_x, feedback_y, align="center")
            pygame.display.flip()
            pygame.time.wait(2000)  # 2 seconds, for example
            current_question_index += 1
            answered = False  # Reset for the next question
            if sound_played:
                pygame.mixer.stop()
                sound = None
                sound_played = False
                pygame.mixer.music.play(-1) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
