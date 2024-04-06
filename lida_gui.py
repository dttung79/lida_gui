from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd

from lida import Manager, TextGenerationConfig , llm
from io import BytesIO
import base64
from PIL import ImageTk, Image

class LidaGUI:
    def __init__(self):
        self.window = self.create_window()
        self.create_widgets()

        openai_key = self.read_openai_key()
        self.lida = Manager(text_gen = llm("openai", api_key=openai_key))
        self.text_gen_config = self.gen_config()
    
    def create_window(self):
        window = Tk()
        window.title("Lida")
        window.geometry("700x500")
        return window

    def create_widgets(self):
        lbl_title = Label(self.window, text="Lida")
        lbl_title.grid(row=0, column=0)

        btn_load = Button(self.window, text="Load CSV File", command=self.load_file)
        btn_load.grid(row=1, column=0)

        lbl_goals = Label(self.window, text="Goals")
        lbl_goals.grid(row=2, column=0)

        self.lst_goals = Listbox(self.window, selectmode=SINGLE, height=20, width=30)
        self.lst_goals.grid(row=3, column=0)
        self.lst_goals.bind('<<ListboxSelect>>', self.on_goal_selected)
        
        self.pic_box = Label(self.window, image=self.load_image(), relief="solid", borderwidth=1)
        self.pic_box.grid(row=3, column=1)
    
    def read_openai_key(self):
        with open("key.data", "r") as f:
            return f.read().strip()

    def gen_config(self):
        with open("text_gen.config", "r") as f:
            n_val = int(f.readline().strip().split('=')[1])
            temperature_val = float(f.readline().strip().split('=')[1])
            model_val = f.readline().strip().split('=')[1]
            use_cache_val = f.readline().strip().split('=')[1] == "True"
            return TextGenerationConfig(n=n_val, temperture=temperature_val, model=model_val, use_cache=use_cache_val)
    
    def run(self):
        self.window.mainloop()

    def load_file(self):
        file_name = fd.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_name:
            self.summary = self.lida.summarize(file_name, summary_method="default", textgen_config=self.text_gen_config) 
            self.goals = self.lida.goals(self.summary, n=3, textgen_config=self.text_gen_config)
            self.lst_goals.delete(0, END)  # Clear the listbox
            for goal in self.goals:
                self.lst_goals.insert(END, goal.question)
            mb.showinfo("Info", "File loaded successfully")

    def on_goal_selected(self, event):
        selected_index = self.lst_goals.curselection()[0]
        goal = self.goals[selected_index]
        charts = self.lida.visualize(summary=self.summary, goal=goal, textgen_config=self.text_gen_config, library='seaborn') 
        chart = charts[0]
        chart.savefig("chart.png")
        # load chart.png to pic_box
        img = self.load_image()
        self.pic_box.configure(image=img)
        # resize the pic_box
        self.pic_box.image = img
    
    def load_image(self):
        img = Image.open("chart.png")
        return ImageTk.PhotoImage(img)



if __name__ == "__main__":
    lida_gui = LidaGUI()
    lida_gui.run()