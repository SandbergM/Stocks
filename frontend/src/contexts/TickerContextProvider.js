import React, { createContext, useEffect, useState } from "react";

export const TickerContext = createContext();

export default function TickerContextProvider(props) {

  const [options, setOptions] = useState([]);
  const [currentTicker, setCurrentTicker] = useState("")
  const [currentCompanyName, setCurrentCompanyName] = useState("")

  const [adjClosePrices, setAdjClosePrices] = useState([]);
  const [dates, setDates] = useState([]);
  const [closePrices, setClosePrices] = useState([]);
  const [openPrices, setOpenPrices] = useState([]);
  const [highPrices, setHighPrices] = useState([]);
  const [lowPrices, setLowPrices] = useState([]);
  const [candleSticksData, setCandleSticksData] = useState([])

  const [bollingerUpper, setBollingerUpper] = useState([]);
  const [bollingerLower, setBollingerLower] = useState([]);
  
  const [wma10, setWma10Data] = useState([]);
  const [wma20, setWma20Data] = useState([]);
  const [wma50, setWma50Data] = useState([]);
  const [wma100, setWma100Data] = useState([]);

  const [chartSetting, setChartSetting] = useState({
    "interval": "1y",
    "b_rate": "10",
    "b_diviation": "2",
  });


  function unpack(rows, key) {
    return rows.map(function (row) { return row[key]; });
  }

  const fetchOptions = async (search = "") => {
    const data = await fetch(`/ticker/ticker_search?company_name_search=${search}`).then((res) => res.json());
    setOptions(data);
  }

  const fetchData = async () => {

    let timeFrame = chartSetting?.interval ? chartSetting?.interval : '3y';
    let b_rate = chartSetting?.b_rate ? chartSetting?.b_rate : '10';
    let b_diviation = chartSetting?.b_diviation ? chartSetting?.b_diviation : '2';

    const tickerData = await fetch(`/ticker/historical_data?ticker=${currentTicker}&timeframe=${timeFrame}&b_rate=${b_rate}&b_diviation=${b_diviation}`).then((res) => res.json());

    let candlesData = []
    let bollingerUpperData = []
    let bollingerLowerData = []
    let wma10Data = []
    let wma20Data = []
    let wma50Data = []
    let wma100Data = []
    let closePricesData = []
    let adjustedClosePricesData = []
    let openPricesData = []
    let lowPricesData = []
    let highPricesData = []
    let dates = []

    tickerData.forEach(e => {

      dates.push(e.date)

      candlesData.push({
        x : e.date,
        y : [ e.open, e.high, e.low, e.close ]
      });
      bollingerUpperData.push({
        x : e.date,
        y : e.b_up
      });
      bollingerLowerData.push({
        x : e.date,
        y : e.b_down
      });
      wma10Data.push({
        x : e.date,
        y : e.wma_10
      });
      wma20Data.push({
        x : e.date,
        y : e.wma_20
      });
      wma50Data.push({
        x : e.date,
        y : e.wma_50
      });
      wma100Data.push({
        x : e.date,
        y : e.wma_100
      });
      wma100Data.push({
        x : e.date,
        y : e.wma_100
      });
      closePricesData.push({
        x : e.date,
        y : e.close
      });
      adjustedClosePricesData.push({
        x : e.date,
        y : e.adj_close
      });
      openPricesData.push({
        x : e.date,
        y : e.open
      });
      lowPricesData.push({
        x : e.date,
        y : e.low
      });
      highPricesData.push({
        x : e.date,
        y : e.low
      });

    });

    setCandleSticksData(candlesData);
    setBollingerLower(bollingerLowerData);
    setBollingerUpper(bollingerUpperData);
    setWma10Data(wma10Data);
    setWma20Data(wma20Data);
    setWma50Data(wma50Data);
    setWma100Data(wma100Data);
    setHighPrices(highPricesData);
    setLowPrices(lowPricesData);
    setOpenPrices(openPricesData);
    setAdjClosePrices(adjustedClosePricesData);
    setClosePrices(closePricesData);
    setDates(dates);

  }

  useEffect(() => {
    if (currentTicker !== "") {
      fetchData()
    }
  }, [currentTicker, chartSetting])

  const values = {
    options,
    fetchOptions,
    currentTicker,
    setCurrentTicker,
    currentCompanyName,
    setCurrentCompanyName,
    setChartSetting,
    chartSetting,
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
    dates
  };

  return (
    <TickerContext.Provider value={values}>{props.children}</TickerContext.Provider>
  );
}
