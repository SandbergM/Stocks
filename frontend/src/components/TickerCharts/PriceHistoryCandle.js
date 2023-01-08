
import React from 'react';
import { useEffect, useContext, useState } from 'react'

import { TickerContext } from '../../contexts/TickerContextProvider.js';

import ApexCharts from 'apexcharts'

function PriceHistoryCandle() {

  const {
    dates,
    wma10,
    wma20,
    wma50,
    wma100,
    adjClosePrices,
    closePrices,
    openPrices,
    highPrices,
    lowPrices,
    candleSticksData,
    bollingerUpper,
    bollingerLower,
  } = useContext(TickerContext);
  const [chart, setChart] = useState(false);
  useEffect(() => {

    if (dates.length !== 0) {

      var options = {
        series: [
          {
            name: 'candle',
            type: 'candlestick',
            data: candleSticksData

          },
          {
            name: 'Bollinger Upper',
            type: 'line',
            data: bollingerUpper
          },
          {
            name: 'Bollinger Lower',
            type: 'line',
            data: bollingerLower
          },
          {
            name: 'Close',
            type: 'line',
            data: closePrices
          },
          {
            name: 'Open',
            type: 'line',
            data: openPrices
          },
          {
            name: 'High',
            type: 'line',
            data: highPrices
          },
          {
            name: 'low',
            type: 'line',
            data: lowPrices
          },
          {
            name: 'Adj Close',
            type: 'line',
            data: adjClosePrices
          },
          {
            name: 'WMA 10',
            type: 'line',
            data: wma10
          },
          {
            name: 'WMA 20',
            type: 'line',
            data: wma20
          },
          {
            name: 'WMA 50',
            type: 'line',
            data: wma50
          },
          {
            name: 'WMA 100',
            type: 'line',
            data: wma100
          },
        ],
        chart: {
          height: 600,
          type: 'line',
        },
        stroke: {
          width: [1]
        },

      };

      if (!chart) {
        let chart = new ApexCharts(document.querySelector("#PriceHistoryCandle"), options)
        chart.render();
        setChart(chart)
      } else {
        chart.updateOptions(options);
      }

    }
  }, [dates])

  return (
    <div>
      <div id="PriceHistoryCandle"></div>
    </div>
  );

}

export default PriceHistoryCandle;