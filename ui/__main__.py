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


# Aplicación UI realizada con tkinter para generar números aleatorios y realizar test chi-cuadrado.
class NumberGenerator(Tk):

    # Constructor de la aplicación.
    #
    # Crea las pantallas de la aplicación.
    #
    # A cada pantalla la agrega a una lista que se utiliza para navegar entre las pantallas y que solo se creen una
    # única vez.
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Cada nueva pantalla que se quiera mostrar debe ser agregada aca.
        screens = (StartPage, CongruentialMixed, CongruentialMultiplicative, TestChiSquare)

        for F in screens:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # "Muestra" la pantalla que se pasa por parámetro siempre y cuando este agregada en la lista inicializada en el
    # constructor.
    # En realidad lo que hace es subirla en el "eje z" de pantallas poniéndola por encima del resto.
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Clase que representa la pantalla inicial de la aplicación.
class StartPage(Frame):

    # Constructor de la pantalla inicial. Agrega los botones para acceder a las siguientes pantallas y nuestros nombres.
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


# Clase base para las pantallas generadores de números aleatorios por el método congruencial.
class CongruentialMethod(Frame):
    # Inicialización de las variables básicas que se necesitan para generar los números aleatorios.
    m = None
    c = None
    seed = None
    a = None
    # Variable destinada a almacenar el generador que se va a utilizar. Ver models/__init__.py
    generator = None
    # Indice del último número generado. Variable global para luego mostrar la cantidad total generada de números.
    last_index_generated = 0

    # Constructor base de las pantallas generadoras de números aleatorios por método congruencial.
    # Agrega los botones de navegación (btn_back), los botones de acción (btn_calculate, add_one), los inputs para
    # ingresar los valores necesario para generar los números (m_input, seed_input, a_input, c_input), sus labels,
    # labels informativos para el total generado (total_label y total_count para mostrar el valor) o errores
    # (error_label) y la tabla donde se podrán visualizar los números generados.
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

    # Método que define las acciones a ejecutar al presionar el botón add_one.
    def add_number(self):
        # Genera un nuevo número mediante el generador.
        new_generated = self.generator.generate_number()

        # Aumenta la cantidad de números generados en 1.
        self.last_index_generated += 1

        # Agrega el número generado a la lista de generados.
        self.generated.append(new_generated)

        # Inserta el número en la tabla, formateandolo correctamente para su visualización.
        self.table.insert("", "end", values=(self.last_index_generated, '{:.4f}'.format(new_generated)))

        # Fuerza el renderizado de la tabla con el nuevo valor.
        self.table.update()

        # Actualiza el label de la cuenta total.
        self.total_count.configure(text=str(self.last_index_generated))

        # Fuerza el renderizado del label de la cuenta total.
        self.total_count.update()

        # Mueve el cursor de la tabla a la última posición para poder ver los resultados.
        self.table.yview_moveto(1)

    # Método que define las acciones a ejecutar al presionar btn_calculate.
    #
    # Parámetro mixed define si se utiliza el generador congruencial mixto o el multiplicativo.
    def generate_numbers(self, mixed):
        # Se limpia el label de error.
        self.error_label.configure(text="")

        # Se limpia la tabla de resultados.
        self.table.delete(*self.table.get_children())

        # Corre la validación de inputs
        valid, error = self.validate_inputs(mixed)

        # Autoexplicativo =B
        if valid:
            if mixed:
                self.generator = MixedCongruentialGenerator(self.seed, self.m, self.a, self.c)
            else:
                self.generator = MultiplicativeCongruentialGenerator(self.seed, self.m, self.a)
        else:
            self.error_label.configure(text=error)
            return

        # Deshabilita los inputs para que no se puedan modificar y no varien los valores luego cuando quiera agregar
        # de a un único número.
        self.m_input.configure(state=DISABLED)
        self.a_input.configure(state=DISABLED)
        self.c_input.configure(state=DISABLED)
        self.seed_input.configure(state=DISABLED)

        # TODO: Cambiar por el método generador múltiple en vez de el único. O tambien llamar al add_number LOL
        # Basandose en BASE_ITERATIONS, genera un número aleatorio y realiza lo mismo que el método add_number.
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

        # Habilita el generador de a un número.
        self.add_one.configure(state=NORMAL)

    # Validación de los inputs.
    #
    # "Recorre" de arriba para abajo inputs de la UI. Al encontrar un error "corta" y devuelve False y el String de
    # error.
    # Si no encuentra ningún error, devuelve True y String vacío.
    #
    # Parámetro mixed en True si se esta validando para el método congruencial mixto. False si es multiplicativo. De
    # esta forma se valida o no c_input.
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

    # Método que define las acciones a realizar al presionar el botón btn_back.
    def go_back(self, controller):
        # Vuelve los inputs al estado habilitado
        self.m_input.configure(state=NORMAL)
        self.a_input.configure(state=NORMAL)
        self.c_input.configure(state=NORMAL)
        self.seed_input.configure(state=NORMAL)

        # Borra el contenido de los inputs
        self.m_input.delete(0, END)
        self.seed_input.delete(0, END)
        self.a_input.delete(0, END)
        self.c_input.delete(0, END)

        # Limpia la lista de números generados.
        self.generated.clear()

        # Limpia la tabla de números generados.
        self.table.delete(*self.table.get_children())

        # Restaura los botones a su estado inicial
        self.btn_calculate.configure(state=NORMAL)
        self.add_one.configure(state=DISABLED)

        # Limpia la referencia al generador
        self.generator = None

        # Limpia el label total de generados.
        self.total_count.configure(text="")

        # Muestra la página inicial.
        controller.show_frame(StartPage)


