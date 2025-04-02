from shiny import App, render, ui, reactive
from drugchecker.models import predict_admet
from drugchecker.utils import (get_risk_class, read_smiles, format_value)

# UI Definition
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(open("styles.css").read()),
    ),
    ui.tags.title("ADMET Prediction Tool"),
    ui.div(
        ui.div(
            ui.h2("ADMET Prediction Tool", class_="text-center mb-3"),
            ui.p("Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity properties", class_="text-center opacity-75"),
            class_="header"
        ),
        class_="container"
    ),
    ui.div(
        ui.div(
            # Metrics Grid
            ui.div(
                ui.div(
                    ui.tags.i(class_="fas fa-flask metric-icon"),
                    ui.p("Properties", class_="metric-title"),
                    ui.div(
                        ui.output_text("total_properties"),
                        class_="metric-value"
                    ),
                    class_="metric-card"
                ),
                ui.div(
                    ui.tags.i(class_="fas fa-chart-line metric-icon"),
                    ui.p("Predictions", class_="metric-title"),
                    ui.div(
                        ui.output_text("total_predictions"),
                        class_="metric-value"
                    ),
                    class_="metric-card"
                ),
                ui.div(
                    ui.tags.i(class_="fas fa-check-circle metric-icon"),
                    ui.p("Passed Rules", class_="metric-title"),
                    ui.div(
                        ui.output_text("passed_rules"),
                        class_="metric-value"
                    ),
                    class_="metric-card"
                ),
                ui.div(
                    ui.tags.i(class_="fas fa-exclamation-triangle metric-icon"),
                    ui.p("Warnings", class_="metric-title"),
                    ui.div(
                        ui.output_text("total_warnings"),
                        class_="metric-value"
                    ),
                    class_="metric-card"
                ),
                class_="metrics-grid"
            ),
            # Main Content
            ui.div(
                ui.div(
                    ui.div(
                        ui.tags.h3("Input", class_="section-title"),
                        ui.div(
                            ui.div(
                                ui.input_text_area("smiles", "Enter SMILES String", 
                                                 placeholder="Enter one SMILES string per line", 
                                                 height="120px"),
                                class_="form-control"
                            ),
                            ui.div(
                                ui.input_file("file", "Upload SMILES File", 
                                            accept=[".smi", ".txt"]),
                                class_="form-control"
                            ),
                            class_="input-section"
                        ),
                        ui.div(
                            ui.tags.h3("Options", class_="section-title"),
                            ui.div(
                                ui.div(
                                    ui.input_checkbox("use_custom_model", "Use Custom Model"),
                                    class_="mt-3"
                                ),
                                class_="input-section"
                            ),
                            class_="mt-4"
                        ),
                        class_="card"
                    ),
                    class_="col-md-4"
                ),
                ui.div(
                    ui.div(
                        ui.tags.h3("Results", class_="section-title"),
                        ui.div(
                            ui.tags.ul(
                                ui.tags.li(ui.tags.a("Physicochemical Properties", href="#physicochemical")),
                                ui.tags.li(ui.tags.a("Pharmacokinetics", href="#pharmacokinetics")),
                                ui.tags.li(ui.tags.a("Drug-likeness", href="#druglikeness")),
                                ui.tags.li(ui.tags.a("Medicinal Chemistry", href="#medicinal")),
                                class_="nav nav-tabs"
                            ),
                            ui.div(
                                ui.div(
                                    ui.h4("Physicochemical Properties", id="physicochemical", class_="section-subtitle"),
                                    ui.output_ui("physicochemical_results"),
                                ),
                                ui.div(
                                    ui.h4("Pharmacokinetics", id="pharmacokinetics", class_="section-subtitle"),
                                    ui.output_ui("pharmacokinetics_results"),
                                ),
                                ui.div(
                                    ui.h4("Drug-likeness", id="druglikeness", class_="section-subtitle"),
                                    ui.output_ui("druglikeness_results"),
                                ),
                                ui.div(
                                    ui.h4("Medicinal Chemistry", id="medicinal", class_="section-subtitle"),
                                    ui.output_ui("medicinal_results"),
                                ),
                                class_="results-content"
                            ),
                            class_="results-container"
                        ),
                        class_="card"
                    ),
                    class_="col-md-8"
                ),
                class_="row"
            ),
            class_="container"
        ),
        class_="container"
    ),
    ui.div(
        ui.div(
            ui.p(
                "This tool is for research purposes only. Please cite appropriately. | Author: ",
                ui.tags.a("Visit teslim404.com", href="https://teslim404.com", target="_blank"),
                class_="text-center"
            ),
            class_="footer"
        ),
        class_="container"
    ),
    # Add Font Awesome for icons
    ui.tags.link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ),
)

