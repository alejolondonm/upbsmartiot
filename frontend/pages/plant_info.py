from dash import html, dcc

# Plant Information layout with styled collapsible sections
layout = html.Div([
    html.H1("Impatiens walleriana, ''Beso''", className="plant-info-title"),
    
    # Two-column layout: Image on the left, collapsible sections on the right
    html.Div([
        html.Div([
            html.Img(src="/assets/img/beso.jpg", className="plant-info-image")  # Image of the plant
        ], className="plant-image-column"),

        html.Div([
            # General Information Section
            html.Details([
                html.Summary("Información General 🌺", className="collapsible-summary"),
                html.Div([
                    html.P("Impatiens walleriana, también conocida como alegría del hogar, alegría de la casa, balsamina o miramelindo. Es una planta herbácea perenne, suculenta que puede alcanzar una altura de entre 15 y 60 cm. Los tallos son poco ramificados, glabros y algunas veces rojizos, enraizando en las nudos inferiores. Las flores pueden ser variables en color, rosadas, púrpuras, violeta, naranjas, rojas o blancas."),
                ], className="collapsible-content")
            ], className="collapsible-section", id='general-info'),

            # Temperatura
            html.Details([
                html.Summary("Temperature 🌡️", className="collapsible-summary"),
                html.Div([
                    html.P("Como hemos visto antes, no soporta el frío. De estar expuesta a temperaturas bajas o, incluso, heladas sus tallos se deteriorarán sin remedio. ¿Cuál es su rango de temperaturas ideal? Siempre superior a los 13º."),
                    html.P(""),
                    html.P("Tampoco podemos exponerla a corrientes de aire o cambios bruscos de temperatura. Pasarán factura a nuestra planta.")
                ], className="collapsible-content")
            ], className="collapsible-section", id='temperature-info'),

            # Humedad
            html.Details([
                html.Summary("Humedad 💧", className="collapsible-summary"),
                html.Div([
                    html.P("Empecemos por el riego, uno de los cuidados de la planta Alegría que suele provocar más problemas en su cultivo. Es importante saber que es una planta que no tolera los encharcamientos, ya que un exceso de agua o un mal drenaje pueden pudrid sus raíces. Por esta razón, es importante regar de forma moderada."),
                    html.P(""),
                    html.P("Además de esto, es importante saber que la Alegría agradece tener un cierto grado de humedad ambiental para estar cómoda. Algo que podemos conseguir colocándola sobre una bandeja con algún árido húmedo. Importante, sobre todo en interior, evitar mojar las hojas y flores: es una planta con cierta predisposición a enfermedades fúngicas como la Botritis.")
                ], className="collapsible-content")
            ], className="collapsible-section", id='humidity-info'),

            # Luz
            html.Details([
                html.Summary("Luz 🌟", className="collapsible-summary"),
                html.Div([
                    html.P("Será fundamental buscarle un emplazamiento luminoso que será clave para que nos regale su floración. Es más: si vemos que tira los capullos de flor sin llegar a abrirlos, nuestra planta nos estará indicando que no está en el lugar correcto. Si decidimos colocarla cerca de una ventana, tendremos que conocer cómo es la luz que entra por ella. La Alegría de la casa tolera sol directo, pero solo en las horas de menor incidencia. En caso de recibir luz de mediodía, podría quemarse."),
                    html.P(""),
                    html.P("Si optamos por plantarla en exterior, su ubicación ideal será ligeramente diferente. Para que esté cómoda y florezca, tendremos que buscar un emplazamiento de semisombra en el que reciba buena luz de la mañana. Y sí: al pie de arbustos, árboles o trepadoras puede ser el lugar ideal.")
                ], className="collapsible-content")
            ], className="collapsible-section", id='light-info')

        ], className="collapsible-column")
    ], className="two-column-layout"),
], className="plant-info-container")
