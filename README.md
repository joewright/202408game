# Demo game
This is a demo app made with [Pyxel](https://github.com/kitao/pyxel).

There's a global menu with each button opening a Scene.

### Demo
Live demo is available via `kitao.github.com` [here](https://kitao.github.io/pyxel/wasm/launcher/?run=joewright.202408game.jw_demo.app)

More details for creating the web version are available here: https://github.com/kitao/pyxel/wiki/How-To-Use-Pyxel-Web

Link to August 2024 [PyATL](https://pyatl.dev/) slides: https://docs.google.com/presentation/d/12s_L2rrJNBV2-5rauwABA3vQQp5MPtDaLxIa42Dc21s

### Running it locally:

```sh
# install virtualenv
# clone this repo and change to its directory
# from the project directory do the following
virtualenv venv
source venv/bin/active

pip install --requirement requirements.txt

# run the app
python jw_demo/app.py

# run the tile editor
pyxel edit jw_demo/assets/characters
```

See the included VS Code `.vscode/launch.json` file for in-editor debugging.