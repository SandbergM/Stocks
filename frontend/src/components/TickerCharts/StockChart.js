
import React from 'react';
import { useEffect, useContext, useState } from 'react'

import { TickerContext } from '../../contexts/TickerContextProvider.js';

import ApexCharts from 'apexcharts'

function StockChart({ chartId }) {

  const { stockData, updateChart } = useContext(TickerContext);
  const [chart, setChart] = useState(false);

  useEffect(() => {
    if (stockData?.Close?.length) {
      let width = []
      let dashes = []
      let series = []
      let yaxis = []
      let rsiAxisSet = false;
      let vals = []

      Object.entries(stockData).forEach(([k, v]) => {
        if (k.split(" ")[0] !== 'RSI') {
          v.forEach((el => {
            if (el.y) {
              vals.push(parseFloat(el.y))
            }
          }));
        }
      });

      let maxVal = parseInt(Math.max.apply(Math, vals));
      let minVal = parseInt(Math.min.apply(Math, vals));
      
      Object.entries(stockData).forEach(([k, v]) => {

        series.push({ name: k, type: k !== 'candleData' ? 'line' : "candlestick", data: v })
        dashes.push(k.split(" ")[0] === "WMA" ? 5 : 0)
        width.push(k.split(" ")[0] === "WMA" ? 3 : 2)

        if (k.split(" ")[0] === "RSI") {
          yaxis.push({
            tickAmount: 10,
            seriesName: k,
            opposite: true,
            max: 100,
            min: 0,
            show: true,
            labels: { style: { colors: '#6c757d' } },
            title: { text: "RSI", style: { color: '#6c757d' } },
          });

          rsiAxisSet = true

        } else {

          yaxis.push({
            seriesName: k,
            tickAmount: 10,
            opposite: false,
            floating: false,
            max: maxVal,
            min: minVal,
            show: k === 'candleData',
            labels: { style: { colors: '#6c757d' } },
            title: { text: k !== 'candleData' ? k : "Value", style: { color: '#6c757d' } },
          });

        }

      });
      
      width.push(1)
      dashes.push(0)

      var options = {
        series: series,
        chart: {
          height: 700,
          type: 'line',
        },
        stroke: {
          width: width,
          curve: 'straight',
          dashArray: dashes,
        },
        yaxis: yaxis,
        tooltip: {
          fixed: {
            enabled: true,
            position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
            offsetY: 30,
            offsetX: 60
          },
        },
        legend: {
          horizontalAlign: 'left',
          offsetX: 40
        }
      };

      if (!chart) {
        let chart = new ApexCharts(document.querySelector("#" + chartId), options)
        chart.render();
        setChart(chart)
      } else {
        chart.updateOptions(options);
      }

    }
  }, [updateChart])

  return (
    <div>
      <div id={chartId}></div>
    </div>
  );

}

export default StockChart;