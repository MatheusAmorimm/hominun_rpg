export type ItemSlot = 'weapon' | 'armor' | 'consumable' | 'quest' | 'misc';

export interface Item {
  id: string;
  name: string;
  slot: ItemSlot;
  quantity: number;
  description?: string;
}
