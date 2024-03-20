from ttkbootstrap import Window, Frame, Label, Button, Treeview, Scrollbar, TOP, SUCCESS, HEADINGS, BOTH, CENTER, HORIZONTAL, VERTICAL, RIGHT, Y, BOTTOM, X, END
from cytoflow import Tube, ImportOp, ThresholdOp, DensityGateOp, FlowPeaksOp
from numpy import argmax, sort
from os import path
from matplotlib.pyplot import subplots, close
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
theme_name = "cyborg"
application_title = "Tkinter experiment"
minimum_window_width = 800
minimum_window_height = 600
f = r"1.fcs"
xchannel = "R1-A"
ychannel = "B8-A"
scale = "log"
channel = "B4-A"
cluster_name = "FlowPeaks"

# Función principal que genera la interfaz gráfica del programa y carga todos los datos
def main():
    '''
    Función principal que genera la interfaz gráfica del programa y carga todos los datos
    '''
    # Generamos la ventana con un tema específico, un título y unas dimensiones mínimas
    root = Window(themename = theme_name)
    root.title(application_title)
    root.minsize(minimum_window_width, minimum_window_height)
    
    # Dimensionamos y posicionamos la ventana en la pantalla
    window_size_placement(root)

    # El estado de la ventana será maximizado
    # root.state("zoomed")

    # Generamos los botones
    generate_buttons(root)

    # Generamos la tabla de datos
    generate_treeview(root)

    # Generamos el hilo que genera la ventana del programa
    root.mainloop()

# Función que dimensiona y posiciona la ventana en la pantalla
def window_size_placement(root):
    '''
    Función que dimensiona y posiciona la ventana en la pantalla
    '''
    # Obtiene las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula la posición del centro
    position_top = int(screen_height / 2 - minimum_window_height / 2)
    position_right = int(screen_width / 2 - minimum_window_width / 2)

    # Posiciona la ventana en el centro de la pantalla
    root.geometry(f"{minimum_window_width}x{minimum_window_height}+{position_right}+{position_top}")

# Función que genera los botones
def generate_buttons(root):
    '''
    Función que genera los botones
    '''
    # Creamos un frame en el que generaremos los botones
    buttons_frame = Frame(root)
    buttons_frame.place(relx = 0, rely = 0, relwidth = 0.2, relheight = 1)

    label1 = Label(buttons_frame)
    label1.pack(side = TOP, expand = True)
    
    # Creamos los botones
    load_files_button = Button(buttons_frame, text = "Load files")
    load_files_button.pack(side = TOP, pady = 50)

    delete_button = Button(buttons_frame, text = "Delete")
    delete_button.pack(side = TOP, pady = 50)

    export_button = Button(buttons_frame, text = "Export")
    export_button.pack(side = TOP, pady = 50)

    label2 = Label(buttons_frame)
    label2.pack(side = TOP, expand = True)

# Función que genera la tabla con los datos
def generate_treeview(root):
    '''
    Función que genera la tabla con los datos
    '''
    # Creamos un frame en el que generaremos el treeview
    treeview_frame = Frame(root)
    treeview_frame.place(relx = 0.2, rely = 0, relwidth = 0.8, relheight = 0.5)

    # Definimos las columnas
    columns = ("file_name", "total_number_events", "number_cluster_events", "percentage_number_events_total", "mfi_cluster")

    # Creamos el Treeview
    treeview = Treeview(treeview_frame, bootstyle = SUCCESS, columns = columns, show = HEADINGS) # NOTA: Para mostrar la columna #0, poner el atributo show = TREEHEADINGS
    treeview.pack(fill = BOTH, expand = True, padx = (0, 20))
    treeview.column(columns[0], minwidth = 162, width = 162, anchor = CENTER)
    treeview.column(columns[1], minwidth = 100, width = 100, anchor = CENTER)
    treeview.column(columns[2], minwidth = 125, width = 125, anchor = CENTER)
    treeview.column(columns[3], minwidth = 150, width = 150, anchor = CENTER)
    treeview.column(columns[4], minwidth = 75, width = 75, anchor = CENTER)

    # Definimos las cabeceras
    treeview.heading(columns[0], text = "File name")
    treeview.heading(columns[1], text = "Total no. of events")
    treeview.heading(columns[2], text = "No. cluster events")
    treeview.heading(columns[3], text = "% no. of events over total")
    treeview.heading(columns[4], text = "MFI cluster")

    # Añadimos los scrollbars del treeview
    add_treeview_scrollbars(treeview_frame, treeview)

    # Añadimos los datos al treeview
    add_data_treeview(root, treeview)

# Función que añade los scrollbars del treeview
def add_treeview_scrollbars(treeview_frame, treeview):
    '''
    Función que añade los scrollbars del treeview
    '''
    vertical_scrollbar = Scrollbar(treeview_frame, orient = VERTICAL, command = treeview.yview)
    horizontal_scrollbar = Scrollbar(treeview_frame, orient = HORIZONTAL, command = treeview.xview)
    treeview.configure(yscrollcommand = vertical_scrollbar.set, xscrollcommand = horizontal_scrollbar.set)
    vertical_scrollbar.pack(side = RIGHT, fill = Y, padx = 5, pady = (0, 20))
    horizontal_scrollbar.pack(side = BOTTOM, fill = X, pady = 5)

