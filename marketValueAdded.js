/**
 * Calculates the market value and market value added (MVA).
 * @param {number} sharePrice - The price per share of the stock.
 * @param {number} sharesOutstanding - The total number of outstanding shares.
 * @param {number} capitalInvested - The amount of capital invested.
 * @returns {Object} An object containing the calculated values.
 * @property {number} marketValue - The total market value of the company.
 * @property {number} marketValueAdded - The market value added (MVA).
 */

export default function MarketValueAdded(sharePrice, sharesOutstanding, capitalInvested) {
    const marketValuePrice = sharePrice * sharesOutstanding;
    const marketValuePriceAdded = marketValuePrice - capitalInvested;

    return {
        marketValuePrice,
        marketValuePriceAdded
    };
};