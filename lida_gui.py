from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd

from lida import Manager, TextGenerationConfig , llm
from PIL import ImageTk, Image
import json

class LidaGUI:
    def __init__(self):
        self.window = self.create_window()
        self.create_widgets()

        openai_key = self.read_openai_key()
        self.lida = Manager(text_gen = llm("openai", api_key=openai_key))

        self.n, self.temperature, self.model, self.use_cache, self.vis_lib = self.read_config()
        self.text_gen_config = TextGenerationConfig(n=self.n, 
                                                    temperature=self.temperature, 
                                                    model=self.model, 
                                                    use_cache=self.use_cache)
    
    def create_window(self):
        window = Tk()
        window.title("TabViz V1.0")
        window.geometry("1400x700")
        return window

    def create_widgets(self):
        lbl_title = Label(self.window, text="Tabular Data Summerization & Visualization Tool")
        lbl_title.grid(row=0, column=0, columnspan=3, padx=10, pady=15, sticky="we")

        btn_load = Button(self.window, width=42, text="Load CSV File", command=self.load_file)
        btn_load.grid(row=1, column=0, padx=10, pady=5, sticky="n", columnspan=2)

        lbl_goals = Label(self.window, text="Suggestions:")
        lbl_goals.grid(row=2, column=0, padx=10, pady=5, sticky="nw", columnspan=2)

        self.lst_goals = Listbox(self.window, selectmode=SINGLE, height=10, width=46, exportselection=False)
        self.lst_goals.grid(row=3, column=0, padx=10, pady=5, sticky="nw", columnspan=2)
        self.lst_goals.bind('<<ListboxSelect>>', self.on_goal_selected)

        lbl_custom = Label(self.window, text="Custom Instruction:")
        lbl_custom.grid(row=4, column=0, padx=10, pady=0, sticky="nw")

        btn_custom = Button(self.window, width=10, text="Apply", command=self.btn_custom_clicked)
        btn_custom.grid(row=4, column=1, padx=10, pady=0, sticky="ne")

        self.txt_custom = Text(self.window, width=58, height=5)
        self.txt_custom.grid(row=5, column=0, padx=10, pady=5, sticky="nw", columnspan=2)

        lbl_instruction = Label(self.window, text="Your own question:")
        lbl_instruction.grid(row=6, column=0, padx=10, pady=5, sticky="nw", columnspan=2)

        self.txt_question = Entry(self.window, width=45)
        self.txt_question.grid(row=7, column=0, padx=10, pady=5, sticky="nw", columnspan=2)
        self.txt_question.bind("<Return>", self.on_question_entered)

        self.pic_box = Label(self.window, image=None, relief="solid", borderwidth=1)
        self.pic_box.grid(row=1, column=2, rowspan=15, padx=10, pady=5, sticky="nw")

        self.txt_description = Text(self.window, width=115, height=5)
        self.txt_description.grid(row=16, column=2, padx=10, pady=5, sticky="nw")

        self.load_image("bg.png")
    
    def read_openai_key(self):
        with open("key.data", "r") as f:
            return f.read().strip()

    def read_config(self):
        try:
            with open("text_gen.config", "r") as f:
                config_data = json.load(f)
                n = int(config_data["n"])
                temperature = float(config_data["temperature"])
                model = config_data["model"]
                use_cache = config_data["use_cache"] == 'True'
                vis_lib = config_data["visualization"]
                return n, temperature, model, use_cache, vis_lib
        except FileNotFoundError:
            return 3, 0.5, "gpt-3.5-turbo-0301", True, "plotly"
    
    def run(self):
        self.window.mainloop()

    def load_file(self):
        file_name = fd.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_name:
            self.summary = self.lida.summarize(file_name, summary_method="default", textgen_config=self.text_gen_config) 
            self.goals = self.lida.goals(self.summary, n=self.n, textgen_config=self.text_gen_config)
            self.load_goals()
            mb.showinfo("Info", "File loaded successfully")

    def load_goals(self):
        self.lst_goals.delete(0, END)  # Clear the listbox
        for goal in self.goals:
            self.lst_goals.insert(END, goal.question)
        

    def on_goal_selected(self, event):
        selected_index = self.lst_goals.curselection()[0]
        goal = self.goals[selected_index]
        charts = self.lida.visualize(summary=self.summary, goal=goal, textgen_config=self.text_gen_config, library=self.vis_lib) 
        
        self.show_explain(goal)
        self.draw_chart(charts)

    def draw_chart(self, charts):
        try:
            self.chart = charts[0]   # normally, there should be only one chart
            self.chart.savefig("chart.png")
            self.load_image()
        except IndexError:      # in case there is no chart
            self.load_image("bg.png")
            mb.showinfo("Info", "No chart available for this question.")
    
    def show_explain(self, goal):
        self.txt_custom.delete(1.0, END)
        self.txt_custom.insert(1.0, goal.visualization)
        self.txt_description.delete(1.0, END)
        self.txt_description.insert(1.0, goal.rationale)
    
    def load_image(self, img_name="chart.png"):
        img = Image.open(img_name).resize((800, 500))
        # convert the image to a Tkinter-compatible photo image
        img = ImageTk.PhotoImage(img)
        self.pic_box.configure(image=img)
        self.pic_box.image = img

    def on_question_entered(self, event):
        persona = self.txt_question.get()
        self.goals = self.lida.goals(self.summary, n=3, textgen_config=self.text_gen_config, persona=persona)
        self.load_goals()

    def btn_custom_clicked(self):
        custom_instruction = self.txt_custom.get(1.0, END)
        edit_charts = self.lida.visualize(
                                goal=custom_instruction, 
                                summary=self.summary, library=self.vis_lib,
                                textgen_config=self.text_gen_config)
        self.draw_chart(edit_charts)

if __name__ == "__main__":
    lida_gui = LidaGUI()
    lida_gui.run()