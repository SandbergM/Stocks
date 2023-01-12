import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import CompanySearch from './components/CompanySearch';

import StockChart from './components/TickerCharts/StockChart';
import TickerSettings from './components/TickerSettings';

import TickerContextProvider from './contexts/TickerContextProvider';

function App() {

  return (
    <Container fluid className="App primary-bgc">
      <TickerContextProvider>
        <Row id="companySearchHeader" className="justify-content-md-center">
          <Col xs={4}>
            <CompanySearch />
          </Col>
        </Row>
        <Row className="justify-content-md-center">
          <Col xs={4}>
            <TickerSettings />
          </Col>
        </Row>
        <Row className="justify-content-md-around">
          <Col xs={11}><StockChart chartId={`chart1`}  /></Col>
        </Row>
      </TickerContextProvider>
    </Container>
  );
}

export default App;