# Server Definition
def server(input, output, session):
    @reactive.Calc
    def get_smiles():
        smiles_from_file = read_smiles(input.file())
        if smiles_from_file is not None:
            return smiles_from_file
        smiles_list = [s.strip() for s in input.smiles().split('\n') if s.strip()]
        return smiles_list[0] if smiles_list else None

    def format_results(category_results):
        if not category_results:
            return "No data available"
        
        result_lines = []
        for prop, value in category_results.items():
            risk_class = get_risk_class(value)
            formatted_value = format_value(value)
            result_lines.append(
                f'<div class="prediction-item"><span class="prediction-title">{prop}:</span> '
                f'<span class="prediction-value {risk_class}">{formatted_value}</span></div>'
            )
        
        return " ".join(result_lines)

    def get_risk_icon(risk_class):
        if risk_class == 'high-risk':
            return '<i class="fas fa-exclamation-circle"></i>'
        elif risk_class == 'medium-risk':
            return '<i class="fas fa-exclamation-triangle"></i>'
        else:
            return '<i class="fas fa-check-circle"></i>'

    def get_risk_label(risk_class):
        if risk_class == 'high-risk':
            return 'High Risk'
        elif risk_class == 'medium-risk':
            return 'Medium Risk'
        else:
            return 'Low Risk'

    @output
    @render.text
    def total_properties():
        smiles = get_smiles()
        if not smiles:
            return "0"
        try:
            results = predict_admet(smiles)
            total = sum(len(category) for category in results.values())
            return str(total)
        except:
            return "0"

    @output
    @render.text
    def total_predictions():
        smiles = get_smiles()
        if not smiles:
            return "0"
        try:
            results = predict_admet(smiles)
            return str(len(results))
        except:
            return "0"

    @output
    @render.text
    def passed_rules():
        smiles = get_smiles()
        if not smiles:
            return "0"
        try:
            results = predict_admet(smiles)
            passed = sum(1 for category in results.values() 
                        for value in category.values() 
                        if get_risk_class(value) == "low-risk")
            return str(passed)
        except:
            return "0"

    @output
    @render.text
    def total_warnings():
        smiles = get_smiles()
        if not smiles:
            return "0"
        try:
            results = predict_admet(smiles)
            warnings = sum(1 for category in results.values() 
                         for value in category.values() 
                         if get_risk_class(value) == "high-risk")
            return str(warnings)
        except:
            return "0"

    @output
    @render.text
    def physicochemical_results():
        smiles = get_smiles()
        if not smiles:
            return "Please enter a SMILES string"
        
        try:
            results = predict_admet(smiles)
            physicochemical = results.get("Physicochemical Properties", {})
            return format_results(physicochemical)
        except Exception as e:
            return f"Error: {str(e)}"

    @output
    @render.text
    def pharmacokinetics_results():
        smiles = get_smiles()
        if not smiles:
            return "Please enter a SMILES string"
        
        try:
            results = predict_admet(smiles)
            pharmacokinetics = results.get("Pharmacokinetics", {})
            return format_results(pharmacokinetics)
        except Exception as e:
            return f"Error: {str(e)}"

    @output
    @render.text
    def druglikeness_results():
        smiles = get_smiles()
        if not smiles:
            return "Please enter a SMILES string"
        
        try:
            results = predict_admet(smiles)
            druglikeness = results.get("Drug-likeness", {})
            return format_results(druglikeness)
        except Exception as e:
            return f"Error: {str(e)}"

    @output
    @render.text
    def medicinal_results():
        smiles = get_smiles()
        if not smiles:
            return "Please enter a SMILES string"
        
        try:
            results = predict_admet(smiles)
            medicinal = results.get("Medicinal Chemistry", {})
            return format_results(medicinal)
        except Exception as e:
            return f"Error: {str(e)}"

app = App(app_ui, server) 