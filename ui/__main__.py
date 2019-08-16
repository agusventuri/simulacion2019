from tkinter import Frame, Label, Radiobutton, DISABLED, Entry, Button, Tk, X, Toplevel, END, BOTH, NORMAL, StringVar
from matplotlib.pyplot import Figure
from numpy import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from models import TestChiCuadrado, PythonRandomGenerator, MultiplicativeCongruentialGenerator, \
    MixedCongruentialGenerator

LARGE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 12, "bold")
LABEL_ERROR = ("Arial", 14, "bold")
BASE_ITERATIONS = 20
OS = "os"
CONG_MIX = "mix"


class NumberGenerator(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CongruentialMixed, CongruentialMultiplicative, TestChiSquare):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Generador de Números Aleatorios", font=LARGE_FONT)
        label.pack(pady=5, padx=10)

        button_container = Frame(self)
        button_container.pack(expand=True, fill=X)

        button = Button(button_container, text="Congruencial Mixto",
                        command=lambda: controller.show_frame(CongruentialMixed))
        button.pack(fill=X, pady=5, padx=20)

        button2 = Button(button_container, text="Congruencial Multiplicativo",
                         command=lambda: controller.show_frame(CongruentialMultiplicative))
        button2.pack(fill=X, pady=5, padx=20)

        button3 = Button(button_container, text="Test Chi-Cuadrado",
                         command=lambda: controller.show_frame(TestChiSquare))
        button3.pack(fill=X, padx=20, pady=5)

        Label(self,
              text="Alumnos: Gersicich, Jeremias; Venturi, Agustin; Grober, Luciana; Bacca, Josue; Britos Anabel").pack(
            pady=20)


