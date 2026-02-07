from tkinter import *
import random
import time
from PIL import Image, ImageTk

class Race:
    def __init__(self, Araba, Dubalar, canvas, Arkaplan):
        self.canvas = canvas
        self.Araba = Araba
        self.Dubalar = Dubalar
        self.ArkaPlan = Arkaplan

        self.idAraba = canvas.create_image(150, 400, image=self.Araba)

        self.canvas.bind_all('<KeyPress-Right>', self.Sag)
        self.canvas.bind_all('<KeyPress-Left>', self.Sol)

        self.x = 0
        self.y = 0

    def Sag(self, event):
        Koordinat = self.canvas.coords(self.idAraba)
        if Koordinat[0] < 280:
            self.canvas.move(self.idAraba, 10, 0)

    def Sol(self, event):
        Koordinat = self.canvas.coords(self.idAraba)
        if Koordinat[0] > 20:
            self.canvas.move(self.idAraba, -10, 0)

    def Ciz(self):
        Koordinat = self.canvas.coords(self.idAraba)
        if self.Dubas(Koordinat):
            return True
        return False

    def Dubas(self, pos):
        for ai in range(0, 50):
            duba_pos = self.canvas.coords(self.Dubalar.idDuba[ai])
            if abs(pos[0] - duba_pos[0]) < 20 and abs(pos[1] - duba_pos[1]) < 30:
                return True
        return False

    def Fin(self):
        Koordinat = self.canvas.coords(self.ArkaPlan)
        return Koordinat


class Duba:
    def __init__(self, canvas, DubaResim):
        self.idDuba = {}
        for ai in range(0, 50):
            startsX = float(random.randint(20, 280))
            startsY = float(random.randint(-5000, 50))
            self.idDuba[ai] = canvas.create_image(startsX, startsY, image=DubaResim)

    def Ciz(self, canvas):
        for ai in range(0, 50):
            canvas.move(self.idDuba[ai], 0, 1)


def oyun():
    global OyunDurumu
    if OyunDurumu == 0:
        canvas.move(idArkaPlan, 0, 1)
        DubaObj.Ciz(canvas)
        if RaceObj.Ciz():
            OyunDurumu = 1
            canvas.create_text(150, 200, text="Kaybettin", font=("Arial", 20), fill="red")

        if RaceObj.Fin()[1] > -250:
            OyunDurumu = 2
            canvas.create_text(150, 200, text="Oyunu Kazandın !", font=("Arial", 25), fill="green")

    tk.after(10, oyun)


tk = Tk()
tk.title('wwPHP Race')
canvas = Canvas(tk, width=301, height=500, bd=0, highlightthickness=0)

ArabaResim = PhotoImage(file='car.png')
ArkaPlanResim = Image.open("racemap.png")
ArkaPlan = ImageTk.PhotoImage(ArkaPlanResim)
idArkaPlan = canvas.create_image(0, -4500, image=ArkaPlan, anchor=NW)

canvas.pack()

DubaResim = PhotoImage(file='duba.png')
DubaObj = Duba(canvas, DubaResim)
RaceObj = Race(ArabaResim, DubaObj, canvas, idArkaPlan)

OyunDurumu = 0
oyun()

tk.mainloop()
