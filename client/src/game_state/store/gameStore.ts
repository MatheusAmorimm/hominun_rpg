import { create } from 'zustand';
import type { Player } from '@/domain/entities/Player';
import type { SessionState } from '@/domain/entities/SessionState';
import type { DialogueNode } from '@/domain/entities/DialogueChoice';
import type { Item } from '@/domain/entities/Item';
import type { Npc } from '@/domain/entities/Npc';

interface TurnState {
  active_player_id: string | null;
  turn_number: number;
  turn_order: string[];
}

interface GameStore {
  player: Player | null;
  session: SessionState | null;
  turn: TurnState;
  dialogue: DialogueNode | null;
  activeNpc: Npc | null;
  inventory: Item[];
  selectedChoiceId: string | null;
  isJournalOpen: boolean;

  setPlayer: (player: Player) => void;
  setSession: (session: SessionState) => void;
  setTurn: (turn: TurnState) => void;
  setDialogue: (node: DialogueNode | null) => void;
  setActiveNpc: (npc: Npc | null) => void;
  setInventory: (items: Item[]) => void;
  selectChoice: (id: string | null) => void;
  toggleJournal: () => void;
}

export const useGameStore = create<GameStore>((set) => ({
  player: null,
  session: null,
  turn: { active_player_id: null, turn_number: 1, turn_order: [] },
  dialogue: null,
  activeNpc: null,
  inventory: [],
  selectedChoiceId: null,
  isJournalOpen: false,

  setPlayer: (player) => set({ player }),
  setSession: (session) => set({ session }),
  setTurn: (turn) => set({ turn }),
  setDialogue: (dialogue) => set({ dialogue }),
  setActiveNpc: (activeNpc) => set({ activeNpc }),
  setInventory: (inventory) => set({ inventory }),
  selectChoice: (selectedChoiceId) => set({ selectedChoiceId }),
  toggleJournal: () => set((s) => ({ isJournalOpen: !s.isJournalOpen })),
}));
