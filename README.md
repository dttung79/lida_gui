# LIDA GUI

LIDA GUI is a graphical user interface for the LIDA tool (https://github.com/microsoft/lida/). It provides an intuitive way to interact with the LIDA system, visualize data, and configure settings.

## Installation
You need to install Lida first. You can install Lida using the following command:

```bash
pip install lida
```

## Running the GUI
You need to create a file key.data that contains your OpenAI API key and store it in the same folder of source code. You can get the key from https://platform.openai.com/account/api-keys. The key.data file should contain a line similar to the following:
sk-bUVFVaKuZ4Z8QDCngHlAT3BlbkFABCyeE25T5Z6nRjZ4TAYN

You can configure some parameters for Lida in the file text_gen.config. 

You can run the GUI using the following command:

```bash
python -m lida_gui
```

## Usage
The GUI provides a simple interface to interact with the LIDA system. You can load data, configure settings, and visualize results using the GUI.

First, click on the "Load Data" button to load a dataset. After loading the data, the application will suggest a list of questions to help user to understand the data. The user can select a question then a chart will show on the right. 

User can also modify the instruction to have a better chart by editing the instruction in the text box then press the button Apply.

User can ask sepecific question by typing the question in the text box then press Enter.