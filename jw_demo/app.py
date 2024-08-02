import pyxel


class SceneMeta:
    """Meta class for scenes"""

    def __init__(self, app: "App"):
        self.app = app

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError


# here's the game
class App:
    target_fps = 60
    current_scene: SceneMeta = None
    menu = [
        # x, y, text, color (aligns with pyxel.text method args)
        (2, 2, "Scene A", pyxel.COLOR_CYAN),
        (32, 2, "Scene B", pyxel.COLOR_LIME),
        (64, 2, "Scene 3", pyxel.COLOR_PURPLE),
        (96, 2, "X", pyxel.COLOR_ORANGE),
    ]
    show_exit_message = False

    def __init__(self):
        self.pyxel = pyxel
        # 120 pixel square canvas, set the page title and target FPS
        pyxel.init(120, 120, title="Big demo", fps=self.target_fps)
        # enable built-in pyxel mouse cursor
        pyxel.mouse(True)
        # organize the game scenes
        self.scenes = [SceneA(self), SceneB(self), SceneC(self)]
        # start the program
        pyxel.run(self.update, self.draw)

    def detect_menu_click(self):
        """Helper to determine which menu item was clicked"""
        bounds = [0, 0, 0, 0]
        for index, entry in enumerate(self.menu):
            x, y, text, _ = entry
            bounds[0] = x
            bounds[1] = y
            # each character is 4 pixels wide with 1 pixel padding
            bounds[2] = x + len(text) * 4
            # each character is 5 pixels tall
            bounds[3] = y + 5
            if (
                bounds[0] <= pyxel.mouse_x <= bounds[2]
                and bounds[1] <= pyxel.mouse_y <= bounds[3]
            ):
                return index

    def update(self):
        """Game loop - update game state"""
        # update the currently loaded scene
        if self.current_scene:
            self.current_scene.update()

        # handle menu clicks
        if self.pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            clicked_index = self.detect_menu_click()
            if clicked_index is not None:
                if clicked_index > len(self.scenes) - 1:
                    self.current_scene = None
                    self.show_exit_message = True
                    return
                self.show_exit_message = False
                self.current_scene = self.scenes[clicked_index]

        # allow the user to quit the game
        if self.pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        """Game loop - render the view"""
        # clear and redraw the screen
        self.pyxel.cls(0)
        for entry in self.menu:
            self.pyxel.text(*entry)

        if self.current_scene:
            self.current_scene.draw()

        if self.show_exit_message:
            self.pyxel.text(10, 70, "Press 'q' to quit", pyxel.COLOR_RED)


# helper class for the dancing sprite
class Dancer:
    # point to image locations in the sprite sheet
    images = [
        # sprite sheet X, sprite sheet Y, width, height
        # will be passed to pyxel.blt as args: u, v, w, h
        (0, 0, 8, 8),
        (8, 0, 8, 8),
        (0, 8, 8, 8),
        (8, 8, 8, 8),
    ]

    def __init__(self, x: int, y: int):
        # set the position and prepare the image tiles
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.width = 8
        self.height = 8
        self.tile_indexes = [0, 1, 2, 3]
        self.previous_index = 0
        self.tile_image = self.images[0]

    def update(self):
        self.tile_image = self.next_tile_image()

    def next_tile_image(self):
        # pick a random index from the tile_indexes
        index = (self.previous_index + 1) % 4
        self.previous_index = index
        return self.images[index]

    def draw(self):
        # pick random number between 0 and 3
        pyxel.blt(self.x, self.y, 0, *self.tile_image)


class SceneA(SceneMeta):
    def __init__(self, app: App):
        # load scene assets and start the scene
        self.app = app
        self.text = "Animated dancing sprite scene"
        app.pyxel.load("assets/characters.pyxres")

        self.dancer = Dancer(24, 24)

    def handle_animation(self):
        # change dancer image every quarter second
        if self.app.pyxel.frame_count % 24 == 0:
            self.dancer.update()

    def update(self):
        self.handle_animation()

        # accept input to move the dancer
        if self.app.pyxel.btn(pyxel.KEY_LEFT):
            self.dancer.x -= 1
        if self.app.pyxel.btn(pyxel.KEY_RIGHT):
            self.dancer.x += 1
        if self.app.pyxel.btn(pyxel.KEY_UP):
            self.dancer.y -= 1
        if self.app.pyxel.btn(pyxel.KEY_DOWN):
            self.dancer.y += 1

    def draw(self):
        self.dancer.draw()


class SceneB(SceneMeta):
    def __init__(self, app: App):
        self.app = app
        self.text = "Message!"

    def update(self):
        pass

    def draw(self):
        self.app.pyxel.text(10, 10, self.text, pyxel.COLOR_RED)


# helper class for a clockwise keyboard
class SoundController:
    images = [
        # sprite sheet X, sprite sheet Y, width, height
        # will be passed to pyxel.blt as args: u, v, w, h
        # sheet is shared with the Dancer class above
        # up, up right, right, down right, down, down left, left, up left
        (0, 16, 8, 8),
        (8, 16, 8, 8),
        (0, 24, 8, 8),
        (8, 24, 8, 8),
        (0, 32, 8, 8),
        (8, 32, 8, 8),
        (0, 40, 8, 8),
        (8, 40, 8, 8),
    ]
    image_positions = [
        # draw the images clockwise starting from up, each an 8x8 square
        (0, 0),
        (8, 8),
        (16, 16),
        (8, 24),
        (0, 32),
        (-8, 24),
        (-16, 16),
        (-8, 8),
    ]
    overall_xy = [32, 24]
    sound_notes = ["C2", "D2", "E2", "F2", "G2", "A2", "B2", "C3"]
    notes = list()

    def __init__(self, app: App):
        self.app = app
        # create pyxel note objects for later playback
        for note in self.sound_notes:
            sound = self.app.pyxel.Sound()
            sound.set_notes(note)
            self.notes.append(sound)

    def handle_click(self):
        # check if the mouse is within the bounds of the controller
        bounds = [0, 0, 0, 0]
        for index, position in enumerate(self.image_positions):
            x, y = position
            x += self.overall_xy[0]
            y += self.overall_xy[1]
            bounds[0] = x
            bounds[1] = y
            bounds[2] = x + 8
            bounds[3] = y + 8
            if (
                bounds[0] <= pyxel.mouse_x <= bounds[2]
                and bounds[1] <= pyxel.mouse_y <= bounds[3]
            ):
                self.app.pyxel.play(snd=self.notes[index], ch=0, loop=False)

    def draw(self):
        for index, image in enumerate(self.images):
            x, y = self.image_positions[index]
            x += self.overall_xy[0]
            y += self.overall_xy[1]
            self.app.pyxel.blt(x, y, 0, *image)


class SceneC(SceneMeta):

    def __init__(self, app: App):
        self.app = app
        self.text = "Push the buttons!"
        # we should load this in the main app if we're using it across scenes
        app.pyxel.load("assets/characters.pyxres")
        self.controller = SoundController(app)

    def update(self):
        if self.app.pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.controller.handle_click()

    def draw(self):
        self.app.pyxel.text(10, 10, self.text, pyxel.COLOR_RED)
        self.controller.draw()


# run the app
App()