class CongruentialMethod(Frame):
    m = None
    c = None
    seed = None
    a = None
    generator = None
    last_index_generated = 0

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.generated = []
        btn_back = Button(self, text="Volver",
                          command=lambda: self.go_back(controller))
        btn_back.pack(pady=5, fill=X, padx=40)

        self.title = Label(self, text="Método", font=LARGE_FONT)
        self.title.pack(padx=10)

        grid_input = Frame(self)
        grid_input.pack(fill='both', ipady=5, pady=5)

        m_label = Label(grid_input, text="M", font=LABEL_FONT)
        m_label.grid(column=0, row=0, padx=10)
        self.m_input = Entry(grid_input)
        self.m_input.grid(column=1, row=0)

        seed_label = Label(grid_input, text="Seed", font=LABEL_FONT)
        seed_label.grid(column=0, row=1, padx=10)
        self.seed_input = Entry(grid_input)
        self.seed_input.grid(column=1, row=1)

        a_label = Label(grid_input, text="A", font=LABEL_FONT)
        a_label.grid(column=0, row=2, padx=10)
        self.a_input = Entry(grid_input)
        self.a_input.grid(column=1, row=2)

        c_label = Label(grid_input, text="C", font=LABEL_FONT)
        c_label.grid(column=0, row=3, padx=10)
        self.c_input = Entry(grid_input)
        self.c_input.grid(column=1, row=3)

        total_label = Label(grid_input, text="Total Generado", font=LABEL_FONT)
        total_label.grid(column=2, row=0, padx=10)
        self.total_count = Label(grid_input, text="", font=LABEL_FONT)
        self.total_count.grid(column=3, row=0, padx=10)

        self.error_label = Label(self, font=LABEL_ERROR, fg="red")
        self.error_label.pack(fill=X)

        self.btn_calculate = Button(self, text="Generar")
        self.btn_calculate.pack(fill=X, padx=40)

        self.add_one = Button(self, text="Agregar Número", state=DISABLED, command=lambda: self.add_number())
        self.add_one.pack(fill=X, padx=40)

        cols = ('Posición', 'Número')
        self.table = ttk.Treeview(self, columns=cols, show='headings')
        self.table.pack(padx=10, pady=10, fill=BOTH)

        for col in cols:
            self.table.heading(col, text=col)

    def add_number(self):
        new_generated = self.generator.generate_number()
        self.last_index_generated += 1
        self.generated.append(new_generated)
        self.table.insert("", "end", values=(self.last_index_generated, '{:.4f}'.format(new_generated)))
        self.table.update()
        self.total_count.configure(text=str(self.last_index_generated))
        self.total_count.update()
        self.table.yview_moveto(1)

    def generate_numbers(self, mixed):
        self.error_label.configure(text="")
        self.table.delete(*self.table.get_children())

        valid, error = self.validate_inputs(mixed)

        if valid:
            if mixed:
                self.generator = MixedCongruentialGenerator(self.seed, self.m, self.a, self.c)
            else:
                self.generator = MultiplicativeCongruentialGenerator(self.seed, self.m, self.a)
        else:
            self.error_label.configure(text=error)
            return

        self.m_input.configure(state=DISABLED)
        self.a_input.configure(state=DISABLED)
        self.c_input.configure(state=DISABLED)
        self.seed_input.configure(state=DISABLED)

        for i in range(BASE_ITERATIONS):
            self.btn_calculate.configure(state=DISABLED)
            new_generated = self.generator.generate_number()
            self.generated.insert(i, new_generated)
            self.last_index_generated = i + 1
            self.table.insert("", "end", values=(self.last_index_generated, '{:.4f}'.format(new_generated)))
            self.table.update()
            self.table.yview_moveto(1)
            self.total_count.configure(text=str(self.last_index_generated))
            self.total_count.update()

        self.add_one.configure(state=NORMAL)

    def validate_inputs(self, mixed):
        self.m = self.m_input.get()
        self.seed = self.seed_input.get()
        self.a = self.a_input.get()
        self.c = self.c_input.get()

        try:
            self.m = round(float(self.m), 4)
            if self.m <= 0:
                return False, "M debe ser positivo o igual a 0"
        except (ValueError, TypeError):
            return False, "El valor de M debe ser un número"

        try:
            self.seed = round(float(self.seed), 4)
            if self.seed <= 0:
                return False, "Seed debe ser positivo o igual a 0"
            if self.seed >= self.m:
                return False, "Seed debe ser menor a M"
        except (ValueError, TypeError):
            return False, "El valor de Seed debe ser un número"

        try:
            self.a = round(float(self.a), 4)
            if self.a <= 0:
                return False, "A debe ser positivo o igual a 0"
            if self.a >= self.m:
                return False, "A debe ser menor a M"
        except (ValueError, TypeError):
            return False, "El valor de A debe ser un número"

        if mixed:
            try:
                self.c = round(float(self.c), 4)
                if self.c <= 0:
                    return False, "C debe ser positivo o igual a 0"
                if self.c >= self.m:
                    return False, "C debe ser menor a M"
            except (ValueError, TypeError):
                return False, "El valor de C debe ser un número"

        return True, ""

    def go_back(self, controller):
        self.m_input.configure(state=NORMAL)
        self.a_input.configure(state=NORMAL)
        self.c_input.configure(state=NORMAL)
        self.seed_input.configure(state=NORMAL)
        self.m_input.delete(0, END)
        self.seed_input.delete(0, END)
        self.a_input.delete(0, END)
        self.c_input.delete(0, END)
        self.generated.clear()
        self.table.delete(*self.table.get_children())
        self.btn_calculate.configure(state=NORMAL)
        self.add_one.configure(state=DISABLED)
        self.generator = None
        self.total_count.configure(text="")
        controller.show_frame(StartPage)


class CongruentialMixed(CongruentialMethod):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.title.configure(text="Método Congruencial Mixto")
        self.btn_calculate.configure(command=lambda: self.generate_numbers(True))
        self.update()


