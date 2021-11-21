# Readme
## Overview
Investment Rebalancer is a terminal tool that helps one to rebalance one's portfolio. A configuration is used to define the classifications into which you want to divide your portfolio (e.g. regions, factor investing, core/satellite).

## Example configurations
### 70/30 portfolio
This example describes a classic 70/30 portfolio. The portfolio is invested 70% in developed markets and 30% in emerging markets.
In this example, the two ETFs *Lyxor Core MSCI World* and Lyxor *MSCI Emerging Markets* were chosen as investments.
```json
{
  "classifications": {
    "Regions": {
      "Developed World": {
        "percentage": 70.0
      },
      "Emerging Markets": {
        "percentage": 30.0
      }
    }
  },
  "investments": {
    "LU1781541179": {
      "name": "Lyxor Core MSCI World",
      "enabled": true,
      "quantity": 100,
      "ter": 0.12,
      "categories": "Developed World"
    },
    "LU0635178014": {
      "name": "Lyxor MSCI Emerging Markets",
      "enabled": true,
      "quantity": 50,
      "ter": 0.14,
      "categories": "Emerging Markets"
    }
  }
}
```

### 70/30 portfolio with small caps
This example is an extension to the above 70/30 portfolio. Again, 70% of the capital is allocated to developed markets and 30% to emerging markets. In addition to the already existing classification Regions, there is now also a classification Factor.  15% of the capital is supposed to be invested with the factor small caps. The remaining 85% should be invested in large and mid caps.
In addition the two ETFs iShares *MSCI World Small Cap* and *SPDR MSCI Emerging Markets Small Cap* were selected for this example.
```json
{
  "classifications": {
    "Regions": {
      "Developed World": {
        "percentage": 70.0
      },
      "Emerging Markets": {
        "percentage": 30.0
      }
    },
    "Factor": {
      "Large Cap": {
        "percentage": 85.0
      },
      "Small Cap": {
        "percentage": 15.0
      }
    }
  },
  "investments": {
    "LU1781541179": {
      "name": "Lyxor Core MSCI World",
      "enabled": true,
      "quantity": 200,
      "ter": 0.12,
      "categories": "Developed World,Large Cap"
    },
    "LU0635178014": {
      "name": "Lyxor MSCI Emerging Markets",
      "enabled": true,
      "quantity": 50,
      "ter": 0.14,
      "categories": "Emerging Markets,Large Cap"
    },
    "IE00BF4RFH31": {
      "name": "iShares MSCI World Small Cap",
      "enabled": true,
      "quantity": 65,
      "ter": 0.35,
      "categories": "Developed World,Small Cap"
    },
    "IE00B48X4842": {
      "name": "SPDR MSCI Emerging Markets Small Cap",
      "enabled": true,
      "quantity": 2,
      "ter": 0.55,
      "categories": "Emerging Markets,Small Cap"
    }
  }
}
```
