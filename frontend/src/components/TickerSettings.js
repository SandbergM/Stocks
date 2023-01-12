import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { useContext } from 'react'
import { TickerContext } from '../contexts/TickerContextProvider.js';

function TickerSettings() {

  const { params, setParams } = useContext(TickerContext);

  const intervalOptions = [
    { "name": "1 Week ( Stock data )", "interval_length": 1, "interval_type": "week" },
    { "name": "2 Weeks ( Stock data )", "interval_length": 2, "interval_type": "week" },
    { "name": "3 Weeks ( Stock data )", "interval_length": 3, "interval_type": "week" },
    { "name": "1 Month ( Stock data )", "interval_length": 1, "interval_type": "month" },
    { "name": "2 Months ( Stock data )", "interval_length": 2, "interval_type": "month" },
    { "name": "3 Month ( Stock data )", "interval_length": 3, "interval_type": "month" },
    { "name": "1 Year ( Stock data )", "interval_length": 1, "interval_type": "year" },
    { "name": "2 Years ( Stock data )", "interval_length": 2, "interval_type": "year" },
    { "name": "3 Years ( Stock data )", "interval_length": 3, "interval_type": "year" },
    { "name": "5 Years ( Stock data )", "interval_length": 5, "interval_type": "year" },
    { "name": "10 Years ( Stock data )", "interval_length": 10, "interval_type": "year" },
    { "name": "Full history ( Stock data )", "interval_length": 100, "interval_type": "year" }, ,
  ]

  const updateParams = (e) => {
    intervalOptions.forEach((element) => {
      if (element.name === `${e.target.value}`){
        setParams({ 
          ...params, 
          interval_length: element.interval_length,
          interval_type: element.interval_type
        })
      }
    });
  }

  return (
    <Row className="d-flex justify-content-around">
      <Col xs={12}>
        <Form.Select className="settingsSelect" onChange={(e) => { updateParams(e) }} size="lg">
          {intervalOptions.map((el, idx) => {
            return (
              <option value={el.name} key={idx}> {el.name} </option>
            )
          })}
        </Form.Select>
      </Col>
    </Row>
  );
}

export default TickerSettings