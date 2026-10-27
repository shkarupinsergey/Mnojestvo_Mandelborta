import math
import tkinter as tk

SIZE = 600
LIMIT = 200
SAMPLES = ((-0.25, -0.25), (0.25, -0.25),
           (-0.25, 0.25), (0.25, 0.25))


def iterations(cx, cy, limit=LIMIT):
    x, y = 0.0, 0.0
    for n in range(1, limit + 1):
        x, y = x * x - y * y + cx, 2 * x * y + cy
        if x * x + y * y > 4:
            return n + 1 - math.log2(math.log(x * x + y * y) / 2)
    return 0


def get_red(cx, cy):
    n = iterations(cx, cy)
    if n == 0:
        return 160
    return min(145, int(110 * (1 - math.exp(-n / 18))))


class App:
    def __init__(self, root):
        self.root = root
        self.center_x = self.center_y = 0.0
        self.width = 4.0
        self.after_id = None
        self.image = None

        root.title("Множество Мандельброта")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=SIZE, height=SIZE,
                                bg="black", highlightthickness=0)
        self.canvas.pack()
        self.picture = self.canvas.create_image(0, 0, anchor=tk.NW)
        buttons = tk.Frame(root)
        buttons.pack(pady=5)
        tk.Button(buttons, text="Увеличить", command=lambda: self.zoom(0.5)
                  ).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Уменьшить", command=lambda: self.zoom(2)
                  ).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Сброс", command=self.reset).pack(side=tk.LEFT)
        tk.Label(root, text="ЛКМ/ПКМ - зум | +/- - масштаб | R - сброс").pack()
        self.status = tk.Label(root)
        self.status.pack(pady=5)
        self.canvas.bind("<Button-1>", lambda e: self.zoom(0.5, e.x, e.y))
        self.canvas.bind("<Button-3>", lambda e: self.zoom(2, e.x, e.y))
        root.bind("<KeyPress-r>", lambda e: self.reset())
        root.bind("<KeyPress-R>", lambda e: self.reset())
        root.bind("<KeyPress>",
                  lambda e: self.reset() if e.keycode == 82 else None)
        root.bind("<KeyPress-plus>", lambda e: self.zoom(0.5))
        root.bind("<KeyPress-equal>", lambda e: self.zoom(0.5))
        root.bind("<KeyPress-minus>", lambda e: self.zoom(2))
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.draw()

    def point(self, px, py):
        cx = self.center_x + (px / (SIZE - 1) - 0.5) * self.width
        cy = self.center_y + (0.5 - py / (SIZE - 1)) * self.width
        return cx, cy

    def draw(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.image = tk.PhotoImage(width=SIZE, height=SIZE)
        self.canvas.itemconfig(self.picture, image=self.image)
        self.row = 0
        self.status.config(text=f"Масштаб: {4 / self.width:g}x | Готово: 0%")
        self.after_id = self.root.after(1, self.draw_rows)

    def draw_rows(self):
        self.after_id = None
        step = self.width / (SIZE - 1)
        for py in range(self.row, min(self.row + 2, SIZE)):
            colors = []
            for px in range(SIZE):
                cx, cy = self.point(px, py)
                red = sum(get_red(cx + dx * step, cy + dy * step)
                          for dx, dy in SAMPLES) // 4
                colors.append(f"#{red:02x}0000")
            self.image.put("{" + " ".join(colors) + "}", to=(0, py))
            self.row = py + 1
        self.status.config(text=f"Масштаб: {4 / self.width:g}x | "
                                f"Готово: {self.row * 100 // SIZE}%")
        if self.row < SIZE:
            self.after_id = self.root.after(1, self.draw_rows)

    def zoom(self, factor, px=None, py=None):
        new_width = self.width * factor
        if not 0.000001 <= new_width <= 4:
            return
        if px is not None:
            self.center_x, self.center_y = self.point(px, py)
        self.width = new_width
        self.draw()

    def reset(self):
        self.center_x = self.center_y = 0.0
        self.width = 4.0
        self.draw()

    def close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    App(window)
    window.mainloop()
