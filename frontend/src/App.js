import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import CompanySearch from './components/CompanySearch';
import TickerSettings from './components/TickerSettings';

import VolumeAndValueChart from './components/TickerCharts/VolumeAndValueChart';
import PriceHistoryCandle from './components/TickerCharts/PriceHistoryCandle';

import TickerContextProvider from './contexts/TickerContextProvider';

function App() {
  return (
    <Container fluid className="App primary-bgc">
      <TickerContextProvider>
        <Row id="companySearchHeader">
          <Col xs={4}>
            <CompanySearch />
          </Col>
          <Col xs={8}>
            <TickerSettings />
          </Col>
        </Row>
        <Row className="justify-content-md-center">
          <Col xs={11}><PriceHistoryCandle /></Col>
        </Row>
      </TickerContextProvider>
    </Container>
  );
}

export default App;
