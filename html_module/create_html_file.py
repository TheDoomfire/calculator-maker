
import os
from typing import Dict


# \n
def create_html_content(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str]):
    print("create_html_content")

    print("params:")
    print(params)
    print("returns:")
    print(returns)
    print("file_names:")
    print(file_names)

    html_name = file_names['html']

    new_html_file = f"""{{% include 'components/warning-no-js.njk' %}}\n\n
{{% set calculatorName = "{html_name}" %}}\n\n
{{% import 'components/inputs/input-custom.njk' as customInput %}}
"""
    
    # TODO: create "imports" for the inputs.
    all_imports = []
    # {'type': 'number', 'name': 'capitalInvested', 'description': 'The amount of capital invested.', 'element': 'unsupported type', 'pretty_name': 'Capital Invested'}
    params_return = [params, returns]
    for pr in params_return:
        for param in pr:
            print("param:", param)
            if 'element' in param:
                element = param['element']
                if element == 'currency' and not 'currency' in all_imports:
                    all_imports.append("currency")
                elif element == "percent" and not "percent" in all_imports:
                    all_imports.append("percent")
                #elif element == "year" and not "custom" in all_imports:
                #    all_imports.append("custom")
    
    # Add imports.
    print("all_imports:", all_imports)
    for imp in all_imports:
        if imp == "currency":
            new_html_file += f"""{{% import 'components/inputs/input-currency.njk' as currencyInput %}}\n"""    
        elif imp == "percent":
            new_html_file += f"""{{% import 'components/inputs/input-percent.njk' as percentInput %}}\n"""
        #elif imp == "custom":
        #    new_html_file += f"""{{% import 'components/inputs/input-custom.njk' as customInput %}}\n"""

    new_html_file += "\n\n"

    new_html_file += f"""<section class="responsive-two">
\t<form id="form-{{ calculatorName }}">"""
    
    # add for loop for params
    # {'type': 'number', 'name': 'investmentReturnPercentage', 'description': 'The percentage return of the investment.', 'element': 'percent', 'pretty_name': 'Inves
    for param in params:
        if 'name' in param:
            element = param['element']
            key = param['name']
            pretty_name = param['pretty_name']
            print("key:", key)
            if element == 'currency':
                print("asd")
            #new_html_file += 

    return new_html_file