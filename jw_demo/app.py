import pyxel


class SceneMeta:
    """Meta class for scenes"""

    def __init__(self, app: "App"):
        self.app = app

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError


class App:
    target_fps = 60
    current_scene: SceneMeta = None
    menu = [
        # x, y, text, color (aligns with pyxel.text method args)
        (20, 2, "Scene A", pyxel.COLOR_CYAN),
        (60, 2, "Ok", pyxel.COLOR_LIME),
        (72, 2, "X", pyxel.COLOR_ORANGE),
    ]
    show_exit_message = False

    def __init__(self):
        self.pyxel = pyxel
        pyxel.init(120, 120, title="We done did it", fps=self.target_fps)
        pyxel.mouse(True)
        self.scenes = [SceneA(self), SceneB(self)]
        pyxel.run(self.update, self.draw)

    def detect_menu_click(self):
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

        if self.pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        self.pyxel.cls(0)
        for entry in self.menu:
            self.pyxel.text(*entry)

        if self.current_scene:
            self.current_scene.draw()

        if self.show_exit_message:
            self.pyxel.text(10, 70, "Press 'q' to quit", pyxel.COLOR_RED)


class Dancer:
    images = [
        # sprite sheet X, sprite sheet Y, width, height
        # will be passed to pyxel.blt as args: u, v, w, h
        (0, 0, 8, 8),
        (8, 0, 8, 8),
        (0, 8, 8, 8),
        (8, 8, 8, 8),
    ]

    def __init__(self, x: int, y: int):
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
        self.app = app
        self.text = "Animated dancing sprite scene"
        app.pyxel.load("assets/characters.pyxres")

        self.dancer = Dancer(0, 0)

    def update(self):
        # change dancer image every quarter second
        if self.app.pyxel.frame_count % 24 == 0:
            self.dancer.update()

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


# run the app
App()
