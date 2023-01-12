import React, { createContext, useEffect, useState } from "react";

export const TickerContext = createContext();

export default function TickerContextProvider(props) {

  const [options, setOptions] = useState([]);
  const [stockData, setStockData] = useState([]);
  const [currentTicker, setCurrentTicker] = useState("")
  const [currentCompanyName, setCurrentCompanyName] = useState("")
  const [updateChart, setUpdateChart] = useState(false)

  const [params, setParams] = useState({
    "interval_type": "year",
    "interval_length": "1",
    "b_rate": "20",
    "b_diviation": "2",
    "wma_1": "20",
    "wma_2": "50",
    "wma_3": "100",
    "rsi_3": "20",
  })

  const fetchOptions = async (search = "") => {
    const data = await fetch(`/ticker/ticker_search?company_name_search=${search}`).then((res) => res.json());
    setOptions(data);
  }

  const getStockData = async () => {
    
    let url = `/ticker/historical_data?ticker=${currentTicker}`
    for (const [key, value] of Object.entries(params)) {
      url = url + `&${key}=${value}`
    }

    let data = {
      "candleData": [],
    }

    const tickerData = await fetch(url).then((res) => res.json());
    if (tickerData.length) {
      Object.entries(tickerData[0]).forEach(([k, v]) => {
        if (!["Company Name", "Date", "Ticker", "Open", "Low", "High", "Adj Close", "Volume"].includes(k))
          data[k] = tickerData.map((el) => {
            return {
              y: el[k],
              x: el.Date
            }
          })
      })

      tickerData.forEach(e => {
        data["candleData"].push({
          y: [e.Open, e.High, e.Low, e.Close],
          x: e.Date
        });
      });
    }

    setStockData(data);
    setUpdateChart(!updateChart);

  }

  useEffect(() => {
    getStockData()
  }, [currentTicker, params])

  const values = {
    options,
    fetchOptions,
    currentTicker,
    setCurrentTicker,
    currentCompanyName,
    setCurrentCompanyName,
    getStockData,
    stockData,
    updateChart,
    params,
    setParams,
  };

  return (
    <TickerContext.Provider value={values}>{props.children}</TickerContext.Provider>
  );
}
