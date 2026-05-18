export interface SessionState {
  session_id: string;
  player_id: string;
  current_region: string;
  current_scene: string;
  faction_reputations: Record<string, number>;
  unlocked_nodes: string[];
  completed_milestones: string[];
  save_version: number;
}
