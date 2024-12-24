templateFormula = """
Do not include any additional text, explanations, or comments before or after the response.

Based on the javascript code create a readable formula with no javascript or any kind of code.
For each return value from the javascript code create a formula.
Each formula should have a h3 title with the name the formula, under the h2 "Formula".
The formula should be inside a paragraph tag with the class "formula".
Each formula should have "Example" as a h4 title.
Each example should be inside a paragraph tag with the class "example".
In the example dont add any text such as "For example" or "Example" or "The formula for" or anything else like that.

Turn the javascript code into a readable formula. For example:
JavaScript Symbol	Meaning	Readable/HTML Equivalent
+	Addition	+
-	Subtraction	-
*	Multiplication	× (HTML: &times;)
/	Division	÷ (HTML: &divide;)
**	Exponentiation	Superscript notation: x² or x^2
%	Modulus (Remainder)	Mod or %
=	Equals	=
>	Greater than	>
<	Less than	<
>=	Greater than or equal to	≥ (HTML: &ge;)
<=	Less than or equal to	≤ (HTML: &le;)



Wrap everything inside a section tag. No other html code outside of the section tags is allowed.

Files: {files}

Answer:
"""

templateFormula = """
Do not include any additional text, explanations, or comments before or after the response.
Take a JavaScript math formula and convert it into a human-readable format. Replace programming operators with traditional mathematical symbols and use superscripts for exponents. Provide both a plain-text version and an HTML version."

Example Input:
a * b + c ** 2

Expected Output:
Plain-text: a × b + c²
HTML: a &times; b + c<sup>2</sup>

Javascript math Operations Data:
JavaScript Symbol	Meaning	Readable/HTML Equivalent
+	Addition	+
-	Subtraction	-
*	Multiplication	× (HTML: &times;)
/	Division	÷ (HTML: &divide;)
**	Exponentiation	Superscript notation: x² or x^2
%	Modulus (Remainder)	Mod or %
=	Equals	=
>	Greater than	>
<	Less than	<
>=	Greater than or equal to	≥ (HTML: &ge;)
<=	Less than or equal to	≤ (HTML: &le;)

Answer:
"""


# TODO: Needs to be shorter and more direct? Needs to follow the formula & provide a better example.
templateExample = """
Prompt:
Write a concise example using this formula: "{formula}".
Use these exact numbers that calculates that formula: {formula_example}
    Use the formula as given, with no modifications or additions.
    Assume inputs directly within the formula.
    Do not display or mention the formula, other then as a example.
    Do not include steps, or intermediate calculations.
    Return only the inputs and the final result in a single, concise statement.
    Avoid lists, bullet points, or any formatting beyond the example itself.
    Have a short and brief explanation.

Answer:
"""

# If needed a list of steps then it should be inside of a ol list with class "steps".

checkExampleCalculation = """
Prompt:
Verify the calculation in the provided example based on the formula.

    If the calculation is correct: Return exactly True. Do not add any additional text, symbols, or formatting.
    If the calculation is incorrect: Return only the corrected example, formatted exactly like the original but with the correct calculation.

Do not include explanations, comments, or labels like "Corrected Calculation" or "Formula." Do not reformat the example. Return only the required output based on the rules above.

Example: {example}

Answer:

"""


templateMeaning = """
Do not include any additional text, explanations, or comments before or after the response.

Create text for "{title}" with the heading "Meaning". The heading should be a h2 html tag.

It should explain plain and simple the meaning of the calculation for {title}.
It should not explain anything about calculations or formula but the meaning of it.

Please wrap the text in a paragraph tag <p> or several.


Answer:
"""


# Meta description.
templateCalculator = """
Do not include any additional text, explanations, or comments before or after the response.
You will write a meta description for a given title. The max character count is 150 characters.
The meta description should be a detailed description of the title.
The meta description be written in a way that is understandable by a human. Easy and direct language is preferred.
Base it on these files data, the meta description is for the calculator in these files.
The javascript file is the actual formula for the calculator. And the html/nunjucks file is the template for the calculator.

Files: {files}

Title: {question}


Answer:
"""


# Meta description History
templateMetaDescriptionHistory = """
Do not include any additional text, explanations, or comments before or after the response. Nor do you need to include any ".
This meta description currently has {character_count} characters. But it is too long. So try to make it shorter and maximum of 150 characters.

Current Meta Description: {meta_description}

title: {question}

The meta description is for the calculator in these files.
files: {files}

Answer:
"""



# Template for the sections and all the H2 titles.
templateContent = """
Do not include any additional text, explanations, or comments before or after the response.
You will write for the title "{question}". The text will be html ready, each h2 will be a section. There will be no boilerplate html surrounding the sections they will be the highest level of the html.
All text should be in a paragraph tag for each text piece.
Here is a list of all the H2 titles in the content:
1. Formula - The formula for "{question}". It should be a H2 tag. It works like the javascript content and the inputs is from the html/nunjucks file and should mimic them and is only acceptable to change them slighly and if it increases the readability.
If there are several return values from the javascript file and about the under the "results" in the results part of the html/nunjucks file then write each forumla with it's name and it's own h3 or h4 "Example".
The example must have numbers in them that will be used in the formula but have numbers instead of only variables, and they must be calculated all the way so the users understand easily how to use the formulas.
The formula should be inside a p tag with the class "formula". The formula should look the a formula, with the inputs in them as variables but words will be seperated so for example "thisVariable" would be "This Variable". There should be a h3 or h4 "Example" that gives a short and easy to understand example.
If there are several formulas then have them all in its own p tag with class "formula", then under the "Example" title display each example for every formula, they can also have a strong tag above them to clearly indicate what formula it is, examples will be wrapped around a p tag with the class "example".
In the example dont add any text such as "For example" or "Example" or "The formula for" because it already exist in the class.
2. Meaning - The meaning of the "{question}". It should be a H2 tag and explain the meaning of the title but leave out the "calculator" part. It should be a short and easy to understand explanation, it must include the word "Meaning" in the meaning title.

Content: {files}

Title: {question}

No text will every not be in a paragraph tag.

Answer:
"""
