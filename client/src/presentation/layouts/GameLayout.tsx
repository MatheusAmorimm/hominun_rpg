import { MenuPanel } from '../components/MenuPanel/MenuPanel';
import { EnvironmentScene } from '../components/EnvironmentScene/EnvironmentScene';
import { InventoryPanel } from '../components/InventoryPanel/InventoryPanel';
import { DialoguePanel } from '../components/DialoguePanel/DialoguePanel';
import { Journal } from '../components/Journal/Journal';

const BG_TEXTURE = `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%238b6f47' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`;

export function GameLayout() {
  return (
    <div className="size-full grid grid-cols-[280px_1fr] grid-rows-[1fr_400px] bg-background relative">
      {/* Textura de pergaminho */}
      <div
        className="absolute inset-0 opacity-10 pointer-events-none"
        style={{ backgroundImage: BG_TEXTURE }}
      />

      {/* Topo esquerdo — navegação */}
      <div className="border-r-4 border-b-4 border-border bg-card relative shadow-[inset_0_0_20px_rgba(0,0,0,0.5)]">
        <MenuPanel />
      </div>

      {/* Topo direito — cena/ambientação */}
      <div className="border-b-4 border-border relative overflow-hidden bg-black shadow-[inset_0_0_30px_rgba(0,0,0,0.8)]">
        <EnvironmentScene />
      </div>

      {/* Inferior esquerdo — status/mochila */}
      <div className="border-r-4 border-border bg-card relative shadow-[inset_0_0_20px_rgba(0,0,0,0.5)]">
        <InventoryPanel />
      </div>

      {/* Inferior direito — diálogo/escolhas */}
      <div className="bg-card relative shadow-[inset_0_0_20px_rgba(0,0,0,0.5)]">
        <DialoguePanel />
      </div>

      {/* Diário — modal overlay */}
      <Journal />
    </div>
  );
}
