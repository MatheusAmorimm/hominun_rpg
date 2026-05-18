import { Heart, Zap, Coins, Sword, Shield, Scroll } from 'lucide-react';
import { useGameStore } from '@/game_state/store/gameStore';
import { hpPercent, manaPercent } from '@/game_state/selectors/playerSelectors';
import { StatBar } from '../ui/StatBar';

export function InventoryPanel() {
  const player = useGameStore((s) => s.player);
  const inventory = useGameStore((s) => s.inventory);

  if (!player) return <EmptyState />;

  return (
    <div className="h-full flex flex-col p-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-secondary/20 to-transparent pointer-events-none" />

      <h3 className="mb-4 text-gold relative border-b-2 border-primary/50 pb-2">Status</h3>

      <div className="flex flex-col gap-3 mb-6 relative">
        <StatBar
          label="Vida"
          current={player.current_hp}
          max={player.derived_stats.hp}
          icon={<Heart className="w-4 h-4 text-hp" />}
          iconBgClass="bg-hp-bg/20 border-hp-bg"
          barClass="bg-gradient-to-r from-hp-bg to-hp"
        />
        <StatBar
          label="Mana"
          current={player.current_mana}
          max={player.derived_stats.mana}
          icon={<Zap className="w-4 h-4 text-mana" />}
          iconBgClass="bg-mana-bg/20 border-mana-bg"
          barClass="bg-gradient-to-r from-mana-bg to-mana"
        />
        <div className="flex items-center gap-3 p-2 bg-background/50 border-2 border-primary/30">
          <div className="w-8 h-8 bg-gold/20 border border-gold flex items-center justify-center">
            <Coins className="w-4 h-4 text-gold" />
          </div>
          <div className="flex-1 text-xs text-muted-foreground">Ouro</div>
          <span className="text-sm text-gold">{player.gold}</span>
        </div>
      </div>

      <h3 className="mb-3 text-gold relative border-b-2 border-primary/50 pb-2">Mochila</h3>

      <div className="flex flex-col gap-2 flex-1 overflow-y-auto relative">
        {inventory.length === 0 ? (
          <p className="text-muted-foreground text-sm italic">Inventário vazio.</p>
        ) : (
          inventory.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-3 p-2 bg-background/50 border-2 border-primary/30 hover:border-primary hover:bg-accent/50 transition-all cursor-pointer"
            >
              <div className="w-8 h-8 bg-secondary border border-primary flex items-center justify-center">
                <ItemIcon slot={item.slot} />
              </div>
              <p className="flex-1 text-sm">{item.name}</p>
              <span className="text-sm text-gold">x{item.quantity}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function ItemIcon({ slot }: { slot: string }) {
  if (slot === 'weapon') return <Sword className="w-4 h-4" />;
  if (slot === 'armor') return <Shield className="w-4 h-4" />;
  return <Scroll className="w-4 h-4" />;
}

function EmptyState() {
  return (
    <div className="h-full flex items-center justify-center">
      <p className="text-muted-foreground text-sm italic">Carregando personagem...</p>
    </div>
  );
}
