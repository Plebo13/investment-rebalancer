# Readme

## Overview

investment-rebalancer is a terminal application that helps one to rebalance one's portfolio. A configuration is used to define the classifications into which you want to divide your portfolio (e.g. regions, factor investing, core/satellite).

## Example configurations

### 70/30 portfolio

This example describes a classic 70/30 portfolio. The portfolio is invested 70% in developed markets and 30% in emerging markets.
In this example, the two ETFs _Lyxor Core MSCI World_ and Lyxor _MSCI Emerging Markets_ were chosen as investments.

```json
{
  "classifications": {
    "Regions": {
      "Developed World": {
        "target_allocation": 70.0,
        "assets": ["LU1781541179"]
      },
      "Emerging Markets": {
        "target_allocation": 30.0,
        "assets": ["LU0635178014"]
      }
    }
  },
  "etf": {
    "LU1781541179": {
      "name": "Lyxor Core MSCI World",
      "enabled": true,
      "quantity": 100,
      "ter": 0.12
    },
    "LU0635178014": {
      "name": "Lyxor MSCI Emerging Markets",
      "enabled": true,
      "quantity": 50,
      "ter": 0.14
    }
  }
}
```

### 70/30 portfolio with small caps

This example is an extension to the above 70/30 portfolio. Again, 70% of the capital is allocated to developed markets and 30% to emerging markets. In addition to the already existing classification Regions, there is now also a classification Factor. 15% of the capital is supposed to be invested with the factor small caps. The remaining 85% should be invested in large and mid caps.
In addition the two ETFs iShares _MSCI World Small Cap_ and _SPDR MSCI Emerging Markets Small Cap_ were selected for this example.

```json
{
  "classifications": {
    "Regions": {
      "Developed World": {
        "target_allocation": 70.0,
        "assets": ["LU1781541179", "IE00BF4RFH31"]
      },
      "Emerging Markets": {
        "target_allocation": 30.0,
        "assets": ["LU0635178014", "IE00B48X4842"]
      }
    },
    "Factor": {
      "Large Cap": {
        "target_allocation": 85.0,
        "assets": ["LU1781541179", "LU0635178014"]
      },
      "Small Cap": {
        "target_allocation": 15.0,
        "assets": ["IE00BF4RFH31", "IE00B48X4842"]
      }
    }
  },
  "etf": {
    "LU1781541179": {
      "name": "Lyxor Core MSCI World",
      "enabled": true,
      "quantity": 200,
      "ter": 0.12
    },
    "LU0635178014": {
      "name": "Lyxor MSCI Emerging Markets",
      "enabled": true,
      "quantity": 50,
      "ter": 0.14
    },
    "IE00BF4RFH31": {
      "name": "iShares MSCI World Small Cap",
      "enabled": true,
      "quantity": 65,
      "ter": 0.35
    },
    "IE00B48X4842": {
      "name": "SPDR MSCI Emerging Markets Small Cap",
      "enabled": true,
      "quantity": 2,
      "ter": 0.55
    }
  }
}
```
