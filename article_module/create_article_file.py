import os
import sys
from typing import Dict, List

# Local Imports
# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_module import get_ai_content


# \n
# TODO: Add content
def create_article_content(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str], files_content: List[str]):
    #html_name = file_names['html']
    #file_name = file_names['file']

    # TODO: Add AI


    pretty_name = file_names['pretty_name']
    nunjucks_file_name = file_names['nunjucks']

    calculator_title = pretty_name + " Calculator"

    # AI 
    ai_returns = get_ai_content.create_ai_content(calculator_title, files_content)
    ai_meta_description = ai_returns['meta_description']
    ai_article_content = ai_returns['article_content']


    category = "investment"
    schema_sub_category = "InvestmentCalculator"

    content = "" # AI: Generate "Formula" + "Meaning" h2 titles.

    article_content = f"""---
title: "{calculator_title}"
layout: 'base.njk'
type: website
tags: ["calculator"]
description: "{ai_meta_description}"
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

        
        {ai_article_content}
        

        {{% include 'components/read-more.njk' %}}
        
    </div>
</article>
"""
    
    return article_content


def main():
    print("Creating dummy article.")
    title = "Dummy Article"
    #article_content = create_article_content(title)
    #print(article_content)


if __name__ == '__main__':
    main()