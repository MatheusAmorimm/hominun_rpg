import { createRoot } from 'react-dom/client';
import { GameplayScreen } from './presentation/screens/GameplayScreen';
import './styles/index.css';

createRoot(document.getElementById('root')!).render(<GameplayScreen />);
