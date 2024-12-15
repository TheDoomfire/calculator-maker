from typing import Dict


# \n
def create_html_content(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str]):
    html_name = file_names['html']
    file_name = file_names['file']

    new_html_file = f"""{{% include 'components/warning-no-js.njk' %}}\n\n
{{% set calculatorName = "{html_name}" %}}\n\n
{{% import 'components/inputs/input-custom.njk' as customInput %}}
"""
    all_imports = []
    params_return = [params, returns]
    for pr in params_return:
        for param in pr:
            if 'element' in param:
                element = param['element']
                if element == 'currency' and not 'currency' in all_imports:
                    all_imports.append("currency")
                elif element == "percent" and not "percent" in all_imports:
                    all_imports.append("percent")
                elif element == "table" and not "table" in all_imports:
                    all_imports.append("table")
                elif element == "compound_frequency_select" and not "compound_frequency_select" in all_imports:
                    all_imports.append("compound_frequency_select")
                #elif element == "year" and not "custom" in all_imports:
                #    all_imports.append("custom")
    
    # Add imports.
    for imp in all_imports:
        if imp == "currency":
            new_html_file += f"""{{% import 'components/inputs/input-currency.njk' as currencyInput %}}\n"""    
        elif imp == "percent":
            new_html_file += f"""{{% import 'components/inputs/input-percent.njk' as percentInput %}}\n"""
        elif imp == "table":
            new_html_file += f"""{{% import 'components/tables/custom-table.njk' as customTable %}}\n"""
        elif imp == "compound_frequency_select":
            new_html_file += f"""{{% import "components/select/compounding-frequency.njk" as customSelectCompoundFrequency %}}\n"""
        #elif imp == "custom":
        #    new_html_file += f"""{{% import 'components/inputs/input-custom.njk' as customInput %}}\n"""

    new_html_file += "\n\n"

    # -------------- FORM  ---------------
    new_html_file += f"""<section class="responsive-two">
\t<form id="form-{{ calculatorName }}" class="form-calculator">\n"""
    
    # TODO: Add input fields.
    # add for loop for params
    # param: {'type': 'number', 'name': 'years', 'description': 'The number of years over which the investment has grown.', 'element': 'year', 'pretty_name': 'S'}
    for param in params:
        if 'name' in param:
            element = param['element']
            key = param['name'] # TODO: Need a better looking name.
            pretty_name = param['pretty_name']
            description = param['description']
            last_word = param['last_word'].capitalize()
            if element == 'currency':
                new_html_file += f"""\t\t{{{{ currencyInput.inputCurrency("{key}", "{pretty_name}", "{description}") }}}}\n"""
            elif element == 'percent':
                new_html_file += f"""\t\t{{{{ percentInput.inputPercent("{key}", "{pretty_name}", "{description}") }}}}\n"""
            elif element == 'compound_frequency_select':
                new_html_file += f"""\t\t<label title="{description}" for={key}>{pretty_name}:&nbsp;{{{{ customSelectCompoundFrequency.compoundingFrequency("1", "{key}") }}}}</label>\n""" # TODO: TRY THIS!
            else: # TODO: Might come to issue later.
                new_html_file += f"""\t\t{{{{ customInput.inputCustom("{key}", "{pretty_name}", "0 {last_word}", "{description}") }}}}\n"""

    new_html_file += "\t</form>\n"

    # -------------- RESULTS ---------------
    new_html_file += f"""\t<div class="compound-result">
\t\t<span class="big-text">Result</span>
"""
    for ret in returns:
        if 'name' in ret:
            element = ret['element']
            if element != 'table':
                key = ret['name']
                pretty_name = ret['pretty_name']
                new_html_file += f"""\t\t<strong>{pretty_name}</strong>\n"""
                placeholder = ""
                if element == 'currency':
                    placeholder = "$0"
                elif element == 'percent':
                    placeholder = "0%"
                elif element == 'unsupported type':
                    placeholder = "0"
                else: # TODO: Might come to issue later.
                    placeholder = f"0 {key}"
                new_html_file += f"""\t\t<span id="result-{key}" class="color-plus big-bold">{placeholder}</span>\n"""


    new_html_file += "\t</div>\n</section>\n\n"
    # Chart
    new_html_file += """<canvas id="chart-{{ calculatorName }}" class="lineChart" role="img"></canvas>\n\n"""

    # TODO: Add table.
    tableID = "table-" + html_name
    for ret in returns:
        if 'name' in ret:
            element = ret['element']
            key = ret['name']
            pretty_name = ret['pretty_name']
            if element == 'table':
                # ERROR: {{ customTable.tableCustom("table-compound-annual-growth-rate")}} NO IMPORT?
                new_html_file += f"""{{{{ customTable.tableCustom("{tableID}")}}}}\n"""

    # Related Calculators
    new_html_file += """{% include 'components/new-calculators.njk' %}\n\n"""

    new_html_file += f"""<script type="module" src="/scripts/forms/{file_name}" defer></script>\n"""
    new_html_file += "{% include 'components/footer/footerScripts.njk' %}"



    return new_html_file