import { motion } from 'motion/react';
import { useGameStore } from '@/game_state/store/gameStore';

export function DialoguePanel() {
  const dialogue = useGameStore((s) => s.dialogue);
  const selectedChoiceId = useGameStore((s) => s.selectedChoiceId);
  const selectChoice = useGameStore((s) => s.selectChoice);

  if (!dialogue) return <WaitingState />;

  return (
    <div className="h-full flex flex-col p-6 overflow-hidden relative">
      <div className="absolute inset-0 bg-gradient-to-b from-secondary/20 to-transparent pointer-events-none" />

      <h3 className="mb-3 flex-shrink-0 text-gold relative border-b-2 border-primary/50 pb-2">
        Tomada de Decisão
      </h3>

      <motion.div
        key={dialogue.id}
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-foreground/10 border-4 border-primary p-4 mb-3 flex-shrink-0 relative"
        style={{ boxShadow: 'inset 0 0 20px rgba(0,0,0,0.3), 0 4px 8px rgba(0,0,0,0.5)' }}
      >
        <GoldCorner pos="top-1 left-1" dirs="border-t-2 border-l-2" />
        <GoldCorner pos="top-1 right-1" dirs="border-t-2 border-r-2" />
        <GoldCorner pos="bottom-1 left-1" dirs="border-b-2 border-l-2" />
        <GoldCorner pos="bottom-1 right-1" dirs="border-b-2 border-r-2" />
        <p className="leading-relaxed text-sm text-foreground relative">{dialogue.text}</p>
      </motion.div>

      <div className="flex flex-col gap-2 overflow-y-auto flex-1 relative">
        {dialogue.choices.map((choice, i) => {
          const isSelected = selectedChoiceId === choice.id;
          return (
            <motion.button
              key={choice.id}
              initial={{ opacity: 0, x: -16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.08 }}
              onClick={() => selectChoice(choice.id)}
              className={`p-3 border-2 transition-all text-left flex-shrink-0 text-sm relative ${
                isSelected
                  ? 'bg-primary text-primary-foreground border-gold shadow-[0_0_10px_rgba(212,175,55,0.4)]'
                  : 'border-primary/50 hover:border-primary hover:bg-accent bg-background/50'
              }`}
            >
              <span className={`mr-3 ${isSelected ? 'text-primary-foreground' : 'text-gold'}`}>
                {i + 1}.
              </span>
              {choice.text}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}

function GoldCorner({ pos, dirs }: { pos: string; dirs: string }) {
  return <div className={`absolute w-3 h-3 border-gold ${pos} ${dirs}`} />;
}

function WaitingState() {
  return (
    <div className="h-full flex items-center justify-center">
      <p className="text-muted-foreground text-sm italic">Aguardando o narrador...</p>
    </div>
  );
}
