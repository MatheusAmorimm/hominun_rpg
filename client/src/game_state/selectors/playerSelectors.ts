import type { Player } from '@/domain/entities/Player';

export const hpPercent = (player: Player): number =>
  Math.round((player.current_hp / player.derived_stats.hp) * 100);

export const manaPercent = (player: Player): number =>
  Math.round((player.current_mana / player.derived_stats.mana) * 100);
