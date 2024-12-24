test_js_content = """
/**
 * Calculates CAGR, Percent Return, and Simple Average Annual Return (SAAR).
 * @param {number} initialValue - The initial value of the investment.
 * @param {number} finalValue - The final value of the investment.
 * @param {number} years - The number of years over which the investment has grown.
 * @returns {object} An object containing CAGR, Percent Return, and SAAR.
 * @property {number} investmentReturn - The percentage return of the investment.
 * @property {number} simpleAverageAnnualReturn - The simple average annual return of the investment.
 * @property {number} cagr - The compound annual growth rate of the investment.
 * @property {number} tableData - The compound annual growth rate of the investment.
 */
import { prettifyMoney } from '/scripts/formats/Money.js';

// Also: "Annualized Rate of Return Calculator"

// TODO: Create table of each year's result.

export default function CompoundAnnualGrowthRate(
    initialValue, // Currency
    finalValue, // Currency 
    years, // Year
) {
    // Percent Return
    const investmentReturn = ((finalValue - initialValue) / initialValue) * 100;

    // Simple Average Annual Return (SAAR)
    const simpleAverageAnnualReturn = investmentReturn / years;

    // Compound Annual Growth Rate (CAGR)
    //const cagr = (Math.pow(finalValue / initialValue, 1 / years) - 1) * 100;
    const cagr = ((finalValue / initialValue) ** ((1 / years) - 1)) * 100;


    const tableData = [];
    let yearlyInvestmentValue = finalValue;
    for (let year = 1; year <= years; year++) { 
                // Calculate the projected value for the current year
                const projectedValue = Math.pow(finalValue / initialValue, year / years) * initialValue;
                // Calculate the CAGR for the current year
                // Add to the array and update yearlyInvestmentValue
                yearlyInvestmentValue = projectedValue;
                // To make it easier to read in a table.
                const Value = prettifyMoney(yearlyInvestmentValue);
                tableData.push({ "Year": year, "Result": Value });
    };

    // Return all results formatted
    return {
        investmentReturn, // Percent
        simpleAverageAnnualReturn, // Currency
        cagr, // Percent
        tableData, // Table
    };
};
"""

test_js_content2 = """ 
/**
 * Net Asset Value Calculator
 * @param {number} totalInvestments - Total investments (cash and cash equivalents, account receivable, etc.)
 * @param {number} cashAndCashEquivalents - Cash and cash equivalents
 * @param {number} accountReceivable - Account receivable
 * @param {number} shortTermLiabilities - Short-term liabilities
 * @param {number} longTermLiabilities - Long-term liabilities
 * @returns {object} navDetails - Details of the NAV calculation
 * @property {number} fundAssets - Fund assets
 * @property {number} fundLiabilities - Fund liabilities
 * @property {number} nav - Net asset value
 */


export default function NetAssetValue(
    totalInvestments, // Currency
    cashAndCashEquivalents, // Currency
    accountReceivable, // Currency
    shortTermLiabilities, // Currency
    longTermLiabilities, // Currency
    ) {
    // Calculate fund assets
    const fundAssets = totalInvestments + cashAndCashEquivalents + accountReceivable;

    // Calculate fund liabilities
    const fundLiabilities = shortTermLiabilities + longTermLiabilities;

    // Calculate NAV
    const nav = fundAssets - fundLiabilities;

    // Return the results in an array
    return {
        fundAssets, // Currency
        fundLiabilities, // Currency
        nav, // Currency
    };
};
"""


test_formula = """fundAssets = totalInvestments + cashAndCashEquivalents + accountReceivable"""
test_params = [{'name': 'totalInvestments', 'pretty_name': 'Total Investments', 'element': 'currency', 'description': 'Total investments (cash and cash equivalents, account receivable, etc.)', 'last_word': 'Investments'}, {'name': 'cashAndCashEquivalents', 'pretty_name': 'Cash And Cash Equivalents', 'element': 'currency', 'description': 'Cash and cash equivalents', 'last_word': 'Equivalents'}, {'name': 'accountReceivable', 'pretty_name': 'Account Receivable', 'element': 'currency', 'description': 'Account receivable', 'last_word': 'Receivable'}, {'name': 'shortTermLiabilities', 'pretty_name': 'Short Term Liabilities', 'element': 'currency', 'description': 'Short-term liabilities', 'last_word': 'Liabilities'}, {'name': 'longTermLiabilities', 'pretty_name': 'Long Term Liabilities', 'element': 'currency', 'description': 'Long-term liabilities', 'last_word': 'Liabilities'}]
test_returns = [{'name': 'fundAssets', 'pretty_name': 'Fund Assets', 'element': 'currency', 'description': 'Fund assets', 'last_word': 'Assets', 'html_formula': '<math xmlns="http://www.w3.org/1998/Math/MathML" class="formula">Fund assets = Total investments + Cash and cash equivalents + Account receivable</math>', 'formula_variables': ['totalInvestments', 'cashAndCashEquivalents', 'accountReceivable']}, {'name': 'fundLiabilities', 'pretty_name': 'Fund Liabilities', 'element': 'currency', 'description': 'Fund liabilities', 'last_word': 'Liabilities', 'html_formula': '<math xmlns="http://www.w3.org/1998/Math/MathML" class="formula">Fund liabilities = Short term liabilities + Long term liabilities</math>', 'formula_variables': ['shortTermLiabilities', 'longTermLiabilities']}, {'name': 'nav', 'pretty_name': 'Nav', 'element': 'currency', 'description': 'Net asset value', 'last_word': 'nav', 'html_formula': '<math xmlns="http://www.w3.org/1998/Math/MathML" class="formula">Nav = Fund assets - Fund liabilities</math>', 'formula_variables': ['fundAssets', 'fundLiabilities']}]