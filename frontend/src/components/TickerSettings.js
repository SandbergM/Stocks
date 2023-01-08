import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { useContext } from 'react'
import { TickerContext } from '../contexts/TickerContextProvider.js';

function TickerSettings() {

  const { setChartSetting, chartSetting } = useContext(TickerContext);

  const intervalOptions = [
    { "name": "1 Week ( Stock data )", "value": "1w" },
    { "name": "2 Weeks ( Stock data )", "value": "2w" },
    { "name": "3 Weeks ( Stock data )", "value": "3w" },
    { "name": "1 Month ( Stock data )", "value": "1m" },
    { "name": "2 Months ( Stock data )", "value": "2m" },
    { "name": "3 Month ( Stock data )", "value": "3m" },
    { "name": "1 Year ( Stock data )", "value": "1y" },
    { "name": "2 Years ( Stock data )", "value": "2y" },
    { "name": "3 Years ( Stock data )", "value": "3y" },
    { "name": "5 Years ( Stock data )", "value": "5y" },
    { "name": "10 Years ( Stock data )", "value": "10y" },
    { "name": "Full history ( Stock data )", "value": "full" },
  ]

  const bollingerDiviationOptions = [
    { "name": "1 Diviation", "value": "1" },
    { "name": "2 Diviation", "value": "2" },
    { "name": "3 Diviation", "value": "3" },
    { "name": "5 Diviation", "value": "5" },
  ]

  const bollingerRateOptions = [
    { "name": "10 Days ( SMA )", "value": "10" },
    { "name": "20 Days ( SMA )", "value": "20" },
    { "name": "30 Days ( SMA )", "value": "30" },
    { "name": "50 Days ( SMA )", "value": "50" },
  ]

  return (
    <Row className="d-flex justify-content-around">
      <Col xs={3}>
        <Form.Select className="settingsSelect" onChange={(e) => {setChartSetting({...chartSetting, 'interval' : e.target.value})}} size="lg">
          { intervalOptions.map((el, idx) => {
            return (
              <option value={el.value} key={idx}> { el.name } </option>
            )
          })}
        </Form.Select>
      </Col>
      <Col xs={3}>
        <Form.Select className="settingsSelect" onChange={(e) => {setChartSetting({...chartSetting, 'b_diviation' : e.target.value})}} size="lg">
          { bollingerDiviationOptions.map((el, idx) => {
            return (
              <option value={el.value} key={idx}> { el.name } </option>
            )
          })}
        </Form.Select>
      </Col>
      <Col xs={3}>
        <Form.Select className="settingsSelect" onChange={(e) => {setChartSetting({...chartSetting, 'b_rate' : e.target.value})}} size="lg">
          { bollingerRateOptions.map((el, idx) => {
            return (
              <option value={el.value} key={idx}> { el.name } </option>
            )
          })}
        </Form.Select>
      </Col>
    </Row>
  );
}

export default TickerSettings