import pygame
import pygame_menu
import random
from numba import jit
import os
from constants import *


clock = pygame.time.Clock()
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm")
pygame.display.update()

ARRAY_GENERATION_MODE = 'random'

# UI
TOP_BAR_OFFSET = 0 # sets the space between the highest bar and the top of the screen
RAND_ARRAY_SIZE = 100
RAND_ARRAY_MIN = 0
RAND_ARRAY_MAX = 100
BAR_THICKNESS = 1

# load images
settings_image = pygame.image.load(os.path.join("Assets", "Settings.jpg")).convert()
settings_image = pygame.transform.scale(settings_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
settings_image_pos = (0, int(HEIGHT/NUM_IMAGES*0))

selection_sorting_image = pygame.image.load(os.path.join("Assets", "selection_sorting.jpg")).convert()
selection_sorting_image = pygame.transform.scale(selection_sorting_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
selection_sorting_image_pos = (0, int(HEIGHT/NUM_IMAGES*1))

bubble_sort_image = pygame.image.load(os.path.join("Assets", "Bubble_Sort.jpg")).convert()
bubble_sort_image = pygame.transform.scale(bubble_sort_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
bubble_sort_image_pos = (0, int(HEIGHT/NUM_IMAGES*2)) # *1 means second in order

# quick_sort_image = pygame.image.load("Quick_Sort.jpg").convert()
# quick_sort_image = pygame.transform.scale(quick_sort_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
# quick_sort_image_pos = (0, int(HEIGHT/NUM_IMAGES*3))

insertion_sort_image = pygame.image.load(os.path.join("Assets", "Insertion_Sort.jpg")).convert()
insertion_sort_image = pygame.transform.scale(insertion_sort_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
insertion_sort_image_pos = (0, int(HEIGHT/NUM_IMAGES*3))

cocktail_shaker_sort_image = pygame.image.load(os.path.join("Assets", "Cocktail_Shaker_sort.jpg")).convert()
cocktail_shaker_sort_image = pygame.transform.scale(cocktail_shaker_sort_image, (WIDTH, int(HEIGHT/NUM_IMAGES)))
cocktail_shaker_sort_image_pos = (0, int(HEIGHT/NUM_IMAGES*4))


# generates array with predefined size and range
def generate_rand_array(array_size, range_start, range_end, generation_mode):
    if generation_mode == 'random':
        return [random.randint(range_start, range_end) for x in range(array_size)]
    elif generation_mode == 'reversed':
        return sorted([random.randint(range_start, range_end) for x in range(array_size)], reverse=True)
    elif generation_mode == 'semi-sorted':
        output_array = sorted([random.randint(range_start, range_end) for x in range(array_size)])
        for x in range(array_size//4): # get 25% unsorted
            output_array[random.randint(0, array_size-1)] = output_array[random.randint(0, array_size-1)]
        return output_array

# value_max - value_min != 0
@jit(nopython=True)
def convert_ranges(value, value_min, value_max, new_min, new_max):
    return (((value - value_min) * (new_max - new_min)) / (value_max - value_min)) + new_min

# displays given array to pygame window starting from bottom left corner and filling up entire floor

def display_array(array, highlight_index=0):
    min_array = min(array)
    max_array = max(array)
    arr_len = len(array)
    rect_width = WIDTH/arr_len
    bar_color = BAR_COLOR
    for num_index, num in enumerate(array):
        if num_index == highlight_index:
            bar_color = RED
        else:
            bar_color = BAR_COLOR
        # rect position arguments
        left = num_index*rect_width
        rect_height = convert_ranges(num, min_array, max_array, 0, HEIGHT)
        top = HEIGHT - rect_height
        pygame.draw.rect(WIN, bar_color, (left, top+TOP_BAR_OFFSET, rect_width, rect_height), BAR_THICKNESS)


# pause game, no events
def pause_menu_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    return

def settings_loop():

    menu = pygame_menu.Menu('Settings', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)

    def set_array_size(value, size):
        global RAND_ARRAY_SIZE, RAND_ARRAY_SIZE, RAND_ARRAY_MAX
        RAND_ARRAY_SIZE = size
        RAND_ARRAY_MIN = 0
        RAND_ARRAY_MAX = size
    def set_delay(value, delay):
        global DELAY
        DELAY = delay

    def start_the_game():
        menu.disable()

    def set_bar_fill_option(value, num):
        global BAR_THICKNESS
        BAR_THICKNESS = num

    def set_bar_color(color):
        global BAR_COLOR
        BAR_COLOR = color

    def set_background_color(color):
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = color

    def set_generation_mode(value, mode):
        global ARRAY_GENERATION_MODE
        ARRAY_GENERATION_MODE = mode

    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.selector('Array Size:', [('Small', 10), ('Medium', 100), ('Large', 1000)], onchange=set_array_size)
    menu.add.selector('Delay:', [('Slow', 1000), ('Normal', 100), ('Fast', 0)], onchange=set_delay)
    menu.add.selector('Bar Mode:', [('Fill', 0), ('Hollow', 1)], onchange=set_bar_fill_option)
    menu.add.selector('Array config:', [('Random', 'random'), ('Reversed', 'reversed'), ('Semi-sorted', 'semi-sorted')], onchange=set_generation_mode)
    menu.add.color_input(title='Bar Color:', color_type='rgb', onchange=set_bar_color)
    menu.add.color_input(title='Background Color:', color_type='rgb', onchange=set_background_color)


    menu.mainloop(WIN)

def selection_sort_step(array, current_index):
    min_value = array[current_index]
    min_index = current_index
    for x in range(current_index+1, len(array)):
        if array[x] < min_value:
            min_value = array[x]
            min_index = x

    array[current_index], array[min_index] = array[min_index], array[current_index]
    return array


def selection_sort_loop():
    rand_array = generate_rand_array(RAND_ARRAY_SIZE, RAND_ARRAY_MIN, RAND_ARRAY_MAX, ARRAY_GENERATION_MODE)
    
    current_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    pause_menu_loop()

        pygame.time.delay(DELAY)

        if current_index == len(rand_array)-1:
            current_index = 0
        if sorted(rand_array) != rand_array:
            rand_array = selection_sort_step(rand_array, current_index)
            current_index += 1
        else:
            current_index = 0
            running = False
            return
        WIN.fill(BACKGROUND_COLOR)
        display_array(rand_array, current_index)
        pygame.display.update()
        clock.tick(FPS)

def bubble_sort_step(array, current_index):
    if array[current_index + 1] < array[current_index]:
        array[current_index + 1],  array[current_index] = array[current_index], array[current_index + 1]
    return array


def bubble_sort_loop():
    rand_array = generate_rand_array(RAND_ARRAY_SIZE, RAND_ARRAY_MIN, RAND_ARRAY_MAX, ARRAY_GENERATION_MODE)
    
    num_times_hit_right = 0
    current_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    pause_menu_loop()

        pygame.time.delay(DELAY)

        if current_index == len(rand_array)-1 - num_times_hit_right:
            current_index = 0
            num_times_hit_right += 1
        if sorted(rand_array) != rand_array:
            rand_array = bubble_sort_step(rand_array, current_index)
            current_index += 1
        else:
            current_index = 0
            running = False
            return
        WIN.fill(BACKGROUND_COLOR)
        display_array(rand_array, current_index)
        pygame.display.update()
        clock.tick(FPS)

# def quick_sort_loop():
#     pass


def insertion_sort_step(array, current_index):
    back_index = current_index - 1
    while back_index >= 0 and array[current_index] < array[back_index]:
        array[current_index], array[back_index] = array[back_index], array[current_index]
        current_index -= 1
        back_index = current_index - 1
        pygame.time.delay(DELAY)
        WIN.fill(BACKGROUND_COLOR)
        display_array(array, current_index)
        pygame.display.update()
        clock.tick(FPS)

    array[back_index + 1] = array[current_index]
    return array

def insertion_sort_loop():
    rand_array = generate_rand_array(RAND_ARRAY_SIZE, RAND_ARRAY_MIN, RAND_ARRAY_MAX, ARRAY_GENERATION_MODE)
    
    current_index = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    pause_menu_loop()

        pygame.time.delay(DELAY)

        if current_index == len(rand_array):
            return
        if sorted(rand_array) != rand_array:
            rand_array = insertion_sort_step(rand_array, current_index)
            current_index += 1
        else:
            current_index = 0
            return

        WIN.fill(BACKGROUND_COLOR)
        display_array(rand_array, current_index)
        pygame.display.update()
        clock.tick(FPS)

def cocktail_shaker_sort_step(array, current_index, moving_right):
    if moving_right:
        if array[current_index + 1] < array[current_index]:
            array[current_index + 1],  array[current_index] = array[current_index], array[current_index + 1]
    else:
        if array[current_index - 1] > array[current_index]:
            array[current_index - 1],  array[current_index] = array[current_index], array[current_index - 1]
    return array

def cocktail_shaker_sort_loop():
    rand_array = generate_rand_array(RAND_ARRAY_SIZE, RAND_ARRAY_MIN, RAND_ARRAY_MAX, ARRAY_GENERATION_MODE)
    moving_right = True
    num_times_hit_left = 0
    num_times_hit_right = 0
    left_count_changed = True
    right_count_changed = False
    current_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    pause_menu_loop()

        pygame.time.delay(DELAY)

        if current_index == len(rand_array)-1 - num_times_hit_right:
            if left_count_changed and not right_count_changed:
                num_times_hit_right += 1
                right_count_changed = True
                left_count_changed = False
                moving_right = False
        
        if current_index == num_times_hit_left:
            if right_count_changed and not left_count_changed:
                num_times_hit_left += 1
                right_count_changed =  False
                left_count_changed = True
                moving_right = True
            
        if sorted(rand_array) != rand_array:
            rand_array = cocktail_shaker_sort_step(rand_array, current_index, moving_right)
            if moving_right:
                current_index += 1
            else:
                current_index -= 1
        else:
            current_index = 0
            running = False
            return
        WIN.fill(BACKGROUND_COLOR)
        display_array(rand_array, current_index)
        pygame.display.update()
        clock.tick(FPS)

def show_main_menu():
    global selection_sorting_image_blit
    global bubble_sort_image_blit
    # global quick_sort_image_blit
    global settings_image_blit
    global insertion_sort_image_blit
    global cocktail_shaker_sort_image_blit

    WIN.fill(BACKGROUND_COLOR)
    selection_sorting_image_blit = WIN.blit(selection_sorting_image, (selection_sorting_image_pos[0], selection_sorting_image_pos[1]))
    bubble_sort_image_blit = WIN.blit(bubble_sort_image, (bubble_sort_image_pos[0], bubble_sort_image_pos[1]))
    # quick_sort_image_blit = WIN.blit(quick_sort_image, (quick_sort_image_pos[0], quick_sort_image_pos[1]))
    insertion_sort_image_blit = WIN.blit(insertion_sort_image, (insertion_sort_image_pos[0], insertion_sort_image_pos[1]))
    cocktail_shaker_sort_image_blit = WIN.blit(cocktail_shaker_sort_image, (cocktail_shaker_sort_image_pos[0], cocktail_shaker_sort_image_pos[1]))
    settings_image_blit = WIN.blit(settings_image, (settings_image_pos[0], settings_image_pos[1]))


def main():
    running = True
    show_main_menu()
    pygame.display.update()
    clock.tick(FPS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selection_sorting_image_blit.collidepoint(event.pos):
                    selection_sort_loop()

                elif bubble_sort_image_blit.collidepoint(event.pos):
                    bubble_sort_loop()

                # elif quick_sort_image_blit.collidepoint(event.pos):
                    # quick_sort_loop()

                elif settings_image_blit.collidepoint(event.pos):
                    settings_loop()
                
                elif insertion_sort_image_blit.collidepoint(event.pos):
                    insertion_sort_loop()
                
                elif cocktail_shaker_sort_image_blit.collidepoint(event.pos):
                    cocktail_shaker_sort_loop()

                # pygame.time.delay(SORT_END_DELAY)
                show_main_menu()
                pygame.display.update()
                clock.tick(FPS)
    pygame.quit()
    

if __name__ == '__main__':
    main()
