from typing import Dict


# \n
def create_article_content(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str]):
    #html_name = file_names['html']
    #file_name = file_names['file']
    pretty_name = file_names['pretty_name']
    nunjucks_file_name = file_names['nunjucks']

    calculator_title = pretty_name + " Calculator"
    calculator_description = "" # TODO: Get AI to generate a text for this.
    category = "investment"
    schema_sub_category = "InvestmentCalculator"

    content = "" # AI: Generate "Formula" + "Meaning" h2 titles.

    article_content = f"""---
title: "{calculator_title}"
layout: 'base.njk'
type: website
tags: ["calculator"]
description: "{calculator_description}"
author: Albini
keywords: investing, calculator
category: ["{category}"]
schema_type: calculator
schema_category: FinanceApplication
schema_sub_category: {schema_sub_category}
---


<article class="posts">
    <div class="container">
        <h1>{{{{ title }}}}</h1>
        <br>
        <p>{{{{ description }}}}</p>
        <br>
        <br>
        {{% include 'components/calc/{nunjucks_file_name}' %}}

        
        {content}
        

        {{% include 'components/read-more.njk' %}}
        
    </div>
</article>
"""
    
    return article_content