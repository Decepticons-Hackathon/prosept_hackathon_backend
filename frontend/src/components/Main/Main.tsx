import './Main.scss';

interface IProps {
  children: React.ReactNode;
}

const Main: React.FC<IProps> = (props) => {
  return (
    <main className='main'>
      {props.children}
    </main>
  )
}

export default Main;
