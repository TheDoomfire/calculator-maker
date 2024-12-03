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