class CongruentialMultiplicative(CongruentialMethod):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.title.configure(text="Método Congruencial Multiplicativo")
        self.c_input.insert(0, "0")
        self.c_input.configure(state=DISABLED)
        self.btn_calculate.configure(command=lambda: self.generate_numbers(False))


class TestChiSquare(Frame):
    m = None
    c = None
    seed = None
    a = None
    generator = None
    last_index_generated = 0

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.generated_series = []
        self.quantity = 0
        self.intervals = 0
        self.intervals_list = []
        self.intervals_average = []
        self.expected_frequency = []
        self.real_frequency = []
        self.expected_series = []
        self.switch_variable = StringVar(value="os")

        btn_back = Button(self, text="Volver",
                          command=lambda: self.go_back(controller))
        btn_back.pack(pady=5, fill=X, padx=40)

        self.title = Label(self, text="Test Chi Cuadrado", font=LARGE_FONT)
        self.title.pack(padx=10)

        grid_input = Frame(self)
        grid_input.pack(fill='both', ipady=5, pady=5)

        quantity_label = Label(grid_input, text="Cantidad de Números", font=LABEL_FONT)
        quantity_label.grid(column=0, row=0, padx=10)
        self.quantity_input = Entry(grid_input)
        self.quantity_input.grid(column=1, row=0)

        intervals_label = Label(grid_input, text="Cantidad de Intervalos", font=LABEL_FONT)
        intervals_label.grid(column=0, row=1, padx=10)
        self.intervals_input = Entry(grid_input)
        self.intervals_input.grid(column=1, row=1)

        total_label = Label(grid_input, text="Total Generado", font=LABEL_FONT)
        total_label.grid(column=0, row=3, padx=10)
        self.total_count = Label(grid_input, text="", font=LABEL_FONT)
        self.total_count.grid(column=1, row=3, padx=10)

        self.language_button = Radiobutton(grid_input, text="Python", variable=self.switch_variable,
                                           indicatoron=False,
                                           value=OS, command=lambda: self.switch_method())
        self.congruential_button = Radiobutton(grid_input, text="Congruencial Mixto", variable=self.switch_variable,
                                               indicatoron=False, value=CONG_MIX,
                                               command=lambda: self.switch_method())
        self.language_button.grid(column=0, row=4, padx=10)
        self.congruential_button.grid(column=1, row=4, padx=10)

        m_label = Label(grid_input, text="M", font=LABEL_FONT)
        m_label.grid(column=2, row=0, padx=10)
        self.m_input = Entry(grid_input)
        self.m_input.grid(column=3, row=0)

        seed_label = Label(grid_input, text="Seed", font=LABEL_FONT)
        seed_label.grid(column=2, row=1, padx=10)
        self.seed_input = Entry(grid_input)
        self.seed_input.grid(column=3, row=1)

        a_label = Label(grid_input, text="A", font=LABEL_FONT)
        a_label.grid(column=2, row=2, padx=10)
        self.a_input = Entry(grid_input)
        self.a_input.grid(column=3, row=2)

        c_label = Label(grid_input, text="C", font=LABEL_FONT)
        c_label.grid(column=2, row=3, padx=10)
        self.c_input = Entry(grid_input)
        self.c_input.grid(column=3, row=3)

        self.error_label = Label(self, font=LABEL_ERROR, fg="red")
        self.error_label.pack(fill=X)

        self.btn_calculate = Button(self, text="Generar Serie", command=lambda: self.generate_sequence())
        self.btn_calculate.pack(fill=X, padx=40)

        self.btn_make_test = Button(self, text="Realizar Test", command=lambda: self.make_test(), state=DISABLED)
        self.btn_make_test.pack(fill=X, padx=40)

        self.btn_make_graph = Button(self, text="Generar Gráficos", command=lambda: self.make_graph(),
                                     state=DISABLED)
        self.btn_make_graph.pack(fill=X, padx=40)

        self.table_container = Frame(self)
        self.table_container.pack(fill=BOTH, pady=5, expand=True, ipady=5)

        serie_label = Label(self.table_container, text="Serie", font=LABEL_FONT)
        serie_label.grid(pady=5, row=0, column=0)
        self.serie_table = ttk.Treeview(self.table_container, columns=1, show='headings')
        self.serie_table.grid(padx=10, row=1, column=0)
        self.serie_table.heading(1, text='Número Generado')

        cols = ('Minimo Intervalo', 'Máximo Intervalo', 'Media del Intervalo', 'Frecuencia Esperada', 'Frecuencia Real')
        frequency_table_label = Label(self.table_container, text="Tabla de Frecuencias", font=LABEL_FONT)
        frequency_table_label.grid(pady=5, row=0, column=1)
        self.frequency_table = ttk.Treeview(self.table_container, columns=cols, show='headings')
        self.frequency_table.grid(padx=10, row=1, column=1)

        for col in cols:
            self.frequency_table.heading(col, text=col)
        self.switch_method()

    def switch_method(self):
        if self.switch_variable.get() == OS:
            self.a_input.configure(state=DISABLED)
            self.m_input.configure(state=DISABLED)
            self.seed_input.configure(state=DISABLED)
            self.c_input.configure(state=DISABLED)

        if self.switch_variable.get() == CONG_MIX:
            self.a_input.configure(state=NORMAL)
            self.m_input.configure(state=NORMAL)
            self.seed_input.configure(state=NORMAL)
            self.c_input.configure(state=NORMAL)

    def generate_sequence(self):
        valid, error = self.validate_inputs()

        if valid:
            self.quantity_input.configure(state=DISABLED)
            self.intervals_input.configure(state=DISABLED)
            self.m_input.configure(state=DISABLED)
            self.a_input.configure(state=DISABLED)
            self.c_input.configure(state=DISABLED)
            self.seed_input.configure(state=DISABLED)
            self.language_button.configure(state=DISABLED)
            self.congruential_button.configure(state=DISABLED)

            if self.switch_variable.get() == OS:
                self.generator = PythonRandomGenerator()
                self.generated_series = self.generator.generate(self.quantity)
            elif self.switch_variable.get() == CONG_MIX:
                self.generator = MixedCongruentialGenerator(self.seed, self.m, self.a, self.c)
                self.generated_series = self.generator.generate(self.quantity)

            self.error_label.configure(text="")
            self.btn_calculate.configure(state=DISABLED)

            i = 1
            for num in self.generated_series:
                self.serie_table.insert("", "end", values='{:.4f}'.format(num))
                self.last_index_generated = i
                self.total_count.configure(text=str(self.last_index_generated))
                self.total_count.update()
                i += 1

            self.serie_table.update()
            self.btn_make_test.configure(state=NORMAL)
        else:
            self.error_label.configure(text=error)
            return

    def make_test(self):
        self.btn_make_test.configure(state=DISABLED)
        self.intervals_list, self.intervals_average = TestChiCuadrado.divide_intervals(self.intervals)
        self.expected_frequency, self.real_frequency = TestChiCuadrado.test_chi_cuadrado(
            self.generated_series,
            self.intervals_list)

        for i in range(len(self.intervals_list)):
            interval_min = '{:.4f}'.format(self.intervals_list[i][0])
            interval_max = '{:.4f}'.format(self.intervals_list[i][1])
            average = '{:.4f}'.format(self.intervals_average[i])
            expected = self.expected_frequency[i]
            real = self.real_frequency[i]

            self.frequency_table.insert("", "end", values=(interval_min, interval_max, average, expected, real))
            self.frequency_table.update()
        self.btn_make_graph.configure(state=NORMAL)

    def make_graph(self):
        expected_series = TestChiCuadrado.generate_expected_distribution(self.intervals_average,
                                                                         self.expected_frequency[0],
                                                                         0,
                                                                         1)
        data = column_stack((expected_series, self.generated_series))

        window = Toplevel(self)

        figure = Figure(figsize=(10, 9), dpi=100)
        plot = figure.add_subplot(111)
        plot.hist(data, label=('Esperada', 'Real'), bins=10)
        scatter3 = FigureCanvasTkAgg(figure, window)
        scatter3.get_tk_widget().pack(fill=BOTH, padx=20, pady=20)
        plot.set_title('Distribución de Frecuencias', fontsize=14)
        plot.legend()
        plot.set_xlabel('Intervalo', fontsize=14)
        plot.set_ylabel('Frecuencia', fontsize=14)

    def validate_inputs(self):
        self.quantity = self.quantity_input.get()
        self.intervals = self.intervals_input.get()

        if self.quantity != "":
            try:
                self.quantity = int(self.quantity)
                if self.quantity <= 0:
                    return False, "Cantidad de Números debe ser positivo"
            except (ValueError, TypeError):
                return False, "La Cantidad de Números debe ser un número"
        else:
            return False, "Ingrese una Cantidad de Números"

        if self.intervals != "":
            try:
                self.intervals = int(self.intervals)
                if self.intervals <= 0:
                    return False, "Cantidad de Intervalos debe ser positivo"
            except (ValueError, TypeError):
                return False, "La Cantidad de Intervalo debe ser un número"
        else:
            return False, "Ingrese una Cantidad de Intervalos"

        if self.switch_variable.get() == CONG_MIX:
            self.m = self.m_input.get()
            self.seed = self.seed_input.get()
            self.a = self.a_input.get()
            self.c = self.c_input.get()

            try:
                self.m = round(float(self.m), 4)
                if self.m <= 0:
                    return False, "M debe ser positivo o igual a 0"
            except (ValueError, TypeError):
                return False, "El valor de M debe ser un número"

            try:
                self.seed = round(float(self.seed), 4)
                if self.seed <= 0:
                    return False, "Seed debe ser positivo o igual a 0"
                if self.seed >= self.m:
                    return False, "Seed debe ser menor a M"
            except (ValueError, TypeError):
                return False, "El valor de Seed debe ser un número"

            try:
                self.a = round(float(self.a), 4)
                if self.a <= 0:
                    return False, "A debe ser positivo o igual a 0"
                if self.a >= self.m:
                    return False, "A debe ser menor a M"
            except (ValueError, TypeError):
                return False, "El valor de A debe ser un número"

            try:
                self.c = round(float(self.c), 4)
                if self.c <= 0:
                    return False, "C debe ser positivo o igual a 0"
                if self.c >= self.m:
                    return False, "C debe ser menor a M"
            except (ValueError, TypeError):
                return False, "El valor de C debe ser un número"

        return True, ""

    def go_back(self, controller):
        self.language_button.configure(state=NORMAL)
        self.congruential_button.configure(state=NORMAL)
        self.switch_variable.set = CONG_MIX
        self.switch_method()
        self.m_input.delete(0, END)
        self.seed_input.delete(0, END)
        self.a_input.delete(0, END)
        self.c_input.delete(0, END)
        self.switch_variable.set = OS
        self.quantity_input.configure(state=NORMAL)
        self.intervals_input.configure(state=NORMAL)
        self.quantity_input.delete(0, END)
        self.intervals_input.delete(0, END)
        self.serie_table.delete(*self.serie_table.get_children())
        self.frequency_table.delete(*self.serie_table.get_children())
        self.btn_calculate.configure(state=NORMAL)
        self.btn_make_test.configure(state=DISABLED)
        self.total_count.configure(text="")
        self.generated_series = []
        self.quantity = 0
        self.intervals = 0
        self.intervals_list = []
        self.intervals_average = []
        self.expected_frequency = []
        self.real_frequency = []
        controller.show_frame(StartPage)


def main():  # type: () -> None
    app = NumberGenerator()
    app.wm_title("Generador de Números Aleatorios")
    app.mainloop()


if __name__ == "__main__":
    main()
