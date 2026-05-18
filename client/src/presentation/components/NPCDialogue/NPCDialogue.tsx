import { motion } from 'motion/react';
import { useGameStore } from '@/game_state/store/gameStore';

export function NPCDialogue() {
  const npc = useGameStore((s) => s.activeNpc);
  const setActiveNpc = useGameStore((s) => s.setActiveNpc);

  if (!npc || !npc.current_dialogue) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="absolute inset-0 z-20"
    >
      <div
        className="absolute inset-0 backdrop-blur-md bg-black/50"
        onClick={() => setActiveNpc(null)}
      />

      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <motion.div
          initial={{ scale: 0.85, y: 40, opacity: 0 }}
          animate={{ scale: 1, y: 0, opacity: 1 }}
          transition={{ delay: 0.15, type: 'spring', damping: 15 }}
          className="relative pointer-events-auto"
        >
          <div className="absolute -inset-4 bg-gold/30 blur-xl rounded-full" />

          <div
            className="relative w-56 h-56 border-8 border-primary rounded-full overflow-hidden"
            style={{ boxShadow: '0 0 40px rgba(212,175,55,0.5), inset 0 0 20px rgba(0,0,0,0.5)' }}
          >
            {npc.portrait_url ? (
              <img src={npc.portrait_url} alt={npc.name} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full bg-secondary flex items-center justify-center text-muted-foreground text-4xl">
                ?
              </div>
            )}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap"
          >
            <div
              className="bg-card border-4 border-primary px-6 py-2"
              style={{ boxShadow: '0 4px 12px rgba(0,0,0,0.8)' }}
            >
              <h3 className="text-gold">{npc.name}</h3>
            </div>
          </motion.div>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.55 }}
        className="absolute bottom-24 left-1/2 -translate-x-1/2 max-w-3xl w-full px-6 pointer-events-auto"
      >
        <div
          className="bg-foreground/95 border-4 border-primary p-6 relative"
          style={{ boxShadow: 'inset 0 0 20px rgba(0,0,0,0.2), 0 8px 16px rgba(0,0,0,0.8)' }}
        >
          <Corner pos="top-2 left-2" dirs="border-t-2 border-l-2" />
          <Corner pos="top-2 right-2" dirs="border-t-2 border-r-2" />
          <Corner pos="bottom-2 left-2" dirs="border-b-2 border-l-2" />
          <Corner pos="bottom-2 right-2" dirs="border-b-2 border-r-2" />
          <p className="text-card leading-relaxed text-center">{npc.current_dialogue}</p>
        </div>

        <button
          onClick={() => setActiveNpc(null)}
          className="mt-4 mx-auto block bg-primary hover:bg-gold text-primary-foreground px-6 py-2 border-2 border-gold transition-colors"
          style={{ boxShadow: '0 4px 8px rgba(0,0,0,0.5)' }}
        >
          Continuar
        </button>
      </motion.div>
    </motion.div>
  );
}

function Corner({ pos, dirs }: { pos: string; dirs: string }) {
  return <div className={`absolute w-4 h-4 border-primary ${pos} ${dirs}`} />;
}
