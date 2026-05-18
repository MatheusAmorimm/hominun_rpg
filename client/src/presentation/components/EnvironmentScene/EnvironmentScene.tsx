import { motion } from 'motion/react';
import { useGameStore } from '@/game_state/store/gameStore';
import { FloatingParticles } from './FloatingParticles';
import { NPCDialogue } from '../NPCDialogue/NPCDialogue';

const SCENE_FALLBACK = 'https://images.unsplash.com/photo-1511497584788-876760111969?w=1920&q=80';

export function EnvironmentScene() {
  const session = useGameStore((s) => s.session);

  const regionName = session?.current_region ?? 'Mundo Desconhecido';

  return (
    <div className="absolute inset-0 overflow-hidden">
      {/* Moldura medieval com ornamentos dourados */}
      <div
        className="absolute inset-0 border-8 border-primary pointer-events-none z-10"
        style={{ boxShadow: 'inset 0 0 30px rgba(0,0,0,0.8), inset 0 0 60px rgba(139,111,71,0.3)' }}
      >
        <GoldCorner pos="top-0 left-0" dirs="border-t-4 border-l-4" size="w-16 h-16" />
        <GoldCorner pos="top-0 right-0" dirs="border-t-4 border-r-4" size="w-16 h-16" />
        <GoldCorner pos="bottom-0 left-0" dirs="border-b-4 border-l-4" size="w-16 h-16" />
        <GoldCorner pos="bottom-0 right-0" dirs="border-b-4 border-r-4" size="w-16 h-16" />
        <Dot pos="top-2 left-2" />
        <Dot pos="top-2 right-2" />
        <Dot pos="bottom-2 left-2" />
        <Dot pos="bottom-2 right-2" />
      </div>

      {/* Imagem de fundo com entrada suave */}
      <motion.div
        initial={{ scale: 1.08, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1.5, ease: 'easeOut' }}
        className="absolute inset-0"
      >
        <img
          src={SCENE_FALLBACK}
          alt={regionName}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background/60 via-transparent to-background/80" />
        <div
          className="absolute inset-0"
          style={{ background: 'radial-gradient(ellipse at center, transparent 30%, rgba(26,20,16,0.8) 100%)' }}
        />
      </motion.div>

      {/* Nome da região */}
      <div className="absolute top-10 left-1/2 -translate-x-1/2 z-10">
        <h2 className="text-gold text-shadow px-4 py-1 border-b border-gold/50">{regionName}</h2>
      </div>

      <FloatingParticles />

      {/* Névoa animada */}
      <motion.div
        className="absolute bottom-0 left-0 right-0 h-1/3 pointer-events-none"
        style={{ background: 'linear-gradient(to top, rgba(139,111,71,0.2), transparent)' }}
        animate={{ opacity: [0.3, 0.7, 0.3] }}
        transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Diálogo de NPC */}
      <NPCDialogue />
    </div>
  );
}

function GoldCorner({ pos, dirs, size }: { pos: string; dirs: string; size: string }) {
  return <div className={`absolute border-gold ${pos} ${dirs} ${size}`} />;
}

function Dot({ pos }: { pos: string }) {
  return <div className={`absolute w-2 h-2 bg-gold rounded-full ${pos}`} />;
}
