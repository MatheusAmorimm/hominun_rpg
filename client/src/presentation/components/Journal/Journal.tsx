import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import { X, Flame, Skull, Scroll, Sparkles } from 'lucide-react';
import { useGameStore } from '@/game_state/store/gameStore';

type Tab = 'quests' | 'magic' | 'demonology';

export function Journal() {
  const isOpen = useGameStore((s) => s.isJournalOpen);
  const toggleJournal = useGameStore((s) => s.toggleJournal);
  const session = useGameStore((s) => s.session);
  const [activeTab, setActiveTab] = useState<Tab>('quests');

  if (!isOpen) return null;

  const quests = session?.completed_milestones ?? [];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-8"
    >
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={toggleJournal} />

      <motion.div
        initial={{ scale: 0.92, rotateY: -8 }}
        animate={{ scale: 1, rotateY: 0 }}
        exit={{ scale: 0.92, rotateY: 8 }}
        className="relative w-full max-w-5xl h-[80vh] bg-[#e8dcc4] border-8 border-primary flex"
        style={{ boxShadow: '0 20px 60px rgba(0,0,0,0.9), inset 0 0 40px rgba(139,111,71,0.3)' }}
      >
        <button
          onClick={toggleJournal}
          className="absolute -top-4 -right-4 w-10 h-10 bg-destructive hover:bg-red-600 border-4 border-gold flex items-center justify-center transition-colors z-10"
        >
          <X className="w-5 h-5 text-white" />
        </button>

        {/* Página esquerda — abas */}
        <div className="w-72 border-r-4 border-primary p-6 bg-gradient-to-br from-[#d4c5a0] to-[#e8dcc4]">
          <h2 className="text-[#2a1f1a] mb-6 text-center border-b-4 border-primary pb-3">
            Diário do Aventureiro
          </h2>
          <div className="flex flex-col gap-2">
            <TabButton active={activeTab === 'quests'} onClick={() => setActiveTab('quests')}>
              <Scroll className="w-5 h-5" /> Missões
            </TabButton>
            <TabButton active={activeTab === 'magic'} onClick={() => setActiveTab('magic')}>
              <Sparkles className="w-5 h-5" /> Magia
            </TabButton>
            <TabButton active={activeTab === 'demonology'} onClick={() => setActiveTab('demonology')}>
              <Skull className="w-5 h-5" /> Demonologia
            </TabButton>
          </div>
          <div className="mt-8 pt-8 border-t-2 border-primary">
            <p className="text-center text-primary/40 text-sm italic">
              "O conhecimento é a maior arma do aventureiro"
            </p>
          </div>
        </div>

        {/* Página direita — conteúdo */}
        <div className="flex-1 p-8 overflow-y-auto bg-gradient-to-br from-[#e8dcc4] to-[#f5ebe0]">
          <AnimatePresence mode="wait">
            {activeTab === 'quests' && (
              <TabContent key="quests">
                <h3 className="text-[#2a1f1a] mb-6 flex items-center gap-2">
                  <Scroll className="w-6 h-6 text-primary" /> Missões
                </h3>
                {quests.length === 0 ? (
                  <EmptyNote text="Nenhuma missão registrada ainda." />
                ) : (
                  quests.map((m) => (
                    <JournalEntry key={m} title={m} badge="Completa" badgeClass="bg-green-700 border-green-500" />
                  ))
                )}
              </TabContent>
            )}
            {activeTab === 'magic' && (
              <TabContent key="magic">
                <h3 className="text-[#2a1f1a] mb-6 flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-primary" /> Grimório de Magia
                </h3>
                <EmptyNote text="Nenhum feitiço aprendido ainda." />
              </TabContent>
            )}
            {activeTab === 'demonology' && (
              <TabContent key="demonology">
                <h3 className="text-[#2a1f1a] mb-6 flex items-center gap-2">
                  <Skull className="w-6 h-6 text-primary" /> Bestiário Demoníaco
                </h3>
                <EmptyNote text="Nenhum demônio catalogado ainda." />
              </TabContent>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </motion.div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-3 p-4 border-2 transition-all ${
        active
          ? 'bg-primary text-[#e8dcc4] border-gold shadow-lg'
          : 'bg-[#2a1f1a]/10 border-primary text-[#2a1f1a] hover:bg-primary/30'
      }`}
    >
      {children}
    </button>
  );
}

function TabContent({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 16 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -16 }}
      className="space-y-4"
    >
      {children}
    </motion.div>
  );
}

function JournalEntry({
  title,
  badge,
  badgeClass,
}: {
  title: string;
  badge: string;
  badgeClass: string;
}) {
  return (
    <div className="bg-[#2a1f1a]/5 border-2 border-primary p-4">
      <div className="flex items-start justify-between">
        <h4 className="text-[#2a1f1a]">{title}</h4>
        <span className={`px-2 py-1 text-xs border text-white ${badgeClass}`}>{badge}</span>
      </div>
    </div>
  );
}

function EmptyNote({ text }: { text: string }) {
  return <p className="text-[#2a1f1a]/60 text-sm italic">{text}</p>;
}
