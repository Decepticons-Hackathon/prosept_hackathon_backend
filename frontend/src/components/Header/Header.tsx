import GradientButton from "../GradientButton/GradientButton";
import { Link } from "react-router-dom";

import './Header.scss';
import logo from "../../assets/images/prosept-logo.svg";

const Header: React.FC = () => {
  return (
    <header className='header'>
      <img src={logo} className='logo' alt="Логотип компании Prosept" />
      <GradientButton>Инструкция</GradientButton>
      <Link to='/comparehistory'><GradientButton>Открыть историю</GradientButton></Link>
    </header>
  )
}

export default Header;
