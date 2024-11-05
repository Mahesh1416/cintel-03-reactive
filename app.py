import plotly.express as px
from shiny.express import input, ui
from shinywidgets import output_widget, render_widget, render_plotly
from shiny import render
import seaborn as sns
import palmerpenguins
from palmerpenguins import load_penguins
penguins_df = palmerpenguins.load_penguins()
from shiny import reactive

ui.page_opts(title="Mahesh Bashyal Penguin project", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar():
# Use the ui.h2() function to add a 2nd level header to the sidebar
    ui.h2("Sidebar")
    
 
ui.input_selectize("selected_attribute","Penguin's features",
                      ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
ui.input_numeric("plotly_bin_count", "number of bins",0)

# Use ui.input_slider() to create a slider input for the number of Seaborn bins
ui.input_slider("seaborn_bin_count","Choose number of bars",0,100,20)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species
ui.input_checkbox_group("selected_species_list","Species",
                           ["Adelie", "Gentoo", "Chinstrap"],selected=["Adelie"],inline=True)
# Use ui.hr() to add a horizontal rule to the sidebar
ui.hr() 

# Use ui.a() to add a hyperlink to the sidebar
ui.a("GitHub",href="https://github.com/Mahesh1416/cintel-02-data/tree/main",target= "_blank") #to add a hyperlink to the sidebar

# Main content layout
penguins = load_penguins()
    # Display the Plotly Histogram
with ui.layout_columns():
    with ui.card():        
        ui.card_header("Palmer Penguins Plotly Histogram")    
        @render_widget  
        def create_histogram_plot():  
            scatterplot = px.histogram(
                data_frame=penguins,
                x="body_mass_g",
                nbins=100,
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="Body Mass (g)",
            )    
            return scatterplot  

    # Display Data Table (showing all data)
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def data_table():
            return render.DataTable(penguins)

    # Display Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def data_grid():
            return render.DataGrid(penguins)


# Display the Scatterplot
with ui.layout_columns():
    with ui.card():        
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
                return px.scatter(penguins_df,
                    x="bill_length_mm",
                    y="body_mass_g",
                    color="species",
                    title="Penguins Plot (Plotly Express)",
                    labels={
                        "bill_length_mm": "Bill Length (mm)",
                        "body_mass_g": "Body Mass (g)",
                    },
                    size_max=8, # set the maximum marker size
                )


    
    # Display the Seaborn Histogram (showing all species)
    with ui.card():
        ui.card_header("Seaborn Histogram: All Species")

        @render.plot
        def seaborn_histogram():
            hist = sns.histplot(
                data=penguins, x="body_mass_g", bins=input.seaborn_bin_count()
            )
            hist.set_xlabel("Mass (g)")
            hist.set_ylabel("Count")
            return hist
            
@reactive.calc
def filtered_data():
    return penguins_df
   
