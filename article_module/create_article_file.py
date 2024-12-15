import os
import sys
from typing import Dict, List

# Local Imports
# Local Imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_module import get_ai_content


# \n
# TODO: Add content
def create_article_content(params: Dict[str, str], returns: Dict[str, str], file_names: Dict[str, str], files_content: List[str], allow_ai: bool = True):
    #html_name = file_names['html']
    #file_name = file_names['file']

    # TODO: Add AI


    pretty_name = file_names['pretty_name']
    nunjucks_file_name = file_names['nunjucks']

    abbreviation = create_abbreviation(pretty_name)

    # Example: "Compound Annual Growth Rate (CAGR) Calculator"
    space = " "
    if abbreviation: # TODO: TEST THIS!
        abbreviation = space + abbreviation
    name_and_abbreviation = pretty_name + abbreviation
    calculator_title = name_and_abbreviation + " Calculator"

    # AI
    ai_meta_description = ""
    ai_article_content = ""

    if allow_ai: # If I allow AI. Because my PC is too slow.
        ai_returns = get_ai_content.create_ai_content(calculator_title, returns, params, files_content)

        ai_meta_description = ai_returns['meta_description']
        ai_article_content = ai_returns['article_content']

    # TODO: Make sure ai_meta_description is max 150 characters.


    category = "investment"
    # TODO: Make this dynamic.
    schema_sub_category = "InvestmentCalculator" # InvestmentCalculator

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



""" def create_abbreviation(input_string):
    words = input_string.split()  # Split the string into words
    abbreviation = ''.join(word[0].upper() for word in words)  # Get first letter of each word
    return "(" + abbreviation + ")" """

def create_abbreviation(input_string):
    words = input_string.split()  # Split the string into words
    abbreviation = ''.join(word[0].upper() for word in words)  # Get first letter of each word
    if len(abbreviation) <= 1:  # Check if abbreviation is one character or less
        return ""  # Return an empty string
    return "(" + abbreviation + ")"  # Return the formatted abbreviation



def main():
    print("Creating dummy article.")
    title = "Dummy Article"
    #article_content = create_article_content(title)
    #print(article_content)


if __name__ == '__main__':
    main()