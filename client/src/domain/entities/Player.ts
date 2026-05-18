export interface BaseStats {
  str_: number;
  dex: number;
  con: number;
  int_: number;
  wis: number;
  cha: number;
}

export interface DerivedStats {
  hp: number;
  mana: number;
  initiative: number;
  ether_resistance: number;
}

export interface Player {
  id: string;
  user_id: string;
  name: string;
  race: string;
  archetype: string;
  origin: string;
  base_stats: BaseStats;
  derived_stats: DerivedStats;
  current_hp: number;
  current_mana: number;
  gold: number;
  narrative_flags: Record<string, unknown>;
  active_demon_ids: string[];
}
