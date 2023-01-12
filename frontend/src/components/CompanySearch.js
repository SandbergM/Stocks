
import React, { useContext, useEffect, useRef, useState } from 'react';

import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import useDebounce from '../hooks/useDebounce';
import { TickerContext } from '../contexts/TickerContextProvider.js';

function CompanySearch(args) {

  const { options, fetchOptions, setCurrentTicker, setCurrentCompanyName, currentGain } = useContext(TickerContext);

  const [search, setSearch] = useState("");
  const [display, setDisplay] = useState(false);

  const wrapperRef = useRef(null);
  const debounceSearch = useDebounce(search, 100);

  const querySearch = (searchFrase) => {
    setSearch(searchFrase)
    if (!display) {
      setDisplay(true);
    }
  }

  const handleClickOutSide = event => {
    const { current: wrap } = wrapperRef;
    if (wrap && !wrap.contains(event.target)) {
      setDisplay(false);
    }
  }

  const selectOption = (companyName, ticker) => {
    setCurrentTicker(ticker);
    setCurrentCompanyName(companyName)
    setSearch(companyName);
    setDisplay(false);
  }

  // useEffect's
  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutSide);
    return () => {
      document.removeEventListener("mousedown", handleClickOutSide);
    }
  }, [])

  useEffect(() => {
    if (debounceSearch) {
      fetchOptions(debounceSearch)
    }
  }, [debounceSearch])

  return (
    <Row className="justify-content-center">
      <p className="text-warning"> {currentGain} </p>
      <Col xs={12}>
        <Form className="mt-4" >
          <Form.Control
            type="text"
            id="company-search-input"
            className="primary-bgc secondary-boarder"
            placeholder="Search"
            onChange={(e) => querySearch(e.target.value)}
            onClick={() => { setDisplay(true) }}
            value={search}
          />
          {display && options.length && (
            <Col xs={2} className="autoContainer mt-2" ref={wrapperRef}>
              {options.map((v, i) => {
                return (
                  <div className="option mb-3" key={i} onClick={() => selectOption(v.company_name, v.ticker)}>
                    <Row>
                      <Col xs={12}> {v.company_name} </Col>
                      <Col xs={12} className="ticker-info"> {v.ticker} </Col>
                      <Col xs={12} className="ticker-info"> {v.country} </Col>
                    </Row>
                  </div>);
              })}
            </Col>
          )}
        </Form>
      </Col>
    </Row>
  );
}

export default CompanySearch;