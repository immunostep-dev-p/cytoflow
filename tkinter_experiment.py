from tkinter import *
from ttkbootstrap import *
from cytoflow import *
from numpy import *
from os import *
from matplotlib.pyplot import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
theme_name = "cyborg"
application_title = "Tkinter experiment"
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
    # Generamos la ventana con un tema específico y un título
    root = Window(themename = theme_name)
    root.title(application_title)
    main_frame = Frame(root, bootstyle = "warning")
    main_frame.pack(fill = BOTH, expand = True)
    
    # Centramos la ventana en la pantalla
    center_window(root)
    root.state("zoomed")

    # Generamos la tabla de datos
    generate_treeview(main_frame)

    # Generamos el hilo que genera la ventana del programa
    root.mainloop()

# Función que centra la ventana en la pantalla
def center_window(root, window_width = 800, window_height = 600):
    '''
    Función que centra la ventana en la pantalla
    '''
    # Obtiene las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula la posición del centro
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Posiciona la ventana en el centro de la pantalla
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Función que genera la tabla con los datos
def generate_treeview(main_frame):
    '''
    Función que genera la tabla con los datos
    '''
    frame1 = Frame(main_frame, bootstyle = "info")
    frame1.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.5)
    # frame.pack(side = LEFT, fill = BOTH, expand = True)
    
    # Definimos las columnas
    columns = ("nombre_fichero", "numero_eventos_total", "numero_eventos_cluster_interes", "porcentaje_representa_numero_eventos_cluster_interes_sobre_total", "imf_cluster_interes")

    # Creamos el Treeview
    treeview = Treeview(frame1, bootstyle = "success", columns = columns, show = "headings")
    treeview.pack()
    treeview.column("nombre_fichero", width = 350, anchor = "center")
    treeview.column("numero_eventos_total", width = 100, anchor = "center")
    treeview.column("numero_eventos_cluster_interes", width = 125, anchor = "center")
    treeview.column("porcentaje_representa_numero_eventos_cluster_interes_sobre_total", width = 150, anchor = "center")
    treeview.column("imf_cluster_interes", width = 75, anchor = "center")

    # Definimos las cabeceras
    treeview.heading("nombre_fichero", text = "Nombre fichero")
    treeview.heading("numero_eventos_total", text = "Nº eventos total")
    treeview.heading("numero_eventos_cluster_interes", text = "Nº eventos cluster")
    treeview.heading("porcentaje_representa_numero_eventos_cluster_interes_sobre_total", text = "% nº eventos sobre total")
    treeview.heading("imf_cluster_interes", text = "IMF cluster")

    # Añadimos los datos al Treeview
    add_data_treeview(main_frame, treeview)

# Función que añade los datos a la tabla
def add_data_treeview(main_frame, treeview):
    '''
    Función que añade los datos a la tabla
    '''
    treeview.insert("", END, values = new_experiment(main_frame, f))

# Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
def new_experiment(main_frame, f):
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
    generate_canvas(main_frame, experiment_flow_peaks)

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

# Función que pinta los eventos del cluster en la ventana del programa
def generate_canvas(main_frame, experiment_flow_peaks):
    '''
    Función que pinta los eventos del cluster en la ventana del programa
    '''
    frame2 = Frame(main_frame, bootstyle = "danger")
    frame2.place(relx = 0, rely = 0.5, relwidth = 1, relheight = 0.5)
    # frame.pack(side = LEFT, fill = BOTH, expand = True)

    data_frame = experiment_flow_peaks.data

    # Dibujamos la gráfica de puntos
    figure, axes = subplots()

    # Dibujamos los puntos, diferenciando los clusters por color
    clusters = data_frame[cluster_name].unique()
    for cluster in clusters:
        data_frame_cluster = data_frame[data_frame[cluster_name] == cluster]
        axes.scatter(data_frame_cluster[xchannel], data_frame_cluster[ychannel], label = f"{cluster_name} {cluster}")

    # Mostramos la leyenda
    axes.legend()
    
    # Crear el canvas de tkinter y añadir la figura de matplotlib
    figure_canvas_tk_agg = FigureCanvasTkAgg(figure, master = frame2)
    figure_canvas_tk_agg.draw()
    figure_canvas_tk_agg.get_tk_widget().pack(pady = 10)
    # figure_canvas_tk_agg.get_tk_widget().config(width = 300, height = 250)

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Ejecutamos la función principal para generar la ventana del programa
    main()