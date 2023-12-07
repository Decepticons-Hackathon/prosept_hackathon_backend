import "./App.scss";
import "./Antd.scss";
import "../../assets/fonts/fonts.scss";
import 'normalize.css';
import { Routes, Route } from 'react-router-dom';
import Header from "../Header/Header";
import Footer from "../Footer/Footer";
import ResultTable from "../ResultTable/ResultTable";
import Main from "../Main/Main";

const App: React.FC = () => {
  return (
    <div className="page">
      <Header />
      <Routes>
        <Route path="/" element={
          <Main>
            <ResultTable />
          </Main>
        } />
        <Route path="/matching" element={
          <Main>
            {/* <Matching /> */}
          </Main>
        } />
        <Route path="/instructions" element={
          <Main>
            {/* <Instructions /> */}
          </Main>
        } />
        <Route path="/statistics" element={
          <Main>
            {/* <Statistics /> */}
          </Main>
        } />
      </Routes>
      <Footer />
    </div>
  );
}

export default App;
