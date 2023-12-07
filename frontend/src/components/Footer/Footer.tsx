import './Footer.scss';

import logo from "../../assets/images/logom2.svg";

const Footer: React.FC = () => {
  return (
    <footer className='footer'>
      <img src={logo} className='logo' alt="Логотип компании Prosept" />
      <p className='text'>#PROSEPTfamily</p>
      <p className='text'>#PROSEPTlive</p>
    </footer>
  )
}

export default Footer;
