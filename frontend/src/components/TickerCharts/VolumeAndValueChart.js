
import React from 'react';
import { useEffect, useContext, useState } from 'react'

import { TickerContext } from '../../contexts/TickerContextProvider.js';

import ApexCharts from 'apexcharts'

function VolumeAndValueChart() {

  const { closePrices, adjClosePrices, openPrices, dates, highPrices, lowPrices, wma10, wma20, wma50, wma100 } = useContext(TickerContext);
  const [chart, setChart] = useState(false);
  useEffect(() => {

    if (dates.length !== 0) {

      var options = {
        chart: {
          type: 'line',
          height: 400,
        },
        series: [
          {
            name: 'Close',
            data: closePrices
          },
          {
            name: 'Open',
            data: openPrices
          },
          {
            name: 'High',
            data: highPrices
          },
          {
            name: 'low',
            data: lowPrices
          },
          {
            name: 'Adj Close',
            data: adjClosePrices
          },
          {
            name: 'WMA 10',
            data: wma10
          },
          {
            name: 'WMA 20',
            data: wma20
          },
          {
            name: 'WMA 50',
            data: wma50
          },
          {
            name: 'WMA 100',
            data: wma100
          },
        ],
        xaxis: {
          categories: dates
        },
        stroke: {
          width: [1]
        },
      }

      if(!chart){
        let chart = new ApexCharts(document.querySelector("#VolumeAndValueChart"), options)
        chart.render();
        setChart(chart)
      }else{
        chart.updateOptions(options);
      }

    }
  }, [dates])

  return (
    <div>
      <div id="VolumeAndValueChart"></div>
    </div>
  );

}

export default VolumeAndValueChart;