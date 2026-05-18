import { Settings, Save, BookOpen, User, Map } from 'lucide-react';
import { useGameStore } from '@/game_state/store/gameStore';

export function MenuPanel() {
  const toggleJournal = useGameStore((s) => s.toggleJournal);

  return (
    <div className="h-full flex flex-col p-4 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-secondary/20 to-transparent pointer-events-none" />

      <h3 className="mb-3 text-gold relative border-b-2 border-primary/50 pb-2">Menu Geral</h3>

      <nav className="flex flex-col gap-1 flex-1 relative">
        <NavButton icon={<User className="w-4 h-4" />} label="Personagem" />
        <NavButton icon={<BookOpen className="w-4 h-4" />} label="Diário" onClick={toggleJournal} />
        <NavButton icon={<Map className="w-4 h-4" />} label="Mapa" />
        <NavButton icon={<Save className="w-4 h-4" />} label="Salvar" />
        <div className="flex-1" />
        <NavButton icon={<Settings className="w-4 h-4" />} label="Configurações" />
      </nav>
    </div>
  );
}

interface NavButtonProps {
  icon: React.ReactNode;
  label: string;
  onClick?: () => void;
}

function NavButton({ icon, label, onClick }: NavButtonProps) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2 p-2 border-2 border-transparent hover:border-primary hover:bg-accent transition-all text-sm group"
    >
      <div className="w-8 h-8 flex items-center justify-center bg-secondary border border-primary group-hover:bg-primary transition-colors">
        {icon}
      </div>
      <span>{label}</span>
    </button>
  );
}