# Especificación de la pantalla del generador del método congruencial para el método congruencial mixto.
class CongruentialMixed(CongruentialMethod):

    # Constructor de la pantalla.
    def __init__(self, parent, controller):
        # Llama al constructor padre para inicializar las cosas comunes de la pantalla.
        super().__init__(parent, controller)

        # Setea el título correspondiente.
        self.title.configure(text="Método Congruencial Mixto")

        # Setea la acción correspondiente al btn_calculate
        self.btn_calculate.configure(command=lambda: self.generate_numbers(True))


# Especificación de la pantalla del generador del método congruencial para el método congruencial multiplicativo.
class CongruentialMultiplicative(CongruentialMethod):

    # Constructor de la pantalla.
    def __init__(self, parent, controller):
        # Llama al constructor padre para inicializar las cosas comunes de la pantalla.
        super().__init__(parent, controller)

        # Setea el título correspondiente.
        self.title.configure(text="Método Congruencial Multiplicativo")

        # Setea el valor 0 a C ya que no se usa.
        self.c_input.insert(0, "0")

        # Deshabilita el input c_input para que no se pueda modificar el valor.
        self.c_input.configure(state=DISABLED)

        # Setea la acción correspondiente al btn_calculate
        self.btn_calculate.configure(command=lambda: self.generate_numbers(False))