# Función que añade los datos al treeview
def add_data_treeview(root, treeview):
    '''
    Función que añade los datos al treeview
    '''
    treeview.insert("", END, values = new_experiment(root, f))
    # treeview.insert("", END, values = ("A"))
    # treeview.insert("", END, values = ("B"))
    # treeview.insert("", END, values = ("C"))
    # treeview.insert("", END, values = ("D"))
    # treeview.insert("", END, values = ("E"))
    # treeview.insert("", END, values = ("F"))
    # treeview.insert("", END, values = ("G"))
    # treeview.insert("", END, values = ("H"))
    # treeview.insert("", END, values = ("I"))
    # treeview.insert("", END, values = ("J"))
    # treeview.insert("", END, values = ("K"))
    # treeview.insert("", END, values = ("L"))
    # treeview.insert("", END, values = ("M"))
    # treeview.insert("", END, values = ("N"))
    # treeview.insert("", END, values = ("Ñ"))
    # treeview.insert("", END, values = ("O"))
    # treeview.insert("", END, values = ("P"))
    # treeview.insert("", END, values = ("Q"))
    # treeview.insert("", END, values = ("R"))
    # treeview.insert("", END, values = ("S"))
    # treeview.insert("", END, values = ("T"))
    # treeview.insert("", END, values = ("U"))
    # treeview.insert("", END, values = ("V"))
    # treeview.insert("", END, values = ("W"))
    # treeview.insert("", END, values = ("X"))
    # treeview.insert("", END, values = ("Y"))
    # treeview.insert("", END, values = ("Z"))

# Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
def new_experiment(root, f):
    '''
    Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    '''
    tube = Tube(file = f)

    import_op = ImportOp(tubes = [tube], channels = {xchannel : xchannel, ychannel : ychannel, channel : channel})
    experiment = import_op.apply()

    # Realizamos la operación Threshold sobre el experimento
    operation_name = "Threshold"
    threshold_op = ThresholdOp(name = operation_name, channel = xchannel, threshold = 2000)
    experiment_threshold = threshold_op.apply(experiment)
    experiment_threshold = experiment_threshold.query(operation_name)

    # Realizamos la operación DensityGate sobre el experimento
    operation_name = "DensityGate"
    density_gate_op = DensityGateOp(name = operation_name, xchannel = xchannel, xscale = scale, ychannel = ychannel, yscale = scale, keep = 0.5)
    density_gate_op.estimate(experiment_threshold)
    experiment_density_gate = density_gate_op.apply(experiment_threshold)
    experiment_density_gate = experiment_density_gate.query(operation_name)

    # Realizamos la operación de clustering FlowPeaks sobre el experimento
    flow_peaks_op = FlowPeaksOp(name = cluster_name, channels = [xchannel, ychannel], scale = {xchannel : scale, ychannel : scale}, h0 = 3)
    flow_peaks_op.estimate(experiment_density_gate)
    experiment_flow_peaks = flow_peaks_op.apply(experiment_density_gate)
    argmax(experiment_flow_peaks[[cluster_name]].groupby(by = experiment_flow_peaks[cluster_name]).count())

    # Una vez realizadas las opereaciones, pintamos la gráfica de puntos en la ventana del programa
    generate_canvas(root, experiment_flow_peaks)

    # Asignamos a variables los datos que queremos retornar del experimento
    file_name = path.basename(f)
    total_number_events = experiment.data.shape[0]
    number_events_cluster_interest = experiment_flow_peaks.data.shape[0]
    percentage_represents_number_events_cluster_interest_total = '{:.2%}'.format(number_events_cluster_interest / total_number_events)
    mfi_cluster_interest = '{:.2f}'.format(median_fluorescence_intensity_cluster_interest(experiment_flow_peaks))
    
    # Retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    return (file_name, total_number_events, number_events_cluster_interest, percentage_represents_number_events_cluster_interest_total, mfi_cluster_interest)

# Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
def median_fluorescence_intensity_cluster_interest(experiment_flow_peaks):
    '''
    Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
    '''
    # Ordenamos los datos del experimento en el canal deseado
    sorted_data = sort(experiment_flow_peaks[channel])

    # Obtenemos el número total de datos
    total_number_data = len(sorted_data)
    
    # Si el número de datos es par
    if total_number_data % 2 == 0:
        return (sorted_data[total_number_data // 2 - 1] + sorted_data[total_number_data // 2]) / 2
    # Si el número de datos es impar
    else:
        return sorted_data[total_number_data // 2]

# Función que pinta los eventos del cluster en una gráfica en la ventana del programa
def generate_canvas(root, experiment_flow_peaks):
    '''
    Función que pinta los eventos del cluster en una gráfica en la ventana del programa
    '''
    # Creamos un frame en el que generaremos el canvas
    canvas_frame = Frame(root)
    canvas_frame.place(relx = 0.2, rely = 0.5, relwidth = 0.8, relheight = 0.5)

    data_frame = experiment_flow_peaks.data

    # Dibujamos la gráfica de puntos
    figure, axes = subplots()

    # Dibujamos los puntos, diferenciando los clusters por color
    clusters = data_frame[cluster_name].unique()
    for cluster in clusters:
        data_frame_cluster = data_frame[data_frame[cluster_name] == cluster]
        axes.scatter(data_frame_cluster[xchannel], data_frame_cluster[ychannel], label = f"{cluster_name} {cluster}", s = 5, color = "green")

    # Mostramos la leyenda
    axes.legend()
    
    # Crear el canvas de tkinter y añadir la figura de matplotlib
    figure_canvas_tk_agg = FigureCanvasTkAgg(figure, master = canvas_frame)
    figure_canvas_tk_agg.draw()
    figure_canvas_tk_agg = figure_canvas_tk_agg.get_tk_widget()
    figure_canvas_tk_agg.pack(fill = BOTH, expand = True, padx = 100, pady = 20)
    close(fig = figure)

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Ejecutamos la función principal para generar la ventana del programa
    main()