# Clase que representa la pantalla para realizar el Test de Chi Cuadrado.
class TestChiSquare(Frame):
    # Inicialización de las variables básicas que se necesitan para generar los números aleatorios.
    m = None
    c = None
    seed = None
    a = None
    # Variable destinada a almacenar el generador que se va a utilizar. Ver models/__init__.py
    generator = None
    # Indice del último número generado. Variable global para luego mostrar la cantidad total generada de números.
    last_index_generated = 0

    # Constructor de la pantalla para realizar el Test de Chi Cuadrado.
    # Agrega los botones de navegación (btn_back), los botones de acción (btn_calculate, btn_make_test, btn_make_graph),
    # los inputs para ingresar los valores necesario para generar los números (m_input, seed_input, a_input, c_input),
    # los inputs para ingresar la cantidad de números aleatorios que se quieren crear (quantity_input), y la cantidad
    # de intervalos en los cuales se quiere dividir y realizar el test (intervals_input), los RadioButtons para definir
    # el método a utilizar para la creación de la serie de números aleatorios (language_button y congruential_button),
    # los labels, labels informativos para el total generado (total_label y total_count para mostrar el valor) o errores
    # (error_label), la tabla donde se podrán visualizar los números generados, la tabla para visualizar la distribución
    # de frecuencia real y esperada por intervalos.
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Serie de números generada.
        self.generated_series = []
        # Cantidad de números a generar en la serie.
        self.quantity = 0
        # Cantidad de intervalos para el test.
        self.intervals = 0
        # Intervalos generados.
        self.intervals_list = []
        # Listado con las medias de los intervalos.
        self.intervals_average = []
        # Listado con las frecuencias esperadas.
        self.expected_frequency = []
        # Listado con las frecuencias reales obtenida de la serie.
        self.real_frequency = []
        # Serie de números que cumple con la frecuencia esperada.
        self.expected_series = []
        # Variable que almacena el tipo de generador a utilizar para los Switch Buttons.
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

    # Define las acciones a realizar al cambiar el método de generación de la serie de números aleatorios.
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

    # Define las acciones a realizar al apretar el botón btn_calculate que genera la serie de números aleatorios.
    def generate_sequence(self):
        # Realiza la validación de los inputs.
        valid, error = self.validate_inputs()

        # "Autoexplicativo" =B
        if valid:
            # Deshabilita inputs para que no se modifiquen los valores iniciales.
            self.quantity_input.configure(state=DISABLED)
            self.intervals_input.configure(state=DISABLED)
            self.m_input.configure(state=DISABLED)
            self.a_input.configure(state=DISABLED)
            self.c_input.configure(state=DISABLED)
            self.seed_input.configure(state=DISABLED)
            self.language_button.configure(state=DISABLED)
            self.congruential_button.configure(state=DISABLED)

            # Asigna un valor al generador de acuerdo a la variable del switch del tipo de generador.
            if self.switch_variable.get() == OS:
                self.generator = PythonRandomGenerator()
                self.generated_series = self.generator.generate(self.quantity)
            elif self.switch_variable.get() == CONG_MIX:
                self.generator = MixedCongruentialGenerator(self.seed, self.m, self.a, self.c)
                self.generated_series = self.generator.generate(self.quantity)

            # Limpia el error.
            self.error_label.configure(text="")

            # Deshabilita la opción de generación de la serie.
            self.btn_calculate.configure(state=DISABLED)

            # Completa la table de la serie con los valores generados y cambia el label del total de generados.
            i = 1
            for num in self.generated_series:
                self.serie_table.insert("", "end", values='{:.4f}'.format(num))
                self.last_index_generated = i
                self.total_count.configure(text=str(self.last_index_generated))
                self.total_count.update()
                i += 1

            # Fuerza la renderización de la tabla.
            self.serie_table.update()

            # Habilita el botón para realizar el test.
            self.btn_make_test.configure(state=NORMAL)
        else:
            self.error_label.configure(text=error)
            return

    # Define las acciones a realizar cuando se presiona el botón btn_make_test.
    def make_test(self):
        # Deshabilita el botón.
        self.btn_make_test.configure(state=DISABLED)

        # Genera la lista de intervalos de acuerdo a la cantidad de intervalos establecida por el input.
        self.intervals_list, self.intervals_average = TestChiCuadrado.divide_intervals(self.intervals)

        # Genera la lista de frecuencias esperadas y la frecuencia real para los intervalos obtenidos.
        self.expected_frequency, self.real_frequency = TestChiCuadrado.test_chi_cuadrado(
            self.generated_series,
            self.intervals_list)

        # Completa la tabla formateando los números para su correcta visualización con la cantidad de decimales
        # esperada.
        for i in range(len(self.intervals_list)):
            interval_min = '{:.4f}'.format(self.intervals_list[i][0])
            interval_max = '{:.4f}'.format(self.intervals_list[i][1])
            average = '{:.4f}'.format(self.intervals_average[i])
            expected = self.expected_frequency[i]
            real = self.real_frequency[i]

            self.frequency_table.insert("", "end", values=(interval_min, interval_max, average, expected, real))
            self.frequency_table.update()

        # Habilita el botón para generar la gráfica.
        self.btn_make_graph.configure(state=NORMAL)

    # Define las acciones a realizar al presionar el botón btn_make_graph.
    def make_graph(self):
        # Crea una serie de números que cumple con la frecuencia esperada.
        expected_series = TestChiCuadrado.generate_expected_distribution(self.intervals_average,
                                                                         self.expected_frequency[0],
                                                                         0,
                                                                         1)

        # Crea una matriz con los datos de las serie esperada y de la serie generada.
        data = column_stack((expected_series, self.generated_series))

        # Se crea una nueva ventana.
        window = Toplevel(self)

        # Crea la figura donde se mostrará la gráfica.
        figure = Figure(figsize=(10, 9), dpi=100)

        # Agrega un graficador a la figura.
        plot = figure.add_subplot(111)

        # Crea el histograma con los datos almacenados en la matriz data.
        plot.hist(data, label=('Esperada', 'Real'), bins=10)

        # Renderiza el histograma en la figura.
        scatter3 = FigureCanvasTkAgg(figure, window)

        # Define la posición de la gráfica.
        scatter3.get_tk_widget().pack(fill=BOTH, padx=20, pady=20)

        # Setea el título.
        plot.set_title('Distribución de Frecuencias', fontsize=14)

        # Setea que se creen las leyendas correspondientes.
        plot.legend()

        # Setea el nombre de los ejes.
        plot.set_xlabel('Intervalo', fontsize=14)
        plot.set_ylabel('Frecuencia', fontsize=14)

    # Validación de los inputs.
    #
    # "Recorre" de arriba para abajo inputs de la UI. Al encontrar un error "corta" y devuelve False y el String de
    # error.
    # Si no encuentra ningún error, devuelve True y String vacío.
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

    # Método que define las acciones a realizar al presionar el botón btn_back.
    def go_back(self, controller):
        # Rehabilita los botones.
        self.language_button.configure(state=NORMAL)
        self.congruential_button.configure(state=NORMAL)

        # Setea la variable del tipo de generador en congruecial para poder limpiar los inputs.
        self.switch_variable.set = CONG_MIX
        self.switch_method()

        # Limpia los inputs del método congruencial.
        self.m_input.delete(0, END)
        self.seed_input.delete(0, END)
        self.a_input.delete(0, END)
        self.c_input.delete(0, END)

        # Vuelve a setear el tipo de generador en el determinado.
        self.switch_variable.set = OS

        # Rehabilita los inputs de generación.
        self.quantity_input.configure(state=NORMAL)
        self.intervals_input.configure(state=NORMAL)

        # Limpia los inputs de generación
        self.quantity_input.delete(0, END)
        self.intervals_input.delete(0, END)

        # Limpia las tablas
        self.serie_table.delete(*self.serie_table.get_children())
        self.frequency_table.delete(*self.serie_table.get_children())

        # Setea los botones en su estado inicial.
        self.btn_calculate.configure(state=NORMAL)
        self.btn_make_test.configure(state=DISABLED)

        # Setea las variables en su estado inicial.
        self.total_count.configure(text="")
        self.generated_series = []
        self.quantity = 0
        self.intervals = 0
        self.intervals_list = []
        self.intervals_average = []
        self.expected_frequency = []
        self.real_frequency = []

        # Regresa a la página original.
        controller.show_frame(StartPage)


def main():  # type: () -> None
    app = NumberGenerator()
    app.wm_title("Generador de Números Aleatorios")
    app.mainloop()


if __name__ == "__main__":
    main()
